from lexer import tokens, reserved
import ply.yacc as yacc
import datetime
from lexer import brace_stack, lexical_errors

# ----------- Logs -------------
success_log = []
error_log = []
vars_con_error = set()

current_function = None
context_stack = []




def log_info(msg):
    print(f"✔ {msg}")
    success_log.append(f"✔ {msg}")

def log_error(msg):
    print(f"✖ {msg}")
    semantic_errors.append(f"✖ {msg}")


# ----------- First Rule (ROOT) -------------
def p_program(p):
    '''program : program element
               | element'''
    log_info("program")

def p_element(p):
    '''element : letAssignment
               | declaracion
               | function
               | arrow_function
               | async_function
               | constAssignment
               | enum_definition
               | controlEstructure
               | class_definition
               | statement
               | interface
               | assignment
               | expression SEMICOLON
               | consolelog'''
    log_info("element")


def p_assignment(p):
    'assignment : IDENTIFIER EQUAL expression SEMICOLON'
    log_info(f"assignment to {p[1]}")


# ----------- Symbol Table -------------
symbol_table = {
    "consts": {},
    "classes": {},
    "enums": {},
    "functions": {}
}
semantic_errors = []



#----------Compatibilty functions for semantic analysis-------------
def are_types_compatible(declared_type, value_type):
    return declared_type == value_type






#Added by Leonardo Zambrano

# ----------- Declare Variable -------------
def p_letAssignment(p):
    'letAssignment : LET IDENTIFIER COLON type EQUAL expression SEMICOLON'
    var = p[2]
    declared_type = p[4]
    value_type = p[6]
    symbol_table[var] = declared_type
    if not are_types_compatible(declared_type, value_type):
        semantic_errors.append(f"Error semántico: '{var}' declarado como '{declared_type}' pero asignado un '{value_type}'")
        vars_con_error.add(var)
    log_info(f"letAssignment: {p[2]}")


def p_letAssignment_no_type(p):
    'letAssignment : LET IDENTIFIER EQUAL expression SEMICOLON'
    var = p[2]
    value_type = p[4]
    symbol_table[var] = value_type
    log_info(f"letAssignment (no type): {p[2]}")

def p_letAssignment_declaration_only(p):
    'letAssignment : LET IDENTIFIER COLON type SEMICOLON'
    var = p[2]
    declared_type = p[4]
    symbol_table[var] = declared_type
    log_info(f"letAssignment (declaración sin valor): {var}")


# ----------- Array Assignment -------------
def p_declaracion(p):
    '''declaracion : LET IDENTIFIER COLON type LBRACKET RBRACKET EQUAL LBRACKET lista_expresiones_opt RBRACKET SEMICOLON'''
    log_info(f"array declaration: {p[2]}")

def p_lista_expresiones_opt(p):
    '''lista_expresiones_opt : lista_expresiones
                            | empty'''
    log_info("optional expression list")

def p_lista_expresiones(p):
    '''lista_expresiones : expression
                        | expression COMMA lista_expresiones'''
    log_info("expression list")


def p_push_loop(p):
    'push_loop :'
    context_stack.append("loop")

def p_pop_loop(p):
    'pop_loop :'
    context_stack.pop()

def p_push_switch(p):
    'push_switch :'
    context_stack.append("switch")

def p_pop_switch(p):
    'pop_switch :'
    context_stack.pop()

# ----------- For -------------

def p_forEstructure(p):
    '''forEstructure : FOR LPAREN for_init SEMICOLON expression SEMICOLON for_update RPAREN LBRACE push_loop instruction_list pop_loop RBRACE
                   | FOR LPAREN CONST IDENTIFIER OF IDENTIFIER RPAREN push_loop statement pop_loop'''
    # Primera alternativa: p[0] = p[12]
    if len(p) == 13:
        p[0] = p[12]
        log_info("for structure")
    # Segunda alternativa: p[0] = p[9]
    else:
        p[0] = p[9]
        log_info("for...of structure")





