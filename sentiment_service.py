# encoding: utf-8

import tornado.ioloop
import tornado.web
import sys
import getopt
import time
import re
import ply.yacc as yacc
from sa_lex import tokens
from treetagger import TreeTagger
from treetagger_wordnet import TreetaggerToWordnet
from sentiwordnet import SentiWordnet
import csv

class MainHandler(tornado.web.RequestHandler):
    """ """

    def initialize(self, to_wordnet, sentiwordnet, tt, rules, stopwords, chunks, language):
        """ """
        self.rules = rules
        self.chunks = chunks
        self.language = language
        self.stopwords = stopwords
        self.sentiwordnet = sentiwordnet
        self.tt = tt
        self.to_wordnet = to_wordnet

    def get(self):
        """ """
        # Start operation time
        time_start = time.time()
        # Prepare the response DS
        response = {}

        # Check input text
        text = self.get_argument("text")
        text = text.replace("\n", "")
        text = text.encode("utf-8")
        response["raw_text"] = text

        # Replace chunks symbols
        for chunk in self.chunks:
            text = text.replace(chunk, " # ")

        # Mapping treetagger postaging to wordnet postagging
        aux = ""
        for tag in self.tt.tag(text):
            lemma = tag[2]
            if lemma == u"<unknown>":
                lemma = tag[0]
            aux += "%s.%s " % (lemma, self.to_wordnet.wordnet_morph_category(self.language, tag[1]))
        text = aux

        # Replace stopwords for the entities
        for stopword in self.stopwords:
            text = text.replace(stopword, " ")

        # Replace postagging for the entities
        aux = ""
        chunks = text.split(" ")
        for chunk in chunks:
            sub_chunks = chunk.split(".")
            if sub_chunks[0].lower() in entities or sub_chunks[0].lower() in inverters:
                aux += "%s " % sub_chunks[0].lower()
            else:
                aux += "%s " % chunk
        text = aux

        # Detecting Words with sentiment (Sentiwordnet)
        aux = ""
        chunks = text.split(" ")
        for chunk in chunks:
            aux += chunk
            sub_chunks = chunk.split(".")
            if len(sub_chunks) > 1:

                # Apply sentiwordnet dictionary
                senti = self.sentiwordnet.get_sentiment(sub_chunks[0], 
                            sub_chunks[1], 
                            language)

                # Calculate score
                score = 0.0
                if senti is not None:
                    score = float(senti["positive"]) + float(senti["negative"])
                if score < 0.0:
                    aux += "%s" % score
                elif score > 0.0:
                    aux += "+%s" % score
            # Return keyword
            aux += " "
        text = aux
        response["text"] = text

        # Split input text
        chunks = text.split('#.None')
        triggered_rule_cont = 0
        response["matches"] = {}

        for chunk in chunks:
            chunk =' '.join(chunk.split())

            # Apply rules and replace matchs
            rule_triggered = False
            while True:

                # Appling all rules over the text
                rule_triggered = False
                for rule in compiled_rules:
                    for match in compiled_rules[rule]["regex"].finditer(chunk):
                        rule_triggered = True
                        response["matches"][triggered_rule_cont] = {}
                        response["matches"][triggered_rule_cont]["rule_triggered"] = rule
                        response["matches"][triggered_rule_cont]["score"] = compiled_rules[rule]["score"]
                        response["matches"][triggered_rule_cont]["match"] = match.group()

                        # Replace chunk with "***"" filling
                        aux = ""
                        for e in match.group().split(" "):
                            aux += "*" * len(e) + " "
                        aux = aux[0:len(aux)-2]

                        # Perfom replace
                        chunk = chunk.replace(match.group(), aux)
                        triggered_rule_cont += 1
                # Break rule matching (precedence behavior)
                if not rule_triggered:
                    break
        # Return response
        response["elipsed_time"] = time.time() - time_start

        # Return result
        self.write(response)

# Variables to manage values in the parser process
start = 'rule'
regex = ''
compiled_rules = {}
adhoc_sentiwords = {}

def p_rule(p):
    'rule : BEGINRULE expression THEN SCORE ENDRULE'
    if p[1] in compiled_rules:
        print("Error: Rule #ID duplicated.")
        sys.exit(0)

    # Replace special character "#" and cast to integer
    # This is main to sort the rules dictionary and to 
    # apply them in order
    rule_id = int(p[1].replace("#", ""))

    # Save rule
    compiled_rules[rule_id] = {}
    compiled_rules[rule_id]["regex"] = regex
    compiled_rules[rule_id]["score"] = float(p[4])
    #print(regex.pattern)


def p_expresion_simple_one(p):
    'expression : QUALIFICATOR ENTITY'
    global regex
    if p[1] == "+":
        regex = re.compile("(\w+\.\w(\%s)(\d+.\d+)+)(\s\S+){0,3}\s%s" % (combined_positives, combined_entities))
    else:
        regex = re.compile("(\w+\.\w(\%s)(\d+.\d+)+)(\s\S+){0,3}\s%s" % (combined_negatives, combined_entities))

