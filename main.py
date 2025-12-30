import argparse
from pathlib import Path
from Repl import repl
from Parser import Parser

""" Main file for Zap programming language """

def setup_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file")
    return parser

def parse_arguments() -> argparse.Namespace:
    parser = setup_argparser()
    args = parser.parse_args()
    return args

def get_file(file_path: str) -> Path:
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist")
    if not file_path.is_file():
        raise FileNotFoundError(f"File {file_path} is not a file")
    if not file_path.suffix == ".zap":
        raise FileNotFoundError(f"File {file_path} is not a zap file")
    return file_path


def main():
    args = parse_arguments()
    parser: Parser = Parser()

    if args.file:
        file = get_file(args.file)

        with open(file, "r") as file:
            data = file.read()
            parser.parse(data)

    repl(parser)

    # print(parser.parse("Erm; "))

if __name__ == "__main__":
    main()