def p_for_init(p):
    '''for_init : LET IDENTIFIER EQUAL expression
                | LET IDENTIFIER COLON type EQUAL expression
                | IDENTIFIER EQUAL expression
                | expression
                | empty'''
    if len(p) == 5:
        var = p[2]
        value_type = p[4]
        symbol_table[var] = value_type
        log_info(f"for init (let, sin tipo declarado): {var}")
        p[0] = value_type  # ← NECESARIO
    elif len(p) == 7:
        var = p[2]
        declared_type = p[4]
        value_type = p[6]
        symbol_table[var] = declared_type
        if not are_types_compatible(declared_type, value_type):
            semantic_errors.append(f"Error semántico: '{var}' declarado como '{declared_type}' pero asignado un '{value_type}'")
            vars_con_error.add(var)
        log_info(f"for init (let, con tipo declarado): {var}")
        p[0] = value_type  # ← NECESARIO
    elif len(p) == 4 and isinstance(p[1], str):
        var = p[1]
        value_type = p[3]
        if var in symbol_table:
            log_info(f"for init (uso de variable declarada): {var}")
        else:
            semantic_errors.append(f"✘ Línea {p.lineno(1)}: variable '{var}' no declarada")
        p[0] = value_type
    elif len(p) == 2:
        p[0] = None
    log_info("for init")



def p_for_update(p):
    '''for_update : expression
                  | expression PLUSPLUS
                  | expression MINUSMINUS
                  | PLUSPLUS expression
                  | MINUSMINUS expression
                  | empty'''
    log_info("for update")

# ----------- Function and Parameter-------------
def p_function(p):
    'function : FUNCTION IDENTIFIER LPAREN parameters RPAREN COLON type LBRACE body_function RBRACE'
    global current_function
    func_name = p[2]
    return_type = p[7]
    current_function = func_name
    symbol_table[func_name] = {
        "type": "function",
        "return_type": return_type,
    }
    log_info(f"function declaration: {func_name} retorna {return_type}")
    current_function = None  

def p_statement_return_expr(p):
    'statement : RETURN expression SEMICOLON'
    log_info("return statement con valor")
    if current_function:
        expected = symbol_table[current_function]["return_type"]
        returned = p[2]
        if not are_types_compatible(expected, returned):
            semantic_errors.append(
                f"Error semántico: función '{current_function}' debe retornar '{expected}' pero retorna '{returned}'"
            )


def p_parameters(p):
    '''parameters : IDENTIFIER COLON type
                | IDENTIFIER COLON type COMMA parameters
                | empty'''
    if len(p) == 4:
        var = p[1]
        declared_type = p[3]
        symbol_table[var] = declared_type
        log_info(f"parameter: {var} de tipo {declared_type}")
    elif len(p) > 4:
        var = p[1]
        declared_type = p[3]
        symbol_table[var] = declared_type
        log_info(f"parameter: {var} de tipo {declared_type}")

def p_body_function(p):
    '''body_function : instruction_list
                    | empty'''
    log_info("function body")

# ----------- Tuple-------------
def p_type_tuple(p):
    'type : LBRACKET type COMMA type RBRACKET'
    log_info("tuple type")

def p_expression_tuple(p):
    'expression : LBRACKET expression COMMA expression RBRACKET'
    log_info("tuple value")

# ---------- TYPES -------------
def p_type(p):
    '''type : NUMBER_TYPE
            | STRING_TYPE
            | BOOLEAN_TYPE
            | IDENTIFIER
            | VOID
            | type LBRACKET RBRACKET'''
    log_info("type")
    p[0] = p[1]

