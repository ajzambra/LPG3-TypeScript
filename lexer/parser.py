from lexer.lexer import tokens, reserved
import ply.yacc as yacc
import datetime

# ----------- Logs -------------
success_log = []
error_log = []

def log_info(msg):
    print(f"✔ {msg}")
    success_log.append(f"✔ {msg}")

# ----------- First Rule (ROOT) -------------
def p_program(p):
    '''program : program element
               | element'''
    log_info("program")

def p_element(p):
    '''element : letAssignment
               | declaracion
               | function
               | constAssignment
               | enum_definition
               | controlEstructure
               | forEstructure
               | class_definition
               | statement
               | expression SEMICOLON
               | consolelog'''
    log_info("element")


# ----------- Declare Variable -------------
def p_letAssignment(p):
    'letAssignment : LET IDENTIFIER COLON type EQUAL expression SEMICOLON'
    log_info(f"letAssignment: {p[2]}")

def p_letAssignment_no_type(p):
    'letAssignment : LET IDENTIFIER EQUAL expression SEMICOLON'
    log_info(f"letAssignment (no type): {p[2]}")

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

# ----------- For -------------
def p_forEstructure(p):
    '''forEstructure : FOR LPAREN for_init SEMICOLON expression SEMICOLON for_update RPAREN statement'''
    log_info("for structure")

def p_for_init(p):
    '''for_init : LET IDENTIFIER EQUAL expression
                | LET IDENTIFIER COLON type EQUAL expression
                | expression
                | empty'''
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
    log_info(f"function declaration: {p[2]}")

def p_parameters(p):
    '''parameters : IDENTIFIER COLON type
                | IDENTIFIER COLON type COMMA parameters
                | empty'''
    log_info("parameters")

def p_body_function(p):
    '''body_function : instruction_list'''
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
            | type LBRACKET RBRACKET'''
    log_info("type")

# ----------- EXPRESSION AND CONSOLE LOG ---------
def p_expression(p):
    '''expression : expression PLUS expression
                | expression MINUS expression
                | expression TIMES expression
                | expression DIV expression
                | expression MOD expression
                | expression PLUS_ASSIGN expression
                | expression MINUS_ASSIGN expression
                | expression MULT_ASSIGN expression
                | expression DIV_ASSIGN expression
                | expression MOD_ASSIGN expression
                | expression POT expression
                | expression AND expression
                | expression OR expression
                | expression EQ expression
                | expression NEQ expression
                | expression STRICT_EQ expression
                | expression STRICT_NEQ expression
                | expression LT expression
                | expression GT expression
                | expression LE expression
                | expression GE expression
                | PROMPT LPAREN STRING RPAREN
                | NOT expression
                | LPAREN expression RPAREN
                | expression DOT IDENTIFIER
                | expression LBRACKET expression RBRACKET
                | IDENTIFIER LPAREN lista_expresiones_opt RPAREN
                | NUMBER
                | FLOAT
                | STRING
                | IDENTIFIER
                | TRUE
                | FALSE'''
    log_info("expression")

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
                 | consolelog
                 | expression SEMICOLON
                 | controlEstructure
                 | RETURN expression SEMICOLON
                 | forEstructure
                 | class_definition'''
    log_info("statement")


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



# ----------- Andres Zambrano -------------
    
# ----------- While -------------
def p_controlEstructure_while(p):
    'controlEstructure : WHILE LPAREN expression RPAREN statement'
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
    'function : CONST IDENTIFIER EQUAL LPAREN parameters RPAREN ARROW LBRACE body_function RBRACE SEMICOLON'
    log_info(f"arrow function: {p[2]}")

# ----------- Parser Execution -------------
parser = yacc.yacc(start='program')

def run_parser(file_path, username):
    global error_log, success_log
    error_log = []
    success_log = []

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

    

# ----------- Roberto Barrios -------------
# ----------- CONST ASSIGNMENT -------------
def p_constAssignment(p):
    'constAssignment : CONST IDENTIFIER COLON type EQUAL expression SEMICOLON'
    log_info(f"const assignment (typed): {p[2]}")

def p_constAssignment_no_type(p):
    'constAssignment : CONST IDENTIFIER EQUAL expression SEMICOLON'
    log_info(f"const assignment: {p[2]}")


# ----------- CLASS WITH CONSTRUCTOR -------------
def p_class_definition(p):
    'class_definition : CLASS IDENTIFIER LBRACE class_body RBRACE'
    log_info(f"class definition: {p[2]}")

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


# ----------- SWITCH ------------
def p_controlEstructure_switch(p):
    'controlEstructure : SWITCH LPAREN expression RPAREN LBRACE case_block RBRACE'
    log_info("switch structure")

def p_case_block(p):
    '''case_block : case_block case
                  | case
                  | empty'''
    log_info("case block")

def p_case(p):
    '''case : CASE expression COLON instruction_list
            | DEFAULT COLON instruction_list'''
    log_info("case")


# -----------ENUM -------------
def p_enum_definition(p):
    'enum_definition : ENUM IDENTIFIER LBRACE enum_members RBRACE'
    log_info(f"enum: {p[2]}")

def p_enum_members(p):
    '''enum_members : IDENTIFIER
                    | IDENTIFIER COMMA enum_members'''
    log_info("enum members")
    
    
# ----------- ASYNC function -------------
def p_async_function(p):
    'function : ASYNC FUNCTION IDENTIFIER LPAREN parameters RPAREN COLON type LBRACE body_function RBRACE'
    log_info(f"async function: {p[3]}")






