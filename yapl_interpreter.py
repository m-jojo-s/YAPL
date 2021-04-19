from yapl_lexer import *
from yapl_parser import *
from copy import deepcopy
import sys

FUNC_STACC = [[{}]]

def init_stacc():
    global FUNC_STACC
    # variables and scope management
    FUNC_STACC = [[{}]] # 0 index handles global scope. new var_stacc added for each new function

# Returns scope index if variable exists, -1 if it is global -2 otherwise
def var_exists(var_name) -> int:
    var_stacc = FUNC_STACC[-1]
    curr_scope = len(var_stacc) - 1
    while curr_scope >= 0:
        var_dict = var_stacc[curr_scope]
        if var_name in var_dict :
            return curr_scope
        curr_scope -= 1
    # check global scope
    var_stacc = FUNC_STACC[0]
    curr_scope = 0
    if var_name in var_stacc[curr_scope]:
        return -1
    return -2

def var_create(var_name, var_type) -> bool:
    var_stacc = FUNC_STACC[-1]
    curr_scope = var_exists(var_name)
    if curr_scope >= len(var_stacc) - 1:
        raise ValueError("ValueError: " + var_name + " already exists")
        return False
    new_var = [var_type, None]
    var_dict = var_stacc[-1]
    var_dict[var_name] = new_var
    return True

# check if var_name exists and return value
def var_access(var_name):
    var_stacc = FUNC_STACC[-1]
    curr_scope = var_exists(var_name)
    if curr_scope < -1:
            raise LookupError("LookupError: variable name " + str(var_name) + " not found. Did you declare it?")
            return None
    # If variable exists in global space
    if curr_scope == -1:
        var_stacc = FUNC_STACC[0]
        curr_scope = 0
    var_dict = var_stacc[curr_scope]
    return var_dict[var_name]

# updates variable if variable exists otherwise returns false
# variables are stored as tuples (type, value) in latest scope dictionary
def var_update(var_name, var_val) -> bool:
    var_dict = {}
    if type(var_name) != type(str("temp_string")):
    # To update dictionary (struct)
        ignore = ["ACCESS", "(", ")", "'", '"', ",", "."]
        for word in ignore:
            var_name = str(var_name).replace(word, " ")
        temp = var_name.split(" ")
        properties = [word for word in temp if word != ""]
        var_name = properties[-1]
        var_dict = var_access(properties[0])[1]
        for prpty in properties[1:-1]:
            var_dict = var_dict[prpty]
    else:
        curr_scope = var_exists(var_name)
        if curr_scope < 0:
            return False
        var_stacc = FUNC_STACC[-1]
        var_dict = var_stacc[curr_scope]
    
    # cast value to required type (float to int etc)
    required_type = var_dict[var_name][0]
    type_groups = {
        str(type(1.2)) : "NUM",
        str(type(1)) : "NUM",
        str(type(True)) : "NUM",
        str(type("str")) : "STR",
    }
    num_only = ["int", "float", "bool"]
    if required_type in num_only and type_groups[str(type(var_val))] != "NUM":
        raise TypeError("TypeError: Unable to cast " + str(type(var_val)) + " to " + required_type)
        return False
    if required_type == "int": var_val = int(var_val)
    elif required_type == "float": var_val = float(var_val)
    elif required_type == "bool": var_val = bool(var_val != 0)
    elif required_type == "string": var_val = str(var_val)
    elif required_type == "char":
        var_val = str(var_val)
        var_val = var_val[0]
    
    var_dict[var_name] = [required_type, var_val]
    return True

# change nested lists to 1D
def flatten(ls):
    if type(ls) != type(["temp_list"]):
        return [ls]
    list_1D = []
    for item in ls:
        list_1D += flatten(item)
    return list_1D
        

