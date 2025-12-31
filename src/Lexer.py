from typing import Any

from src.Token import Token
from src.TokenKind import TokenKind

source: str = 'let x=5; let y = 10; x = 9; output(500);'

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
        start = i
        while i < len(source) and source[i] == '"':
            i += 1
        tokens.append(source[start:i])
        continue

    if char.isalpha():
        start = i
        while i < len(source) and source[i].isalpha():
            i += 1
        tokens.append(source[start:i])
        continue

    if char.isdigit():
        start = i
        while i < len(source) and source[i].isdigit():
            i += 1
        tokens.append(source[start:i])
        continue

    if char in "=;()":
        tokens.append(char)
        i += 1
        continue

    raise Exception(f"Unknown character: {char}")

#print(tokens)

parsed_tokens: list[Any] = []

for token in tokens:
    if token in keywords:
        parsed_tokens.append(Token(TokenKind.KEYWORD, token))
    elif token == '"':
        parsed_tokens.append(Token(TokenKind.STRING, token))
    elif token.isalpha():
        parsed_tokens.append(Token(TokenKind.IDENTIFIER, token))
    elif token in "=;()":
        parsed_tokens.append(Token(TokenKind.SYMBOL, token))
    elif token.isdigit():
        parsed_tokens.append(Token(TokenKind.NUMBER, int(token)))
    else:
        raise Exception(f"Unknown token: {token}")


#print(parsed_tokens)