# ----------- EXPRESSION AND CONSOLE LOG ---------
# def p_expression(p):
#     '''expression : expression PLUS expression
#                 | expression MINUS expression
#                 | expression TIMES expression
#                 | expression DIV expression
#                 | expression MOD expression
#                 | expression PLUS_ASSIGN expression
#                 | expression MINUS_ASSIGN expression
#                 | expression MULT_ASSIGN expression
#                 | expression DIV_ASSIGN expression
#                 | expression MOD_ASSIGN expression
#                 | expression POT expression
#                 | expression AND expression
#                 | expression OR expression
#                 | expression EQ expression
#                 | expression NEQ expression
#                 | expression STRICT_EQ expression
#                 | expression STRICT_NEQ expression
#                 | expression LT expression
#                 | expression GT expression
#                 | expression LE expression
#                 | expression GE expression
#                 | PROMPT LPAREN STRING RPAREN
#                 | NOT expression
#                 | LPAREN expression RPAREN
#                 | expression DOT IDENTIFIER
#                 | expression LBRACKET expression RBRACKET
#                 | IDENTIFIER LPAREN lista_expresiones_opt RPAREN
#                 | NUMBER
#                 | FLOAT
#                 | STRING
#                 | IDENTIFIER
#                 | TRUE
#                 | FALSE'''
#     log_info("expression")

def p_expression_plus(p):
    'expression : expression PLUS expression'
    left_type = p[1]
    right_type = p[3]
    # Plus between two expressions number and string
    if left_type == 'number' and right_type == 'number':
        p[0] = 'number'
    elif left_type == 'string' or right_type == 'string':
        # Allow string + string, string + number, number + string
        if left_type in ('string', 'number') and right_type in ('string', 'number'):
            p[0] = 'string'
        else:
            p[0] = 'undefined'
            semantic_errors.append(
                f"Error semántico: no se puede sumar '{left_type}' y '{right_type}' (línea {p.lineno(2)})"
            )
    else:
        p[0] = 'undefined'
        semantic_errors.append(
            f"Error semántico: no se puede sumar '{left_type}' y '{right_type}' (línea {p.lineno(2)})"
        )
    log_info("expression")


def p_expression_minus(p):
    'expression : expression MINUS expression'
    left_type = p[1]
    right_type = p[3]
    if left_type == 'number' and right_type == 'number':
        p[0] = 'number'
    else:
        p[0] = 'undefined'
        semantic_errors.append(
            f"Error semántico: no se puede restar '{left_type}' y '{right_type}' (línea {p.lineno(2)})"
        )
    log_info("expression")

def p_expression_times(p):
    'expression : expression TIMES expression'
    left_type = p[1]
    right_type = p[3]
    if left_type == 'number' and right_type == 'number':
        p[0] = 'number'
    else:
        p[0] = 'undefined'
        semantic_errors.append(
            f"Error semántico: no se puede multiplicar '{left_type}' y '{right_type}' (línea {p.lineno(2)})"
        )
    log_info("expression")

def p_expression_div(p):
    'expression : expression DIV expression'
    left_type = p[1]
    right_type = p[3]
    if left_type == 'number' and right_type == 'number':
        p[0] = 'number'
    else:
        p[0] = 'undefined'
        semantic_errors.append(
            f"Error semántico: sólo se pueden dividir números, no '{left_type}' y '{right_type}' (línea {p.lineno(2)})"
        )
    log_info("expression")


def p_expression_mod(p):
    'expression : expression MOD expression'
    left_type = p[1]
    right_type = p[3]
    if left_type == 'number' and right_type == 'number':
        p[0] = 'number'
    else:
        p[0] = 'undefined'
        semantic_errors.append(
            f"Error semántico: sólo se pueden calcular restos de números, no '{left_type}' y '{right_type}' (línea {p.lineno(2)})"
        )
    log_info("expression")

def p_expression_plus_assign(p):
    'expression : expression PLUS_ASSIGN expression'
    log_info("expression")

def p_expression_minus_assign(p):
    'expression : expression MINUS_ASSIGN expression'
    log_info("expression")

