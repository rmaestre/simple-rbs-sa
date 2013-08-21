import ply.yacc as yacc
from sa_lex import tokens
import sys
import re

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
        regex = ("%s(?:\W+\w+){0,2}?\W+%s" % (combined_positives, combined_entities))
    else:
        regex = ("%s(?:\W+\w+){0,2}?\W+%s" % (combined_negatives, combined_entities))

def p_expresion_simple_two(p):
    'expression : ENTITY QUALIFICATOR'
    global regex
    if p[2] == "+":
        regex = ("%s(?:\W+\w+){0,2}?\W+%s" % (combined_entities, combined_positives))
    else:
        regex = ("%s(?:\W+\w+){0,2}?\W+%s" % (combined_entities, combined_negatives))

def p_expresion_simple_swaping_one(p):
    'expression : SWAP QUALIFICATOR ENTITY'
    global regex
    if p[2] == "+":
         regex = ("%s(?:\W+\w+){0,2}?\W+%s" % (combined_negatives,combined_entities))
    else:
         regex = ("%s(?:\W+\w+){0,2}?\W+%s" % (combined_positives, combined_entities))

def p_expresion_simple_swaping_two(p):
    'expression : ENTITY SWAP QUALIFICATOR'
    global regex
    if p[3] == "+":
         regex = ("%s(?:\W+\w+){0,2}?\W+(no)(?:\W+\w+){0,2}?\W+%s" % (combined_entities, combined_positives))
    else:
         regex = ("%s(?:\W+\w+){0,2}?\W+(no)(?:\W+\w+){0,2}?\W+%s" % (combined_entities, combined_negatives))

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
parser = yacc.yacc(write_tables=0, debug=False)
print ("\nLoading RULES:")
for rule in rules:
    result = parser.parse(rule)
    print("\tRule parsed succesfully: %s" % rule) 

# Sample test
raw = """movistar no funciona muy bien pero nada bien, pero vodafone es muy buena. orange no es muy buena.
algunas veces vodafone no me gusta nada, por otro lado, otras veces vodafone si me gusta"""
raw = raw.replace("\n", "")


# Split input text
chunks = re.split(r'[,;.]+',raw)
print("\nAnalizing %s chunks" % len(chunks))
for chunk in chunks:
    print("\tChunk \"%s\"" % chunk)
    # Appling all rules over the text
    for rule in compiled_rules:
        match = re.findall(compiled_rules[rule]["regex"], chunk)
        if len(match) > 0:
            print("\tRule triggered:%s" % rule)
            print("\tScore: %s" % compiled_rules[rule]["score"])
            print("\tMatch: %s" % match)
            break
    print("\n")


