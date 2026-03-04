import os
import sys
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from typing import Dict, Tuple
import builtins

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from src.Errors.Errors import ZapError
from src.Interpreter import Interpreter
from src.Lexer import Lexer
from src.Parser import Parser


def run_test(file_path: str) -> Tuple[bool, str, str]:
    output_stream = StringIO()
    original_input = builtins.input

    def fake_input(prompt: str = "") -> str:
        # Keep prompts visible in captured output while avoiding interactive blocking.
        if prompt:
            print(prompt, end="")
        return os.environ.get("ZAP_TEST_INPUT", "test-user")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            code = file.read()

        lexer = Lexer()
        parser = Parser(code, lexer)
        interpreter = Interpreter(lexer, parser)
        builtins.input = fake_input
        with redirect_stdout(output_stream), redirect_stderr(output_stream):
            nodes, _ = parser.parse(parser.tokens, 0)
            interpreter.nodes = nodes
            interpreter.interpret_nodes(nodes, interpreter.global_environment)
        return True, "Passed", output_stream.getvalue().strip()
    except ZapError as error:
        return False, f"ZapError: {error}", output_stream.getvalue().strip()
    except Exception as error:
        return False, f"Unexpected error: {error}", output_stream.getvalue().strip()
    finally:
        builtins.input = original_input


def main() -> int:
    tests: Dict[str, Tuple[bool, str, str]] = {}
    tests_dir = os.path.join(ROOT_DIR, "tests")
    test_files = sorted(file for file in os.listdir(tests_dir) if file.endswith(".zap"))

    if not test_files:
        print("No .zap test files found in tests/.")
        return 1

    print(f"Running {len(test_files)} test(s)...")
    print("-" * 50)

    for file_name in test_files:
        file_path = os.path.join(tests_dir, file_name)
        passed, message, captured_output = run_test(file_path)
        tests[file_name] = (passed, message, captured_output)
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {file_name}")
        if not passed:
            print(f"       {message}")
            if captured_output:
                print("       Captured output:")
                for line in captured_output.splitlines():
                    print(f"       {line}")

    print("-" * 50)
    passed_count = sum(1 for passed, _, _ in tests.values() if passed)
    failed_count = len(tests) - passed_count
    print(f"Summary: {passed_count} passed, {failed_count} failed, {len(tests)} total")

    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