def p_expression_mult_assign(p):
    'expression : expression MULT_ASSIGN expression'
    log_info("expression")

def p_expression_div_assign(p):
    'expression : expression DIV_ASSIGN expression'
    log_info("expression")

def p_expression_mod_assign(p):
    'expression : expression MOD_ASSIGN expression'
    log_info("expression")

def p_expression_pot(p):
    'expression : expression POT expression'
    log_info("expression")

def p_expression_and(p):
    'expression : expression AND expression'
    log_info("expression")

def p_expression_or(p):
    'expression : expression OR expression'
    log_info("expression")

def p_expression_eq(p):
    'expression : expression EQ expression'
    log_info("expression")

def p_expression_neq(p):
    'expression : expression NEQ expression'
    log_info("expression")

def p_expression_strict_eq(p):
    'expression : expression STRICT_EQ expression'
    log_info("expression")

def p_expression_strict_neq(p):
    'expression : expression STRICT_NEQ expression'
    log_info("expression")

def p_expression_lt(p):
    'expression : expression LT expression'
    log_info("expression")

def p_expression_gt(p):
    'expression : expression GT expression'
    log_info("expression")

def p_expression_le(p):
    'expression : expression LE expression'
    log_info("expression")

def p_expression_ge(p):
    'expression : expression GE expression'
    log_info("expression")

def p_expression_prompt(p):
    'expression : PROMPT LPAREN STRING RPAREN'
    log_info("expression")
    p[0] = 'string'

def p_expression_not(p):
    'expression : NOT expression'
    log_info("expression")

def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    log_info("expression")
    p[0] = p[2]

def p_expression_dot_identifier(p):
    'expression : expression DOT IDENTIFIER'
    log_info("expression")

    # Soportar arreglo.length como tipo number
    if p[3] == "length":
        p[0] = "number"
    else:
        p[0] = "undefined"


def p_expression_bracket(p):
    'expression : expression LBRACKET expression RBRACKET'
    log_info("expression")

def p_expression_call(p):
    'expression : IDENTIFIER LPAREN lista_expresiones_opt RPAREN'
    func_name = p[1]
    if func_name in symbol_table and symbol_table[func_name]["type"] == "function":
        p[0] = symbol_table[func_name]["return_type"]
    else:
        p[0] = "undefined"
        semantic_errors.append(
            f"Error semántico: función '{func_name}' no declarada (línea {p.lineno(1)})"
        )
    log_info(f"llamada a función: {func_name}")

def p_expression_number(p):
    'expression : NUMBER'
    log_info("expression")
    p[0] = 'number'

def p_expression_float(p):
    'expression : FLOAT'
    log_info("expression")
    p[0] = 'number'

def p_expression_string(p):
    'expression : STRING'
    log_info("expression")
    p[0] = 'string'

def p_expression_identifier(p):
    'expression : IDENTIFIER'
    log_info("expression")
    name = p[1]
    if name in symbol_table:
        p[0] = symbol_table[name]
    else:
        error_msg = f"✘ Línea {p.lineno(1)}: variable '{name}' no declarada"
        print(error_msg)
        semantic_errors.append(error_msg)
        p[0] = 'undefined'

def p_expression_true(p):
    'expression : TRUE'
    log_info("expression")
    p[0] = 'boolean'

def p_expression_false(p):
    'expression : FALSE'
    log_info("expression")
    p[0] = 'boolean'


def p_expression_increment(p):
    '''expression : expression PLUSPLUS
                    | expression MINUSMINUS
                    | PLUSPLUS expression
                    | MINUSMINUS expression'''
    log_info("increment/decrement expression")

def p_consolelog(p):
    '''consolelog : CONSOLE DOT LOG LPAREN lista_expresiones_opt RPAREN SEMICOLON'''
    log_info("console.log")

