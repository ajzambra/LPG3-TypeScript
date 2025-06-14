import ply.lex as lex
import datetime

# INICIO Aporte Leonardo Zambrano
# Tokens for identifiers, primitive types, arithmetic ops...
# FIN Aporte Leonardo Zambrano

# INICIO Aporte Andrés Zambrano
# Tokens for assignment/comparison operators, object structure...
# FIN Aporte Andrés Zambrano

# INICIO Aporte Roberto Barrios
# Tokens for logical operators, delimiters, comments, tuples...
# FIN Aporte Roberto Barrios

# Full list of token names (must include all from all contributors)
tokens = [
    # Identifiers, keywords, operators, etc.

    'PLUS', 'MINUS', 'TIMES', 'DIV', 'MOD', 'POT',
    'IDENTIFIER', 'EQUAL','STRING','LBRACKET', 'RBRACKET', 
    'COMMA', 'SEMICOLON',
    #Added by Leonardo Zambrano

]

# Reserved words
reserved = {
    # 'if': 'IF', 'else': 'ELSE', ...


    'number': 'NUMBER_TYPE',
    'string': 'STRING_TYPE',
    'boolean': 'BOOLEAN_TYPE',
    'null': 'NULL_TYPE',
    'undefined': 'UNDEFINED_TYPE',
    'bigint': 'BIGINT_TYPE',
    'symbol': 'SYMBOL_TYPE',
    'let': 'LET',
    'var': 'VAR',
    
    #Added by Leonardo Zambrano
}

# Merge reserved into tokens list
tokens += list(reserved.values())

# Token regex rules go here...
# e.g., t_PLUS = r'\+'

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_POT = r'\*\*'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA     = r','
t_SEMICOLON = r';'
t_EQUAL   = r'='
#Added by Leonardo Zambrano




#Added by Leonardo Zambrano
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_STRING(t):
    r'(\"([^\\\n"]|\\.)*\")|(\'([^\\\n\']|\\.)*\')'
    t.value = str(t.value)
    return t


t_ignore = ' \t\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)




#Creating the lexer
lexer = lex.lex()






def run_lexer(file_path, username):
    lexer = lex.lex()
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
        lexer.input(data)
        base_username = username.lower().replace(" ", "")
        now = datetime.datetime.now().strftime("%d-%m-%Y-%Hh%M")
        log_file = f"logs/lexer-{base_username}-{now}.txt"

        with open(log_file, 'w', encoding='utf-8') as log:
            while True:
                tok = lexer.token()
                if not tok:
                    break
                line = f"{tok.type}({tok.value}) at line {tok.lineno}\n"
                log.write(line)
                print(line.strip())
