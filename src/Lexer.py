from typing import Any

from Token import Token
from TokenKind import TokenKind

source: str = 'let x = 10; let ten = 10; if (x == ten) { output("x is equal to ten"); if (false) { output("second nested if working"); } else { output("else working");}}'

i: int = 0
tokens: list[Any] = []

keywords: list[str] = [
    "let",
    "output",
    "request",
    "if",
    "else",
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
        
        if source[start:i] == "true" or source[start:i] == "false":
            tokens.append(("BOOLEAN", source[start:i]))
        else:
            tokens.append(("IDENTIFIER", source[start:i]))
        continue

    if char.isdigit():
        start = i
        while i < len(source) and source[i].isdigit():
            i += 1
        tokens.append(("NUMBER", source[start:i]))
        continue

    if char in ["=", ";", "(", ")", "{", "}", "+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">="]:
        if char in ["=", "!", "<", ">"] and i + 1 < len(source) and source[i + 1] == "=":
            tokens.append(("SYMBOL", char + "="))
            i += 2
            continue
        tokens.append(("SYMBOL", char))
        i += 1
        continue

    raise Exception(f"Unknown character: {char}")

#print(tokens)

parsed_tokens: list[Any] = []

for kind, value in tokens:
    if kind == "STRING":
        parsed_tokens.append(Token(TokenKind.STRING, value))
    elif kind == "BOOLEAN":
        parsed_tokens.append(Token(TokenKind.BOOLEAN, value))
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

# for token in parsed_tokens:
#     print(f"TokenKind: {token.kind}, Value: {token.value}")