# ----------- IF MANAGEMENT STRUCTURE -------------
def p_controlEstructure(p):
    '''controlEstructure : IF LPAREN expression RPAREN statement 
                        | IF LPAREN expression RPAREN statement ELSE statement 
                        | IF LPAREN expression RPAREN statement ELSE IF LPAREN expression RPAREN statement 
                        | IF LPAREN expression RPAREN statement ELSE IF LPAREN expression RPAREN statement ELSE statement'''
    log_info("if/else structure")

# ----------- Statements and instructions -------------
def p_statement(p):
    '''statement : LBRACE instruction_list RBRACE
                 | letAssignment
                 | varAssignment
                 | constAssignment
                 | declaracion
                 | function
                 | arrow_function
                 | async_function
                 | consolelog
                 | expression SEMICOLON
                 | controlEstructure
                 | forEstructure
                 | RETURN SEMICOLON
                 | class_definition'''
                
    log_info("statement")


def p_statement_block(p):
    '''statement : LBRACE RBRACE'''
    log_info("block statement")


def p_instruction_list(p):
    '''instruction_list : instruction_list statement
                        | statement
                        | empty'''
    log_info("instruction list")

# ----------- Empty -------------
def p_empty(p):
    'empty :'
    pass

# ----------- Error Handling -------------
def p_error(p):
    if p:
        msg = f"✘ Línea {p.lineno}: token inesperado '{p.value}'"
    else:
        msg = "✘ Fin de archivo inesperado"
    print(msg)
    error_log.append(msg)
    
    
    
    
    

# ----------- Roberto Barrios -------------
# ----------- CONST ASSIGNMENT -------------

def p_constAssignment(p):
    'constAssignment : CONST IDENTIFIER COLON type EQUAL expression SEMICOLON'
    var_name = p[2]
    if var_name in symbol_table["consts"]:
        log_error(f"Error: constante '{var_name}' ya fue declarada previamente.")
    else:
        symbol_table["consts"][var_name] = {"type": p[4], "value": p[6]}
    log_info(f"const assignment (typed): {var_name}")


def p_constAssignment_no_type(p):
    'constAssignment : CONST IDENTIFIER EQUAL expression SEMICOLON'
    var_name = p[2]
    if var_name in symbol_table["consts"]:
        log_error(f"Error: constante '{var_name}' ya fue declarada previamente.")
    else:
        symbol_table["consts"][var_name] = {"value": p[4]}
    log_info(f"const assignment: {var_name}")



# ----------- CLASS WITH CONSTRUCTOR -------------
def p_class_definition(p):
    'class_definition : CLASS IDENTIFIER LBRACE class_body RBRACE'
    class_name = p[2]
    if class_name in symbol_table["classes"]:
        log_error(f"Error: clase '{class_name}' ya existe.")
    else:
        symbol_table["classes"][class_name] = {}
    log_info(f"class definition: {class_name}")


def p_class_body(p):
    '''class_body : class_body class_element
                  | class_element
                  | empty'''
    log_info("class body")

def p_class_element(p):
    '''class_element : function
                     | letAssignment
                     | varAssignment
                     | constAssignment'''
    log_info("class element")


# —————— Switch ——————
def p_controlEstructure_switch(p):
    'controlEstructure : SWITCH LPAREN expression RPAREN LBRACE push_switch case_list pop_switch RBRACE'
    # p[7] es la lista de casos
    p[0] = p[7]
    log_info("switch structure")


# —————— Lista de casos ——————
def p_case_list(p):
    '''case_list : case_list case
                 | case
                 | empty'''
    if len(p) == 3:
        # concatenamos listas
        p[0] = p[1] + [p[2]]
    elif p[1] is None:
        # empty ⇒ sin casos
        p[0] = []
    else:
        # un único case
        p[0] = [p[1]]
    log_info("case list")


# —————— Caso individual ——————
def p_case(p):
    '''case : CASE expression COLON instruction_list
            | DEFAULT COLON instruction_list'''
    if p[1] == 'case':
        # guardamos (etiqueta, expresión, lista de instrucciones)
        p[0] = ('case', p[2], p[4])
    else:
        # DEFAULT no lleva expresión
        p[0] = ('default', p[3])
    log_info("case")