# returns (value_type, result)
def exp_eval(p): # evaluate expression
    operator = p[0]
    operators = ['+', '-', '*', '/', '^', '%', '++', '--', '>', '<', '>=', '<=', '==', '!=', 'ya', 'aur', 'nahi']
    num_only_operators = ['-', '*', '/', '^', '%', '++', '--']
    type_groups = {
        "int": "NUM",
        "float": "NUM",
        "bool": "NUM",
        "string": "STR",
        "char": "STR",
        "NUM": "NUM",
        "BOOL": "NUM",
        "STR": "STR",
    }
    res1 = 0
    res2 = 0
    group = ""
    if operator in operators:
        res1 = exp_eval(p[1])
        res2 = exp_eval(p[2])
        if res1[0] != res2[0] and type_groups[res1[0]] != type_groups[res2[0]]:
            raise TypeError("TypeError: Invalid operand type(s) for operator " + operator + ": " + res1[0] + " " + res2[0])
            return None
        group = type_groups[res1[0]]
        if group != "NUM" and operator in num_only_operators:
            raise TypeError("TypeError: Invalid operand type(s) for operator " + operator + ": " + res1[0] + " " + res2[0])
            return None
    if operator == '+':
        return (res1[0], res1[1] + res2[1])
    elif operator == '-':
        return (res1[0], res1[1] - res2[1])
    elif operator == '*':
        return (res1[0], res1[1] * res2[1])
    elif operator == '/':
        return (res1[0], res1[1] / res2[1])
    elif operator == '^':
        return (res1[0], res1[1] ** res2[1])
    elif operator == '%':
        valid_types = [bool, int]
        if type(res1[1]) not in valid_types or type(res2[1]) not in valid_types:
            raise TypeError("TypeError: Invalid operand type(s) for operator " + operator + ": " + str(type(res1[1])) + " " + str(type(res2[1])))
            return None
        return (res1[0], int(res1[1]) % int(res2[1]))
    elif operator == ">":
        return (res1[0], res1[1] > res2[1])
    elif operator == "<":
        return (res1[0], res1[1] < res2[1])
    elif operator == ">=":
        return (res1[0], res1[1] >= res2[1])
    elif operator == "<=":
        return (res1[0], res1[1] <= res2[1])
    elif operator == "==":
        return (res1[0], res1[1] == res2[1])
    elif operator == "!=":
        return (res1[0], res1[1] != res2[1])
    elif operator == "ya":
        return (res1[0], res1[1] or res2[1])
    elif operator == "aur":
        return (res1[0], res1[1] and res2[1])
    elif operator == 'nahi':
        return (res1[0], not res1[1])
    elif operator == ",":
        flat = []
        for item in p[1:]:
            res = exp_eval(item)
            flat += res
        return flat
    elif operator == "ASSIGN":
        var_name = p[1]
        exp = p[2]
        result = exp_eval(exp)
        var_update(var_name, result[1])
        return result
    elif operator == "ACCESS":
        return var_access(p[1])
    elif operator == ".":
        var = exp_eval(p[1])
        prpty = p[2]
        if var[0] in type_groups: # if in pre-defined types group, it is not a struct
            raise TypeError("TypeError: Invalid operand type(s) for operator " + operator + ": " + var[0])
            return None
        instance = var[1]
        result = instance.get(str(prpty))
        if result == None:
            raise LookupError("LookupError: Could not access property " + prpty + " of struct type " + str(var[0]))
        return result
    else: # operator was a single value
        return p

def stmt_eval(p): # p is the parsed statement subtree / program
    stype = p[0] # node type of parse tree
    if stype == 'PRINT':
        args = p[1]
        result = exp_eval(args)
        if type(result) != type(["temp_list"]) or len(result) == 2:
            print(result[1])
            return
        to_print = ""
        for item in result[1:-1:2]:
            to_print += str(item) + " "
        to_print += str(result[-1])
        print(to_print)
                
    elif stype == "DECLARE":
        dtype = p[1]
        var_name = p[2]
        var_create(var_name, dtype)
    elif stype == "ASSIGN":
        exp_eval(p)
    elif stype == "DEC_ASS":
        stmt_eval(p[1])
        stmt_eval(p[2])
    elif stype == "DEC_CHAIN":
        for stmt in p[1:]:
            stmt_eval(stmt)
    elif stype == "EXP":
        exp_eval(p[1])
    elif stype == "IF":
        cond = bool(exp_eval(p[1])[1])
        if cond == True:
            stmt_eval(p[2])
        else:
            stmt_eval(p[3])
    elif stype == "STMT_BLK":
        # add new scope dict in curr function's stack
        var_stacc = FUNC_STACC[-1]
        var_stacc.append({})
        # evaluate statements
        for stmt in p[1]:
            stmt_eval(stmt)
        # remove added scope
        var_stacc.pop()
    elif stype == "FOR":
        # FOR stmt exp exp stmt_blk
        start = p[1]
        cond = p[2]
        inc = p[3]
        blk = p[4]
        # add new scope dict in curr function's stack
        var_stacc = FUNC_STACC[-1]
        var_stacc.append({})
        stmt_eval(start)
        while bool(exp_eval(cond)[1]):
            stmt_eval(blk)
            stmt_eval(inc)
        # remove added scope
        var_stacc.pop()
    elif stype == "STRUCT":
        var_name = p[1]
        dec_chain = p[2]
        # temporarily add a new dict in scope so all dec-stmts go there
        var_stacc = FUNC_STACC[-1]
        var_stacc.append({})
        # evaluate dec-chain and pop dict to make struct
        stmt_eval(dec_chain)
        data_struct = var_stacc.pop()
        struct_var = ["struct", data_struct]
        # add to global scope
        FUNC_STACC[0][0][var_name] = struct_var
    elif stype == "DEC_STRUCT":
        struct_name = p[1]
        instance_name = p[2]
        struct_type = var_access(struct_name) # Should raise lookup error if not existent
        if struct_type == None:
            return
        # make sure another variable with same name hasn't been defined before
        var_stacc = FUNC_STACC[-1]
        curr_scope = var_exists(instance_name)
        if curr_scope >= len(var_stacc) - 1:
            raise ValueError("ValueError: " + instance_name + " already exists")
            return
        new_var = [struct_name, deepcopy(struct_type[1])]
        var_dict = var_stacc[-1]
        var_dict[instance_name] = new_var
        
def run_program(p): # p[0] == 'Program': a bunch of statements
    for stmt in p: # statements in proglist
        if stmt != None:
            stmt_eval(stmt) # statement subtree as tuple
        

if len(sys.argv) == 1:
    print('File name/path not provided as cmd arg.')
    exit(1)

while True:
    init_stacc()
    fileHandler = open(sys.argv[1],"r")
    userin = fileHandler.read()
    fileHandler.close()

    print("Welcome to your YAPL's Interpreter!")
    parsed = parser.parse(userin)
    if not parsed:
        continue
    
    for line in userin.split('\n'):
        print(line)
    print("=========================================\n{OUTPUT}")
    try:
        run_program(parsed)
    except Exception as e:
        print(e)
    
    input("Press any key to run code again.")


exit()