# encoding: utf-8

import tornado.ioloop
import tornado.web
import sys
import time
import ply.yacc as yacc
from sa_lex import tokens
import re
from treetagger import TreeTagger
from treetagger_wordnet import TreetaggerToWordnet


class MainHandler(tornado.web.RequestHandler):
    """ """
    
    def initialize(self, rules, chunks):
        """ """
        self.rules = rules
        self.chunks = chunks
        self.tt = TreeTagger(encoding='latin-1', language='spanish')
        self.to_wordnet = TreetaggerToWordnet()

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
        # Perform PosTaggin onto the text
        aux = ""

        # Replace chunks symbols
        for chunk in self.chunks:
            text = text.replace(chunk, " # ")

        # Mapping treetagger postaging to wordnet postagging
        for tag in self.tt.tag(text):
            lemma = tag[2]
            if lemma == u"<unknown>":
                lemma = tag[0]
            aux += "%s.%s " % (lemma, self.to_wordnet.wordnet_morph_category('es', tag[1]))
        text = aux

        # Replace postagging for the entities
        aux = ""
        chunks = text.split(" ")
        for chunk in chunks:
            sub_chunks = chunk.split(".")
            if sub_chunks[0] in entities or sub_chunks[0]  in swaps:
                aux += "%s " % sub_chunks[0]
            else:
                aux += "%s " % chunk
        text = aux
        response["text"] = text


        # Split input text
        chunks = text.split('#.None')
        triggered_rule_cont = 0
        response["matches"] = {}

        for chunk in chunks:
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

def p_rule(p):
    'rule : BEGINRULE expression THEN SCORE ENDRULE'
    if p[1] in compiled_rules:
        print("Error: Rule #ID duplicated.")
        sys.exit(0)
    compiled_rules[p[1]] = {}
    compiled_rules[p[1]]["regex"] = regex
    compiled_rules[p[1]]["score"] = float(p[4])

def p_expresion_simple_one(p):
    'expression : QUALIFICATOR ENTITY'
    global regex
    if p[1] == "+":
        regex = re.compile("%s(?:\W+\w+){0,4}?\W+%s" % (combined_positives, combined_entities))
    else:
        regex = re.compile("%s(?:\W+\w+){0,4}?\W+%s" % (combined_negatives, combined_entities))

def p_expresion_simple_two(p):
    'expression : ENTITY QUALIFICATOR'
    global regex
    if p[2] == "+":
        regex = re.compile("%s(?:\W+\w+){0,4}?\W+%s" % (combined_entities, combined_positives))
    else:
        regex = re.compile("%s(?:\W+\w+){0,4}?\W+%s" % (combined_entities, combined_negatives))

def p_expresion_simple_swaping_one(p):
    'expression : SWAP QUALIFICATOR ENTITY'
    global regex
    if p[2] == "+":
         regex = re.compile("%s(?:\W+\w+){0,3}?\W+%s(?:\W+\w+){0,3}?\W+%s" % (combined_swaps, combined_positives, combined_entities))
    else:
         regex = re.compile("%s(?:\W+\w+){0,3}?\W+%s(?:\W+\w+){0,3}?\W+%s" % (combined_swaps, combined_negatives, combined_entities))

def p_expresion_simple_swaping_two(p):
    'expression : ENTITY SWAP QUALIFICATOR'
    global regex
    if p[3] == "+":
         regex = re.compile("%s(?:\W+\w+){0,3}?\W+%s(?:\W+\w+){0,3}?\W+%s" % (combined_entities, combined_swaps, combined_positives))
    else:
         regex = re.compile("%s(?:\W+\w+){0,3}?\W+%s(?:\W+\w+){0,3}?\W+%s" % (combined_entities, combined_swaps, combined_negatives))

# Error rule for syntax errors
def p_error(p):
    print ">>> %s" % p
    print "Syntax error in input!"
    sys.exit(0)

def load_dict(file):
    """
    Load files from disk into variables
    """
    aux = []
    for line in open(file, "r"):
        line = line.replace("\n", "")
        aux.append(line)
    return aux



# Check if server por is valid
port = -1
if len(sys.argv) == 2:
    port = int(sys.argv[1])
else:
    print("Port hould be specified")
    sys.exit()



# Load dicts into global variables
print("Loading dicts:")
positives = load_dict("dict/positives.tsv")
combined_positives = "(%s)" % "|".join(positives)
print("\t%s positives terms loaded" % len(positives))

negatives = load_dict("dict/negatives.tsv")
combined_negatives = "(%s)" % "|".join(negatives)
print("\t%s negatives terms loaded" % len(negatives))

entities = load_dict("dict/entities.tsv")
combined_entities = "(%s)" % "|".join(entities)
print("\t%s entities terms loaded" % len(entities))

swaps = load_dict("dict/swaps.tsv")
combined_swaps = "(%s)" % "|".join(swaps)
print("\t%s swaps terms loaded" % len(combined_swaps))

chunks = load_dict("dict/chunks.tsv")
print("\t%s chunks loaded" % len(chunks))

# Read the rules from the file
rules = []
for line in open("dict/rules.tsv", "r"):
        line = line.replace("\n", "")
        rules.append(line)

# Build the parser, and parse rules
parser = yacc.yacc()
print ("\nLoading RULES:")
for rule in rules:
    result = parser.parse(rule)
    print("\tRule parsed succesfully: %s" % rule) 



# Init Tornado web server
application = tornado.web.Application([
    (r"/", MainHandler, dict(rules = compiled_rules, chunks = chunks)),
])

# Listen on specific port and start server
application.listen(8080)
tornado.ioloop.IOLoop.instance().start()