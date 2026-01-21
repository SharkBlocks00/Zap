from typing import Any

from Errors.ParseErrors import UnexpectedTokenError, UnterminatedStringError
from Logger import get_logger
from Token import Token
from TokenKind import TokenKind

logger = get_logger(__name__)

source: str = """
let name = request("Enter your name: ");
output("Hi" + name);
"""

i: int = 0
tokens: list[Any] = []

keywords: list[str] = [
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

line_count: int = -1

while i < len(source):
    char = source[i]

    if char == "\n":
        line_count += 1
        i += 1
        continue

    if char.isspace():
        i += 1
        continue

    if char == "-" and i + 1 < len(source) and source[i + 1] == "-":
        while i < len(source) and source[i] != "\n":
            i += 1
        continue

    if char == '"':
        i += 1
        start = i

        while i < len(source) and source[i] != '"':
            i += 1

        if i >= len(source):
            raise UnterminatedStringError(line=line_count + 1)

        tokens.append(("STRING", source[start:i]))
        i += 1
        continue

    if char.isalpha():
        start = i
        while i < len(source) and (
            source[i].isalnum() or source[i] == "_" or source[i] == "-"
        ):
            i += 1

        if source[start:i] == "True" or source[start:i] == "False":
            tokens.append(("BOOLEAN", source[start:i]))
        elif source[start : i + 1].endswith("(") and source[start:i] not in keywords:
            tokens.append(("FunctionCall", source[start:i]))
        else:
            # logger.debug(f"Identified identifier: {source[start:i]}")
            tokens.append(("IDENTIFIER", source[start:i]))
        continue

    if char.isdigit():
        start = i
        while i < len(source) and source[i].isdigit():
            i += 1
        tokens.append(("NUMBER", source[start:i]))
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
            and i + 1 < len(source)
            and source[i + 1] == "="
        ):
            tokens.append(("SYMBOL", char + "="))
            i += 2
            continue
        elif char in ["&", "|"]:
            if source[i + 1] in ["&", "|"]:
                tokens.append(("SYMBOL", char + char))
                i += 2
                continue
            tokens.append(("SYMBOL", char))
            i += 1
            continue
        tokens.append(("SYMBOL", char))
        i += 1
        continue

    raise UnexpectedTokenError(char, line=line_count + 1)

# logger.debug(tokens)

parsed_tokens: list[Any] = []

for kind, value in tokens:
    if kind == "STRING":
        parsed_tokens.append(Token(TokenKind.STRING, value))
    elif kind == "BOOLEAN":
        parsed_tokens.append(Token(TokenKind.BOOLEAN, value))
    elif kind == "IDENTIFIER" and value == "break":
        parsed_tokens.append(Token(TokenKind.BREAK, value))
    elif kind == "IDENTIFIER" and value in keywords:
        parsed_tokens.append(Token(TokenKind.KEYWORD, value))
    elif kind == "IDENTIFIER":
        parsed_tokens.append(Token(TokenKind.IDENTIFIER, value))
    elif kind == "NUMBER":
        parsed_tokens.append(Token(TokenKind.NUMBER, value))
    elif kind == "SYMBOL":
        parsed_tokens.append(Token(TokenKind.SYMBOL, value))
    elif kind == "FunctionCall":
        parsed_tokens.append(Token(TokenKind.FunctionCall, value))
    else:
        raise UnexpectedTokenError(value)

# for token in parsed_tokens:
#     logger.debug(f"TokenKind: {token.kind}, Value: {token.value}")
# logger.debug(f"Line count: {line_count}")
