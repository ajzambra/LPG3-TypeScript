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
]

# Reserved words
reserved = {
    # 'if': 'IF', 'else': 'ELSE', ...
}

# Merge reserved into tokens list
tokens += list(reserved.values())

# Token regex rules go here...
# e.g., t_PLUS = r'\+'

t_ignore = ' \t\r'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

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
