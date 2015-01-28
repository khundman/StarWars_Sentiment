characters = []

def chars(name_list, side, force="None"):
	obj = {'Name': name_list, 'Affiliation': side, 'Force': force}
	characters.append(obj)

chars(["Ackbar", "Admiral Ackbar"],"Rebel Alliance")
chars(["Anakin", "Anakin Skywalker", "Darth Vader", "Vader"],"Empire","Sith")
chars(["Biggs", "Red 3"],"Rebel Alliance", "None")
chars(["Boba", "Boba Fett"],"None")
chars(["C-3PO", "Threepio"],"Rebel Alliance")
chars(["Chewbacca", "Chewie"],"Rebel Alliance")
chars(["Dooku", "Count Dooku", "Tyranus", "Darth Tyranus"],"Empire","Sith")
chars(["Dodonna"], "Rebel Alliance", "None")
chars(["Darth Maul"],"Empire","Sith")
chars(["General Grievous"],"Empire","Sith")
chars(["Grand Moff Tarkin", "Tarkin", "Governor Tarkin"],"Empire")
chars(["Greedo"],"None")
chars(["Han Solo", "Han", "Solo"],"Rebel Alliance")
chars(["Imperial Officer"], "Empire", "None")
chars(["Jabba the Hutt", "Jabba", "Jabba Desilijic Tiure"],"None")
chars(["Jango Fett", "Jango"],"None")
chars(["Jar Jar Binks", "Jar Jar", "Binks"],"Rebel Alliance")
chars(["Lando Calrissian", "Lando", "Calrissian"],"Rebel Alliance")
chars(["Luke Skywalker", "Luke", "Red 5"],"Rebel Alliance","Jedi")
chars(["Mace Windu", "Windu"],"Rebel Alliance","Jedi")
chars(["Mon Mothma", "Mon", "Mothma"],"Rebel Alliance", "None")
chars(["Motti"], "Empire", "None")
chars(["Nute Gunray", "Nute", "Gunray"],"Empire")
chars(["Owen"], "None", "None")
chars(["Aunt Beru"], "None", "None")
chars(["Obi-Wan Kenobi", "Obi-Wan", "Kenobi", "Ben"],"Rebel Alliance","Jedi")
chars(["Padmé Amidala", "Padmé", "Padme", "Amidala"],"Rebel Alliance")
chars(["Emperor Palpatine", "Palpatine", "Sidious", "Darth Sidious"],"Empire","Sith")
chars(["Princess Leia", "Leia"],"Rebel Alliance")
chars(["Qui-Gon Jinn", "Qui-Gon"],"Rebel Alliance","Jedi")
chars(["R2-D2", "R2", "Artoo"],"Rebel Alliance")
chars(["Trooper"], "Empire", "None")
chars(["Watto"],"None")
chars(["Wedge Antilles", "Wedge", "Antilles", "Red Two"],"Rebel Alliance")
chars(["Yoda", "Master Yoda"],"Rebel Alliance","Jedi")

places = ["Alderaan","Bespin","Cato Neimoidia","Centax-1","Centax-2","Centax-3","Chenini","Corellia","Coruscant","Dagobah","Dantooine","Endor","Forest moon of Endor","Felucia","Geonosis","Ghomrassen","Guermessa","Hesperidium","Hoth","Jestefad","Kamino","Kashyyyk","Mustafar","Mygeeto","Naboo","Ohma-D'un","Polis Massa","Rori","Saleucami","Tatooine","Utapau","Yavin"]

vehicles = ["Landspeeder","Snowspeeder","Speeder bike","Walkers","A-wing","B-wing","Jedi starfighter","TIE fighters","X-wing","Y-wing","Death Star","Millennium Falcon","Mon Calamari cruiser","Nebulon-B frigate","Slave I","Star Destroyer","Eclipse-class dreadnought","Tantive IV"]