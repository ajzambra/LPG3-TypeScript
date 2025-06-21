
import sys
from lexer.parser import run_parser
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python run_parser.py <archivo.ts> <usuarioGit>")
    else:
        file_path = sys.argv[1]
        username = sys.argv[2]
        run_parser(file_path, username)