def p_expresion_simple_two(p):
    'expression : ENTITY QUALIFICATOR'
    global regex
    if p[2] == "+":
        regex = re.compile("%s(\s\S+){0,3}\s(\w+\.\w(\%s)(\d+.\d+)+)" % (combined_entities, combined_positives))
    else:
        regex = re.compile("%s(\s\S+){0,3}\s(\w+\.\w(\%s)(\d+.\d+)+)" % (combined_entities, combined_negatives))

def p_expresion_simple_swaping_one(p):
    'expression : SWAP QUALIFICATOR ENTITY'
    global regex
    if p[2] == "+":
         regex = re.compile("%s(\s\S+){0,3}\s(\w+\.\w(\%s)(\d+.\d+)+)(\s\S+){0,3}\s%s" % (combined_inverters, combined_positives, combined_entities))
    else:
         regex = re.compile("%s(\s\S+){0,3}\s(\w+\.\w(\%s)(\d+.\d+)+)(\s\S+){0,3}\s%s" % (combined_inverters, combined_negatives, combined_entities))

def p_expresion_simple_swaping_two(p):
    'expression : ENTITY SWAP QUALIFICATOR'
    global regex
    if p[3] == "+":
         regex = re.compile("%s(\s\S+){0,3}\s%s(\s\S+){0,3}\s(\w+\.\w(\%s)(\d+.\d+)+)" % (combined_entities, combined_inverters, combined_positives))
    else:
         regex = re.compile("%s(\s\S+){0,3}\s%s(\s\S+){0,3}\s(\w+\.\w(\%s)(\d+.\d+)+)" % (combined_entities, combined_inverters, combined_negatives))
    # print(regex.pattern)

def p_expresion_adhoc_one(p):
    'expression : ENTITY IDENTIFICATOR'
    global regex
    regex = re.compile("%s(\s\S+){0,3}\s(%s)" % (combined_entities, p[2]))

def p_expresion_adhoc_two(p):
    'expression : IDENTIFICATOR ENTITY'
    global regex
    regex = re.compile("(%s)(\s\S+){0,3}\s%s" % (p[1], combined_entities))



# Error rule for syntax errors
def p_error(p):
    print ">>> %s" % p
    print "Syntax error in input!"
    sys.exit(0)

def load_dict(file_path):
    """
    Load files from disk into variables
    """
    aux = []
    f_in = open(file_path, "r")
    tsv_reader = csv.reader(f_in, delimiter='\t')
    for row in tsv_reader:
        aux.append(row[0])
    return aux



# Check if parameters are valid
try:
    opts, args = getopt.getopt(sys.argv[1:], "l:p:", ["language=","port="])
    assert(len(opts) == 2)
except:
    print 'sentiment_Service.py -l <language> -p <port>'
    sys.exit()


for o, a in opts:
    if o == "-l":
        language = a
        if language not in ["spanish", "english"]:
            print 'Valid languages: spanish, english'
            sys.exit()
    elif o == "-p":
        port = a
    else:
        pass



# Load dicts into global variables
print("Loading Negative and positive constants:")
positive = load_dict("dict/positive.tsv")
assert(len(positive) == 1)
combined_positives = positive[0]
negative = load_dict("dict/negative.tsv")
combined_negatives = negative[0]
assert(len(negative) == 1)
print("...loaded.")
print("\n")


print("Loading dicts:")

entities = load_dict("dict/entities.tsv")
combined_entities = "(%s)" % "|".join(entities)
print("\t%s entities terms loaded" % len(entities))

inverters = load_dict("dict/inverters.tsv")
combined_inverters = "(%s)" % "|".join(inverters)
print("\t%s inverters terms loaded" % len(inverters))

chunks = load_dict("dict/chunks.tsv")
print("\t%s chunks loaded" % len(chunks))

stopwords = load_dict("data/stopwords.tsv")
print("\t%s stopwords loaded" % len(stopwords))

# Read the rules from the file
rules = []
for line in open("dict/rules.tsv", "r"):
        line = line.replace("\n", "")
        line = line.replace("\r", "")
        rules.append(line)

# Build the parser, and parse rules
parser = yacc.yacc()
print ("\nLoading rules:")
for rule in rules:
    result = parser.parse(rule)
    print("\tRule parsed succesfully: %s" % rule)


tt = TreeTagger(encoding='latin-1', language=language)
sentiwordnet = SentiWordnet()
to_wordnet = TreetaggerToWordnet()

# Init Tornado web server
application = tornado.web.Application([
    (r"/", MainHandler, dict(rules = compiled_rules, to_wordnet = to_wordnet, sentiwordnet = sentiwordnet, tt = tt, stopwords = stopwords, chunks = chunks, language = language)),
])

# Listen on specific port and start server
application.listen(port)
tornado.ioloop.IOLoop.instance().start()