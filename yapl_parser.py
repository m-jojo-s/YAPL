import ply.yacc as yacc
from yapl_lexer import *

#sys.tracebacklimit = 0 # to prevent traceback debug output since it is not needed

# to resolve ambiguity, individual tokens assigned a precedence level and associativity. 
# tokens ordered from lowest to highest precedence, rightmost terminal judged
precedence = (
    ('nonassoc', 'LESSER', 'GREATER', "LESSER_EQUAL", "GREATER_EQUAL", "IS_EQUAL", "NOT_EQUAL"),
    ('left', 'PLUS', 'MINUS'), # +, - same precedence, left associative
    ("left", "FWSLASH", "ASTERISK"),
    ("left", "MOD", "TOPI"),
    ("left", "L_ROUND", "R_ROUND"),
    ("left", "L_CURLY", "R_CURLY"),
    ("left", "L_SQR", "R_SQR")
)

start = 'S'
# multiple variables, assigning data from one variable to another

# after the lexing, start parsing

def p_start(p): # non-terminal, starting
    """
    S : stmt S
    """
    p[0] = [p[1]] + p[2] # list comprehension used to solve recursive grammar, added/appending as well
    

def p_start_empty(p):
    """
    S :
    """
    p[0] = []
    

def p_stmt_exp(p):
    """
    stmt : exp SEMICOL
        | SEMICOL
        | L_ROUND R_ROUND
        | L_CURLY R_CURLY
        | L_SQR R_SQR
    """
    p[0] = ("EXP", p[1])

def p_stmt_blk(p):
    """
    stmt_blk : L_CURLY S R_CURLY
    """
    p[0] = ("STMT_BLK", p[2])


def p_print_stmt(p):
    """
    stmt : PRINT L_ROUND args R_ROUND SEMICOL
    """
    p[0] = ('PRINT', p[3])


def p_args_exp(p):
    """
    args : exp
        | args COMMA args
    """
    p[0] = (p[1])
    if len(p) > 2:
        p[0] = (",", p[1], p[3])

def p_if_stmt(p):
    """
    stmt : if
    """
    p[0] = p[1]

def p_if(p):
    """
    if : IF L_ROUND exp R_ROUND stmt_blk else 
    """
    p[0] = ("IF", p[3], p[5], p[6])

def p_else(p):
    """
    else : ELSE stmt_blk
        | ELSE if
        |
    """
    if(len(p) > 2):
        p[0] = (p[2])

def p_for_stmt(p):
    """
    stmt : FOR L_ROUND stmt exp SEMICOL stmt R_ROUND stmt_blk
    """
    p[0] = ("FOR", p[3], p[4], p[6], p[8])
        
def p_dec_stmt(p):
    """
    stmt : DATA_TYPE VAR_NAME SEMICOL
        | DATA_TYPE VAR_NAME ASSIGNMENT exp SEMICOL
    """
    if(len(p) == 4):
        p[0] = ("DECLARE", p[1], p[2])
    elif(len(p) == 6):
        p[0] = ("DEC_ASS", ("DECLARE", p[1], p[2]), ("ASSIGN", p[2], p[4]) )
    
def p_assign_stmt(p):
    """
    stmt : VAR_NAME ASSIGNMENT exp SEMICOL
    """
    p[0] = ("ASSIGN", p[1], p[3])

def p_exp_brackets(p):
    """
    exp : L_ROUND exp R_ROUND
        | L_CURLY exp R_CURLY
        | L_SQR exp R_SQR
    """
    p[0] = (p[2])

def p_exp_bin(p):
    """ 
    exp : exp PLUS exp
        | exp MINUS exp
        | exp ASTERISK exp
        | exp FWSLASH exp
        | exp TOPI exp
        | exp MOD exp
        | exp LESSER exp
        | exp GREATER exp
        | exp LESSER_EQUAL exp
        | exp GREATER_EQUAL exp
        | exp IS_EQUAL exp
        | exp NOT_EQUAL exp
        | exp LOGICAL exp
    """
    p[0] = (p[2], p[1], p[3])

def p_exp_neg(p):
    """
    exp : MINUS exp
    """
    p[0] = (p[1], ('NUM', 0), p[2])

def p_exp_not(p):
    """
    exp : NOT exp
    """
    p[0] = (p[1], p[2], p[2])

def p_exp_uni(p):
    """
    exp : VAR_NAME PLUS_PLUS
        | VAR_NAME MINUS_MINUS
    """
    p[0] = ("ASSIGN", p[1], (p[2][0], ("ACCESS", p[1]), ("NUM", 1)))
    
def p_exp_var(p):
    """
    exp : VAR_NAME
    """
    p[0] = ("ACCESS", p[1])

def p_exp_num(p):
    """
    exp : INT
        | FLOAT
    """
    p[0] = ('NUM', p[1])

def p_exp_str(p):
    """
    exp : STRING
        | CHAR
    """
    p[0] = ("STR", p[1])

def p_exp_bool(p):
    """
    exp : BOOL
    """
    p[0] = ("BOOL", p[1])

def p_error(p):
    print("Syntax error at token", p.value, p.type, p.lexpos)
    exit(1)

parser = yacc.yacc() # start parsing, yacc object created