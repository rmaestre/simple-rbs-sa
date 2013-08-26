from pymongo import *


config = {}
config['db'] = {}
config['db']['host'] = "web40"
config['db']['port'] = 27017
config['db']['db'] = "wordnet"


synsets = {}
connection = Connection(config['db']['host'], config['db']['port'])
db = connection[config['db']['db']]
collection = db["words"]
for item in collection.find():
    if item["index"] == 0:
        synsets[item["synset"]] = item["word"]
print("loaded %s synsets" % len(synsets))


connection = Connection(config['db']['host'], config['db']['port'])
db = connection[config['db']['db']]
collection = db["synsets"]
meaning = {}
for item in collection.find():
    meaning[item["synset"]] = item["meaning"]
print("loaded %s meanings" % len(synsets))
0/0

f_in = file("dump/SentiWordNet_3.0.0_20130122.txt", "r")
cont = 0
for line in f_in:
    chunks = line.split("\t")
    if len(chunks) == 6 and len(chunks[0]) == 1:
        line = {"synset": chunks[1], "pos": chunks[0], 
                    "positive": float(chunks[2]), "negative": float(chunks[3])}
        if chunks[1] in synsets and (line["positive"] != 0.0 or line["negative"] != 0.0):
            # Get definition
            line["meaning"] = meaning[line["synset"]]
            line["word_en"] = synsets[chunks[1]]
            print("%s\n" % line)
            cont +=1
f_in.close()

print("Total: %s" % cont)