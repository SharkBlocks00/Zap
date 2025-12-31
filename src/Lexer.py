from typing import Any

from src.Token import Token
from src.TokenKind import TokenKind

source: str = 'let x=5; let y = 10; x = 9; output("hi"); let b = "hi";'

i: int = 0
tokens: list[Any] = []

keywords: list[str] = [
    "let",
    "output",
    "request",
]

while i < len(source):
    char = source[i]

    if char.isspace():
        i += 1
        continue

    if char == '"':
        i += 1
        start = i

        while i < len(source) and source[i] != '"':
            i += 1

        if i >= len(source):
            raise Exception("Unterminated string literal")

        tokens.append(("STRING", source[start:i]))
        i += 1
        continue

    if char.isalpha():
        start = i
        while i < len(source) and source[i].isalpha():
            i += 1
        tokens.append(("IDENTIFIER", source[start:i]))
        continue

    if char.isdigit():
        start = i
        while i < len(source) and source[i].isdigit():
            i += 1
        tokens.append(("NUMBER", source[start:i]))
        continue

    if char in "=;()":
        tokens.append(("SYMBOL", char))
        i += 1
        continue

    raise Exception(f"Unknown character: {char}")

#print(tokens)

parsed_tokens: list[Any] = []

for kind, value in tokens:
    if kind == "STRING":
        parsed_tokens.append(Token(TokenKind.STRING, value))
    elif kind == "IDENTIFIER" and value in keywords:
        parsed_tokens.append(Token(TokenKind.KEYWORD, value))
    elif kind == "IDENTIFIER":
        parsed_tokens.append(Token(TokenKind.IDENTIFIER, value))
    elif kind == "NUMBER":
        parsed_tokens.append(Token(TokenKind.NUMBER, int(value)))
    elif kind == "SYMBOL":
        parsed_tokens.append(Token(TokenKind.SYMBOL, value))
    else:
        raise Exception(f"Unknown token: {value}")

#print(parsed_tokens)


