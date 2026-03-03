from typing import Any

from Errors.ParseErrors import UnexpectedTokenError, UnterminatedStringError
from Logger import get_logger
from Token import Token
from TokenKind import TokenKind

logger = get_logger(__name__)

source: str = """
let name = request("Enter your name: ");
output("Hi" + name);
if (false) {
    output("Hello, world!");
}
"""


class Lexer:
    def __init__(self):
        self.i: int = 0
        self.tokens: list[Any] = []

        self.keywords: list[str] = [
            "let",
            "output",
            "request",
            "if",
            "else",
            "elseif",
            "func",
            "define",
            "while",
            "break",
            "foreach",
            "const",
        ]

        self.line_count: int = -1

    def lexate(self, source):
        while self.i < len(source):
            char = source[self.i]

            if char == "\n":
                self.line_count += 1
                self.i += 1
                continue

            if char.isspace():
                self.i += 1
                continue

            if char == "-" and self.i + 1 < len(source) and source[self.i + 1] == "-":
                while self.i < len(source) and source[self.i] != "\n":
                    self.i += 1
                continue

            if char == '"':
                self.i += 1
                start = self.i

                while self.i < len(source) and source[self.i] != '"':
                    self.i += 1

                if self.i >= len(source):
                    raise UnterminatedStringError(line=self.line_count + 1)

                self.tokens.append(("STRING", source[start : self.i]))
                self.i += 1
                continue

            if char.isalpha():
                start = self.i
                while self.i < len(source) and (
                    source[self.i].isalnum()
                    or source[self.i] == "_"
                    or source[self.i] == "-"
                ):
                    self.i += 1

                if (
                    source[start : self.i] == "true"
                    or source[start : self.i] == "false"
                ):
                    self.tokens.append(("BOOLEAN", source[start : self.i]))
                elif (
                    source[start : self.i + 1].endswith("(")
                    and source[start : self.i] not in self.keywords
                ):
                    self.tokens.append(("FunctionCall", source[start : self.i]))
                else:
                    # logger.debug(f"Identified identifier: {source[start:i]}")
                    self.tokens.append(("IDENTIFIER", source[start : self.i]))
                continue

            if char.isdigit():
                start = self.i
                while self.i < len(source) and source[self.i].isdigit():
                    self.i += 1
                self.tokens.append(("NUMBER", source[start : self.i]))
                continue

            if char in [
                "=",
                ";",
                "(",
                ")",
                "{",
                "}",
                "+",
                "-",
                "*",
                "/",
                "!",
                "<",
                ">",
                ":",
                "&",
                "|",
            ]:
                if (
                    char in ["=", "!", "<", ">"]
                    and self.i + 1 < len(source)
                    and source[self.i + 1] == "="
                ):
                    self.tokens.append(("SYMBOL", char + "="))
                    self.i += 2
                    continue
                elif char in ["&", "|"]:
                    if source[self.i + 1] in ["&", "|"]:
                        self.tokens.append(("SYMBOL", char + char))
                        self.i += 2
                        continue
                    self.tokens.append(("SYMBOL", char))
                    self.i += 1
                    continue
                self.tokens.append(("SYMBOL", char))
                self.i += 1
                continue

            raise UnexpectedTokenError(char, line=self.line_count + 1)

        # logger.debug(f"Tokens: {self.tokens}")
        self.parsed_tokens: list[Any] = []

        for kind, value in self.tokens:
            if kind == "STRING":
                self.parsed_tokens.append(Token(TokenKind.STRING, value))
            elif kind == "BOOLEAN":
                self.parsed_tokens.append(Token(TokenKind.BOOLEAN, value))
            elif kind == "IDENTIFIER" and value == "break":
                self.parsed_tokens.append(Token(TokenKind.BREAK, value))
            elif kind == "IDENTIFIER" and value in self.keywords:
                self.parsed_tokens.append(Token(TokenKind.KEYWORD, value))
            elif kind == "IDENTIFIER":
                self.parsed_tokens.append(Token(TokenKind.IDENTIFIER, value))
            elif kind == "NUMBER":
                self.parsed_tokens.append(Token(TokenKind.NUMBER, value))
            elif kind == "SYMBOL":
                self.parsed_tokens.append(Token(TokenKind.SYMBOL, value))
            elif kind == "FunctionCall":
                self.parsed_tokens.append(Token(TokenKind.FunctionCall, value))
            else:
                raise UnexpectedTokenError(value)
        return self.parsed_tokens

        # for token in parsed_tokens:
        #     logger.debug(f"TokenKind: {token.kind}, Value: {token.value}")
        # logger.debug(f"Line count: {line_count}")
