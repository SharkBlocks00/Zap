import os
from Errors.Errors import ZapError
from Interpreter import Interpreter
from Lexer import Lexer
from Parser import Parser


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "..", "test.zap")
    with open(file_path, "r") as f:
        source = f.read()


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
