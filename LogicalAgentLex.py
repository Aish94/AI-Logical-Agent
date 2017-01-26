import ply.lex as lex

# List of token names.
tokens = (
   'NOT',
   'OR',
   'AND',
   'IMPLIES',
   'LPAREN',
   'RPAREN',
   'VAR',
   'CONST',
   'COMMA',
)

predicates = []
# Regular expression rules for simple tokens
t_NOT    = r'~'
t_OR   = r'\|'
t_AND   = r'&'
t_IMPLIES  = r'=>'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COMMA = r','
t_VAR = r'([a-z])'
t_CONST = r'([A-Z])([a-zA-Z])*'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def build_lexer():
  # Build the lexer
  lexer = lex.lex()
  return lexer

def lexical_analyzer(data,lexer):
  # Give the lexer some input
  lexer.input(data)
  '''
  #print tokens
  s = ""
  for tok in lexer:
	 s += str(tok) + "\n"
  print(s)'''

