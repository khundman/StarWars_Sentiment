from bs4 import BeautifulSoup
import requests
import re
from whoosh.index import create_in, open_dir
from whoosh.fields import * 
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh import highlight
import lists
import textwrap
from collections import Counter
import os
import math

# Write index
def write(path):
	#create index directory
	if not os.path.exists(path):
	    os.mkdir(path)
	schema = Schema(quote=TEXT(stored=True), affiliation=TEXT(stored=True), force=TEXT(stored=True), name=TEXT(stored=True), count=NUMERIC(stored=True))
	ix = create_in(path, schema)
	writer = ix.writer()

	# Bring down HTML
	r = requests.get("http://www.imsdb.com/scripts/Star-Wars-A-New-Hope.html")
	data = r.text
	quote_counter = 0
	sections = re.split('<b>', data)

	for section in sections:
		quote_counter += 1
		match = re.search('([A-Z])+(( )*([A-Z])*)*((\n)(.)+)+', section, re.MULTILINE)
		if match:
			string = match.group(0)
			string = re.sub('\n',' ', string)
			split = re.split('</b>', string)
			name = str(split[0].strip())
			quote = textwrap.dedent(str(split[1].strip()))
			quote = re.sub('  ','',quote)
			end_paren = ')'
			if end_paren in quote:
				quote = re.sub('\(.*\)','', quote)
			for char in lists.characters:
				for charName in char['Name']:
					if name.lower() == charName.lower():
						nameFirst = char['Name'][0].upper()
						affil = char['Affiliation']
						forceType = char['Force']
						writer.add_document(quote = quote, affiliation = affil, force = forceType, name = nameFirst, count = quote_counter)
	writer.commit()

# All quotes to text file, depending on affiliation
#--------------------------
def affiliations(ind):
	affils = [u"Rebel Alliance", u"Empire", u"None"]
	affilParser = QueryParser("affiliation", schema=ind.schema)

	for affil in affils:
		query = affilParser.parse(affil)
		with ind.searcher() as searcher:
			results = searcher.search(query, limit=None)
			with open('/users/kh/desktop/star_wars/SW_' + str(affil) + '.txt','w') as f:
				# f.write("Result count: " + str(len(results)) + "\n")
				for result in results:
					f.write(str(result['count']) + ': ' + str(result['quote']) + "\n")

# Search index
def search(path):
	ix = open_dir(path)
	# print(ix.doc_count())
	for x in ix.searcher().documents():
		print(str(x['count']))
		print(str(x['quote']))
	# affiliations(ix)
	
def count_sentiment(path, allegiance):
	sentiments = []
	file = open(path)
	raw = file.read()
	neg_count = Counter(re.findall(r"Negative", raw))
	very_neg_count = Counter(re.findall(r"Very negative", raw))
	pos_count = Counter(re.findall(r"Positive", raw))
	very_pos_count = Counter(re.findall(r"Very positive", raw))
	neut_count = Counter(re.findall(r"Neutral", raw))
	total = neg_count["Negative"] + pos_count["Positive"] + neut_count["Neutral"] # add "very"
	neg_percent = neg_count["Negative"] / total
	very_neg_percent = very_neg_count["Very negative"] / total
	pos_percent = pos_count["Positive"] / total
	very_pos_percent = very_pos_count["Very positive"] / total
	neut_percent = neut_count["Neutral"] / total
	with open('Sent_Count_' + str(allegiance) + '.txt','w') as f:
		f.write(str(neg_count) + "\n")
		f.write("Percent of total: "+ str(neg_percent) + "\n")
		f.write(str(very_neg_count) + "\n")
		f.write("Percent of total: "+ str(very_neg_percent) + "\n")
		f.write(str(pos_count) + "\n")
		f.write("Percent of total: "+ str(pos_percent) + "\n")
		f.write(str(very_pos_count) + "\n")
		f.write("Percent of total: "+ str(very_pos_percent) + "\n")
		f.write(str(neut_count) + "\n")
		f.write("Percent of total: "+ str(neut_percent) + "\n")

def sentiment(quote_path, allegiance):
	file = open(quote_path)
	raw = file.read()
	os.system('java -cp "*" -mx5g edu.stanford.nlp.sentiment.SentimentPipeline -file ' + str(quote_path) + 
		' > /users/kh/desktop/star_wars/' + str(allegiance) + '_sentiment.txt')

def moving_average(sent_path, allegiance):
	file = open(sent_path)
	raw = file.read()
	list_1 = re.split('\n', raw)
	moving_avgs = {}
	cursor = 0
	win_start = 0
	win_end = 30
	quote_count = ':'
	while cursor < len(list_1):
		temp_qc = []
		score = []
		while cursor < win_end:
			if win_end >= len(list_1):
				win_end = len(list_1)
			if quote_count in list_1[cursor]:
				temp_split = re.split(':', list_1[cursor])
				temp_qc.append(int(temp_split[0]))
			if "Negative" in list_1[cursor]:
				score.append(-1)
			if "Positive" in list_1[cursor]:
				score.append(1)
			if "Neutral" in list_1[cursor]:
				pass
			if "Very negative" in list_1[cursor]:
				score.append(-3)
			if "Very positive" in list_1[cursor]:
				score.append(3)
			cursor += 1
		moving_avgs[(win_start/30)] = [(int(sum(temp_qc)/len(temp_qc))), (sum(score)/len(score))]
		win_start += 15
		win_end += 15
	with open('/users/kh/desktop/star_wars/MovingAvg_' + str(allegiance) + '.txt','w') as f:
		f.write('Window Number, Average Quote Count, Sentiment Score, Allegiance' + '\n')
		for key,value in moving_avgs.items():
			str_value = str(value)
			clean_value = re.sub("\[","", str_value)
			clean_value = re.sub("]","", clean_value)
			f.write(str(key) + ', ' + str(clean_value) + ', ' + str(allegiance) + '\n')

def concat(file1, file2, output):
	file = open(file1)
	file2 = open(file2)
	raw = file.read()
	raw2 = file2.read()
	together = raw + raw2
	with open(output,'w') as f:
		f.write(together)

if __name__ == "__main__":
	path = "/Users/kh/desktop/star_wars/StarWars_index"

	# quote_path_rebel = "/users/kh/desktop/star_wars/SW_Rebel_Alliance.txt"
	# quote_path_none = "/users/kh/desktop/star_wars/SW_None.txt"
	# quote_path_empire = "/users/kh/desktop/star_wars/SW_Empire.txt"

	sent_path_rebel = "/users/kh/desktop/star_wars/rebel_sentiment.txt"
	sent_path_empire = "/users/kh/desktop/star_wars/empire_sentiment.txt"
	sent_path_none = "/users/kh/desktop/star_wars/none_sentiment.txt"

	concat1 = "/users/kh/desktop/star_wars/MovingAvg_Rebel.txt"
	concat2 = "/users/kh/desktop/star_wars/MovingAvg_Empire.txt"
	output = "/users/kh/desktop/star_wars/MovingAvg_Both.txt"
	
	# write(path)
	search(path)
	# sentiment(quote_path_rebel, "rebel")
	# sentiment(quote_path_none, "none")
	# sentiment(quote_path_empire, "empire")
	# moving_average(sent_path_rebel, 'Rebel')
	# moving_average(sent_path_empire, 'Empire')
	# moving_average(sent_path_none, 'None')
	# concat(concat1, concat2, output)