# -----------BREAK -------------
def p_statement_break(p):
    'statement : BREAK SEMICOLON'
    if not any(ctx in ("loop", "switch") for ctx in context_stack):
        semantic_errors.append("Error semántico: 'break' fuera de bucle o switch")
    log_info("break statement")




def p_statement_continue(p):
    'statement : CONTINUE SEMICOLON'
    if not any(ctx == "loop" for ctx in context_stack):
        semantic_errors.append("Error semántico: 'continue' fuera de bucle")
    log_info("continue statement")


# -----------ENUM -------------
def p_enum_definition(p):
    'enum_definition : ENUM IDENTIFIER LBRACE enum_members RBRACE'
    enum_name = p[2]
    members = p[4]

    if enum_name in symbol_table["enums"]:
        log_error(f"Error: enum '{enum_name}' ya fue declarado.")
    elif len(members) != len(set(members)):
        log_error(f"Error: enum '{enum_name}' tiene miembros duplicados.")
    else:
        symbol_table["enums"][enum_name] = members
    log_info(f"enum: {enum_name}")


def p_enum_members(p):
    '''enum_members : IDENTIFIER
                    | IDENTIFIER COMMA enum_members'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]
    
    # Validación semántica
    if len(set(p[0])) != len(p[0]):
        log_error("Error: miembros duplicados en definición de enum.")
    log_info("enum members")

    
    
# ----------- ASYNC function -------------
def p_async_function(p):
    'async_function : ASYNC FUNCTION IDENTIFIER LPAREN parameters RPAREN COLON type LBRACE body_function RBRACE'
    fname = p[3]
    if fname in symbol_table["functions"]:
        log_error(f"Error: función '{fname}' ya existe.")
    else:
        symbol_table["functions"][fname] = {"async": True, "returnType": p[8]}
    log_info(f"async function: {fname}")

    
    
    
    
    
    

# ----------- Andres Zambrano -------------
    
# ----------- While -------------
def p_controlEstructure_while(p):
    'controlEstructure : WHILE LPAREN expression RPAREN push_loop statement pop_loop'
    p[0] = p[6]
    log_info("while structure")






# ----------- Var - Const-------------
def p_varAssignment(p):
    'varAssignment : VAR IDENTIFIER COLON type EQUAL expression SEMICOLON'
    log_info(f"varAssignment: {p[2]}")

def p_varAssignment_no_type(p):
    'varAssignment : VAR IDENTIFIER EQUAL expression SEMICOLON'
    log_info(f"varAssignment (no type): {p[2]}")

# ----------- Arrow Function -------------
def p_arrow_function(p):
    'arrow_function : CONST IDENTIFIER EQUAL LPAREN parameters RPAREN ARROW LBRACE body_function RBRACE SEMICOLON'
    log_info(f"arrow function: {p[2]}")


# ----------- INTERFACE Definition -------------

def p_interface(p):
    'interface : INTERFACE IDENTIFIER LBRACE interface_body RBRACE'
    log_info(f"interface: {p[2]}")

def p_interface_body(p):
    '''interface_body : interface_body interface_property
                      | interface_property
                      | empty'''
    log_info("interface body")

def p_interface_property(p):
    'interface_property : IDENTIFIER COLON type SEMICOLON'
    log_info(f"property {p[1]} in interface")


def p_expression_variables(p):
    '''expression : LBRACE object_properties RBRACE'''
    log_info("object with many variables")

def p_object_properties(p):
    '''object_properties : object_property
                         | object_property COMMA object_properties
                         | empty'''
    log_info("object properties")

def p_object_property(p):
    '''object_property : IDENTIFIER COLON expression'''
    log_info(f"object property: {p[1]}")



# ----------- Parser Execution -------------
parser = yacc.yacc(start='program')

if semantic_errors:
    print("\nErrores semánticos encontrados:")
    for err in semantic_errors:
        print(err)
else:
    print("\nAnálisis semántico completado sin errores.")



def run_parser(file_path, username):
    global error_log, success_log, semantic_errors, symbol_table, vars_con_error, context_stack
    error_log = []
    success_log = []
    semantic_errors = []
    context_stack = []
    symbol_table = {}
    vars_con_error = set()
    
    # 🔁 Reset de llaves y errores léxicos
    brace_stack.clear()
    lexical_errors.clear()
    if brace_stack:
        error_log.append("⚠ Error: hay llaves de apertura '{' sin su correspondiente cierre '}'")
        


    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
        parser.parse(data)

    base_username = username.lower().replace(" ", "")
    now = datetime.datetime.now().strftime("%d%m%Y-%Hh%M")
    log_file = f"logs/sintactico-{base_username}-{now}.txt"

    with open(log_file, 'w', encoding='utf-8') as log:
        log.write("-------Resultados del análisis sintáctico:-----------\n\n")
        if success_log:
            log.write("✔ Producciones reconocidas:\n")
            for s in success_log:
                log.write(f"{s}\n")
            log.write("\n")
        if error_log:
            log.write("---------- :( Errores sintácticos encontrados-------------:\n")
            for err in error_log:
                log.write(f"{err}\n")
        else:
            log.write(" ---------------:D Análisis sintáctico completado sin errores. -----------------\n")
        
        
        log.write("\n")
        log.write("-------Resultados del análisis semántico:-----------\n\n")
        if semantic_errors:
            log.write("---------- :( Errores semánticos encontrados-------------:\n")
            for err in semantic_errors:
                log.write(f"{err}\n")
            log.write("\n")
        else:
            log.write("--------------- :D Análisis semántico completado sin errores. -----------------\n\n")
        if symbol_table:
            log.write("✔ Variables declaradas correctamente:\n")
            alguna = False
            for var, tipo in symbol_table.items():
                 if var not in vars_con_error:
                    log.write(f"{var}: {tipo}\n")
                    alguna = True
        if not alguna:
            log.write("Ninguna variable fue declarada correctamente.\n")
        else:
           log.write("No hay variables declaradas correctamente.\n")

       

    

def run_parser_string(data: str) -> str:
    global error_log, success_log, semantic_errors, symbol_table, vars_con_error
    error_log = []
    success_log = []
    semantic_errors = []
    symbol_table = {}
    vars_con_error = set()

    
    # 🔁 Reset de pila y errores léxicos
    brace_stack.clear()
    lexical_errors.clear()



    parser.parse(data)


    if brace_stack:
        error_log.append("⚠ Error: hay llaves de apertura '{' sin su correspondiente cierre '}'")


    output = "-------Resultados del análisis sintáctico:-----------\n\n"
    if success_log:
        output += "✔ Producciones reconocidas:\n"
        output += "\n".join(success_log) + "\n\n"
    if error_log:
        output += "✘ Errores sintácticos:\n"
        output += "\n".join(error_log) + "\n"
    else:
        output += "✔ Análisis sintáctico completado sin errores.\n\n"

    output += "-------Resultados del análisis semántico:-----------\n\n"
    if semantic_errors:
        output += "✘ Errores semánticos:\n"
        output += "\n".join(semantic_errors) + "\n\n"
    else:
        output += "✔ Análisis semántico completado sin errores.\n\n"

    if symbol_table:
        output += "✔ Variables declaradas correctamente:\n"
        alguna = False
        for var, tipo in symbol_table.items():
            if var not in vars_con_error:
                output += f"{var}: {tipo}\n"
                alguna = True
        if not alguna:
            output += "Ninguna variable fue declarada correctamente.\n"
    else:
        output += "No se detectaron variables.\n"

    return output








