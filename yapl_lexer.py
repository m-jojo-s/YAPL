import ply.lex as lex
import re

# TOKEN IDENTIFIERS, have to match name of our token

# list of all possible tokens
tokens = [
    # DATA TYPES
    "INT",
    "FLOAT",
    "STRING",
    "CHAR",
    "BOOL",
    # OPERATORS
    "ASSIGNMENT",
    "PLUS",
    "MINUS",
    "ASTERISK",
    "FWSLASH",
    "TOPI",
    "MOD",
    "PLUS_PLUS",
    "MINUS_MINUS",
    "LESSER",
    "GREATER",
    "GREATER_EQUAL",
    "LESSER_EQUAL",
    "IS_EQUAL",
    "NOT_EQUAL",
    "NOT",
    "LOGICAL", # AND, OR
    # DELIMITERS
    "COMMA",
    "SEMICOL",
    # NAMES
    "PRINT",
    "VAR_NAME",
    "DATA_TYPE",
    "FOR",
    "IF",
    "ELSE",
    # BRACKETS
    "L_ROUND",
    "R_ROUND",
    "L_CURLY",
    "R_CURLY",
    "L_SQR",
    "R_SQR"
]

t_ASSIGNMENT = r'\='
t_PLUS = r'\+'
t_MINUS = r'\-'
t_ASTERISK = r'\*'
t_FWSLASH = r'\/'
t_TOPI = r'\^'
t_MOD = r'\%'
t_PLUS_PLUS = r'\+\+'
t_MINUS_MINUS = r'\-\-'
t_LESSER = r'\<'
t_GREATER = r'\>'
t_LESSER_EQUAL = r'\<\='
t_GREATER_EQUAL = r'\>\='
t_IS_EQUAL = r'\=\='
t_NOT_EQUAL = r'\!\='
t_SEMICOL = r'\;'
t_COMMA = r'\,'
t_L_ROUND = r'\('
t_R_ROUND = r'\)'
t_L_CURLY = r'\{'
t_R_CURLY = r'\}'
t_L_SQR = r'\['
t_R_SQR = r'\]'
    
t_ignore = ' \t\r\n\f\v'

def t_FLOAT(t):
    r'([0-9]*\.?[0-9]+f)|([0-9]*\.[0-9]+f?)'
    if t.value[-1] == 'f': t.value = t.value[:-1]
    t.value = float(t.value)
    return t

def t_INT(t): # parameter t is the token
    r'\d+' # atleast one digit
    t.value = int(t.value) # convert to int
    return t


def t_STRING(t):
    r'"[^"]+"'
    t.value = str(t.value[1:-1])
    return t

def t_CHAR(t):
    r"'.'"
    t.value = str(t.value[1:-1])
    return t

def t_BOOL(t):
    r'sach|jhoot'
    t.value = t.value == "sach"
    return t

def t_LOGICAL(t):
    r"ya|aur"
    return t

def t_NOT(t):
    r"nahi"
    return t

# variable or function names (including predefined functions like print)
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    types = ["int", "float", "string", "char", "bool"]
    if t.value in types:
        t.type = "DATA_TYPE"
    elif t.value == 'print':
        t.type = 'PRINT'
    elif t.value == 'for':
        t.type = "FOR"
    elif t.value == "agar":
        t.type = "IF"
    elif t.value == "warna":
        t.type = "ELSE"
    else:
        t.type = 'VAR_NAME'
        
    return t

def t_lineno(t):
    r'\n'
    t.lexer.lineno += len(t.value) 


def t_error(t): # error while lexing
    print("[Lexer Error] Line",t.lineno)
    print(f"Illegal character: {t.value}")
    t.lexer.skip(1) # skips illegal character

# create lexer
lexer = lex.lex()

# ENABLE THIS TO TEST YOUR LEXER DIRECTLY
# while True:
#     print("YAPL_LEXER>>",end='')
#     lexer.input(input()) # reset lexer, store new input
        
#     while True: # necessary to lex all tokens
#         tokenEntered = lexer.token() # return next token from lexer
#         if not tokenEntered: # lexer error also given
#             break
#         print(tokenEntered)