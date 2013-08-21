import ply.lex as lex

# List of token names.   This is always required
tokens = (
    'SPACES',
    'SCORE',
    'QUALIFICATOR',
    'SWAP',
    'ENTITY',
    'MULTIPLIER',
    'THEN',
    'BEGINRULE',
    'ENDRULE'
)

# Regular expression rules for simple tokens
t_THEN   = r'\>'
t_ENTITY = r'ENTITY'
t_QUALIFICATOR = r'\+|\-'
t_ENDRULE = r'\;'
t_BEGINRULE = r'\#\d+'
t_SWAP = r'NOT'

# A regular expression rules with some action code
def t_SPACES(t):
    r'\{\d+\}'
    t.value = int(t.value[1:len(t.value)-1])    
    return t

def t_SCORE(t):
    r'-?\d+\.\d+'
    t.value = t.value  
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\n'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

"""
# Test it out
data = '''
#1 POSITIVE {2} ENTITY > -0.3;
#25 NEGATIVE POSITIVE {3} ENTITY > 0.3;
END
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print tok
"""
