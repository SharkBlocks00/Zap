import os
import sys
from Errors.Errors import ZapError
from Interpreter import Interpreter
from Lexer import Lexer
from Parser import Parser


def main():
    if len(sys.argv) < 2:
        print("Usage: zap <file_path>")
        return

    file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return
    if not os.access(file_path, os.R_OK):
        print(f"File not readable: {file_path}")
        return
    if os.path.splitext(file_path)[1] != ".zap":
        print(f"Invalid file type: {file_path}")
        return


    try:
        with open(file_path, "r") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return


    lexer = Lexer()
    parser = Parser(source, lexer)
    interpreter = Interpreter(lexer, parser)

    try:
        nodes, _ = parser.parse(parser.tokens, 0)
        interpreter.nodes = nodes
        interpreter.interpret_nodes(nodes, interpreter.global_environment)
    except ZapError as error:
        print(f"Zap {error.__class__.__name__}:\n{error}")


if __name__ == "__main__":
    main()
