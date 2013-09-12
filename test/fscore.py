import csv


matchs = {}
matchs["++"] = 0
matchs["--"] = 0
matchs["??"] = 0

matchs["+-"] = 0
matchs["+?"] = 0
matchs["-+"] = 0
matchs["-?"] = 0
matchs["?+"] = 0
matchs["?-"] = 0

f_in = open("results.tsv", "r")
tsv_reader = csv.reader(f_in, delimiter='\t')
for row in tsv_reader:
    if len(row) == 4:
        t = row[0]
        e = float(row[1])

        if t=="+" and e > 0.0:
            matchs["++"] += 1
        elif t=="-" and e < 0.0:
            matchs["--"] += 1
        elif t=="?" and e == 0.0:
            #matchs["??"] += 1
            pass
        elif t=="+" and e < 0.0:
            matchs["+-"] += 1
        elif t=="+" and e == 0.0:
            #matchs["+?"] += 1
            pass
        elif t=="-" and e > 0.0:
            matchs["-+"] += 1
        elif t=="-" and e == 0.0:
            #matchs["-?"] += 1
            pass
        elif t=="?" and e > 0.0:
            matchs["?+"] += 1
        elif t=="?" and e < 0.0:
            matchs["?-"] += 1

success = matchs["++"]+matchs["--"]+matchs["??"]
fails = matchs["+-"]+matchs["+?"]+matchs["-+"]+matchs["-?"]+matchs["?+"]+matchs["?-"]
total = sum([matchs[k] for k in matchs])

print("Tagged = infered")
for match in matchs:
    print("%s = %s" %(match, matchs[match]))

print("\nPrecision:%s%% Recall:%s%%" % (((100*success)/total), ((100*fails)/total)))

