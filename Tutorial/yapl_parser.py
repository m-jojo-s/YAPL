import ply.yacc as yacc
from yapl_lexer import *

#sys.tracebacklimit = 0 # to prevent traceback debug output since it is not needed

# to resolve ambiguity, individual tokens assigned a precedence level and associativity. 
# tokens ordered from lowest to highest precedence, rightmost terminal judged
precedence = (
    ('left', 'PLUS', 'MINUS'), # +, - same precedence, left associative
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


def p_print_stmt(p):
    """
    stmt : PRINT exp SEMICOL
    """
    p[0] = ('PRINT', p[2])


def p_exp_bin(p):
    """ 
    exp : exp PLUS exp
        | exp MINUS exp
    """
    p[0] = (p[2], p[1], p[3]) # '1+2' -> ('+', '1', '2')


def p_exp_num(p):
    """
    exp : INT
    """
    p[0] = ('NUM', p[1])


def p_error(p):
    print("Syntax error at token", p.value, p.type, p.lexpos)
    exit(1)

parser = yacc.yacc() # start parsing, yacc object created