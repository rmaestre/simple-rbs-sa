import requests
import csv
import json

def request(text):
    """ """
    r = requests.get("http://localhost:8080", params = {"text": text})
    try:
        return json.loads(r.text)
    except:
        aux = {}
        aux["matches"] = {}
        return aux


f_out = open("/tmp/results.tsv", "w")
f_in = open("corpus.tsv", "r")
tsv_reader = csv.reader(f_in, delimiter='\t')
for row in tsv_reader:

    print(row[0]) 

    if len(row) == 2:
        data = request(row[0])
        score = 0.0
        for match in data["matches"]:
            score += data["matches"][match]["score"]

        out = "%s\t%s\t%s\t%s\n" % (row[1],  score, row[0], data["matches"])
        #print(out)
        f_out.write(out)
f_out.close()
    