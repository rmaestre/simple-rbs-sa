import tornado.ioloop
import tornado.web
import sys
import time
import ply.yacc as yacc
from sa_lex import tokens
import re


class MainHandler(tornado.web.RequestHandler):
    """ """
    
    def initialize(self, rules):
        """ """
        self.rules = rules

    def get(self):
        """ """
        # Start operation time
        time_start = time.time()
        # Prepare the response DS
        response = {}
        # Check input text
        text = self.get_argument("text")
        text = text.replace("\n", "")

        # Split input text
        chunks = re.split(r'[,;.]+',text)
        triggered_rule_cont = 0
        for chunk in chunks:
            # Appling all rules over the text
            for rule in compiled_rules:
                match_triggered = False
                for match in compiled_rules[rule]["regex"].finditer(chunk):
                    match_triggered = True
                    response[triggered_rule_cont] = {}
                    response[triggered_rule_cont]["rule_triggered"] = rule
                    response[triggered_rule_cont]["score"] = compiled_rules[rule]["score"]
                    response[triggered_rule_cont]["match"] = match.group()
                    response[triggered_rule_cont]["start"] = match.start()
                    triggered_rule_cont += 1
                    break
                if match_triggered:
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
        regex = re.compile("%s(?:\W+\w+){0,2}?\W+%s" % (combined_positives, combined_entities))
    else:
        regex = re.compile("%s(?:\W+\w+){0,2}?\W+%s" % (combined_negatives, combined_entities))

def p_expresion_simple_two(p):
    'expression : ENTITY QUALIFICATOR'
    global regex
    if p[2] == "+":
        regex = re.compile("%s(?:\W+\w+){0,2}?\W+%s" % (combined_entities, combined_positives))
    else:
        regex = re.compile("%s(?:\W+\w+){0,2}?\W+%s" % (combined_entities, combined_negatives))

def p_expresion_simple_swaping_one(p):
    'expression : SWAP QUALIFICATOR ENTITY'
    global regex
    if p[2] == "+":
         regex = re.compile("%s(?:\W+\w+){0,2}?\W+%s" % (combined_negatives,combined_entities))
    else:
         regex = re.compile("%s(?:\W+\w+){0,2}?\W+%s" % (combined_positives, combined_entities))

def p_expresion_simple_swaping_two(p):
    'expression : ENTITY SWAP QUALIFICATOR'
    global regex
    if p[3] == "+":
         regex = re.compile("%s(?:\W+\w+){0,2}?\W+(no)(?:\W+\w+){0,2}?\W+%s" % (combined_entities, combined_positives))
    else:
         regex = re.compile("%s(?:\W+\w+){0,2}?\W+(no)(?:\W+\w+){0,2}?\W+%s" % (combined_entities, combined_negatives))

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





# Check if server por is valid
port = -1
if len(sys.argv) == 2:
    port = int(sys.argv[1])
else:
    print("Port hould be specified")
    sys.exit()

# Init Tornado web server
application = tornado.web.Application([
    (r"/", MainHandler, dict(rules = compiled_rules)),
])

# Listen on specific port and start server
application.listen(8080)
tornado.ioloop.IOLoop.instance().start()