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
    
    #Added by Leonardo Zambrano
    'PLUS', 'MINUS', 'TIMES', 'DIV', 'MOD', 'POT',
    'IDENTIFIER', 'EQUAL','STRING','LBRACKET', 'RBRACKET', 
    'COMMA', 'SEMICOLON','NUMBER', 'FLOAT',
    
    #Added by Andres Zambrano
    'EQUALS', 'PLUS_ASSIGN', 'MINUS_ASSIGN', 'MULT_ASSIGN', 'DIV_ASSIGN', 'MOD_ASSIGN',
    'EQ', 'NEQ', 'STRICT_EQ', 'STRICT_NEQ',
    'LT', 'GT', 'LE', 'GE',
    'COLON', 'LBRACE', 'RBRACE','LPAREN', 'RPAREN',
    'DOT',
    
    #Added by Roberto Barrios:
    'AND', 'OR', 'NOT', 'ARROW'
]

# Reserved words
reserved = {
    #Added by Leonardo Zambrano
    'number': 'NUMBER_TYPE',
    'string': 'STRING_TYPE',
    'boolean': 'BOOLEAN_TYPE',
    'null': 'NULL_TYPE',
    'undefined': 'UNDEFINED_TYPE',
    'bigint': 'BIGINT_TYPE',
    'symbol': 'SYMBOL_TYPE',
    'let': 'LET',
    'var': 'VAR',

    #Added by Andres Zambrano
    'if':'IF',
    'else':'ELSE',
    'for':'FOR',
    'while':'WHILE',
    'switch':'SWITCH',
    'case':'CASE',
    'break':'BREAK',
    'continue':'CONTINUE',
    'return':'RETURN',
    'function':'FUNCTION',
    'const':'CONST',
    'class':'CLASS',
    'new':'NEW',
    'try':'TRY',
    'catch':'CATCH',
    'finally':'FINALLY',
    'void':'VOID',
    'any':'ANY',
    'true': 'TRUE',
    'false': 'FALSE',
    
    #Added by Roberto Barrios
    'export': 'EXPORT',
    'import': 'IMPORT',
    'type': 'TYPE',
    'enum': 'ENUM',
    
}

# Merge reserved into tokens list
tokens += list(reserved.values())

# Token regex rules go here...
# e.g., t_PLUS = r'\+'

#Added by Leonardo Zambrano
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

#Added by Andres Zambrano
t_EQUALS = r'='
t_PLUS_ASSIGN = r'\+='
t_MINUS_ASSIGN = r'-='
t_MULT_ASSIGN = r'\*='
t_DIV_ASSIGN = r'/='
t_MOD_ASSIGN = r'%='
t_EQ = r'=='
t_NEQ = r'!='
t_STRICT_EQ = r'==='
t_STRICT_NEQ = r'!=='
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_COLON = r':'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ignore = ' \t\r'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_DOT = r'\.'

#Added by Roberto Barrios
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_ARROW = r'=>'



#Added by Leonardo Zambrano
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_STRING(t):
    r'(\"([^\\\n"]|\\.)*\")|(\'([^\\\n\']|\\.)*\')'
    t.value = str(t.value)
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)


#Added by Roberto Barrios
def t_COMMENT(t):
    r'//[^\n]*'
    pass

def t_MULTILINE_COMMENT(t):
    r'/\*[\s\S]*?\*/'
    pass

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
