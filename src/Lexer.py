from typing import Any

from Token import Token
from TokenKind import TokenKind
from Errors.ParseErrors import UnexpectedTokenError, UnterminatedStringError

source: str = """
let x = 10;
output(x); -- plz dont break
if (true) { -- still plz dont break
    output("Condition is true");
} else {
    output("Condition is false");
}
func greet = define() {
    output("Hello, World!");
}
greet();
let name = request("Enter your name: ");
output("Hello " + name + "!");
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
]

while i < len(source):
    char = source[i]

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
            raise UnterminatedStringError()

        tokens.append(("STRING", source[start:i]))
        i += 1
        continue

    if char.isalpha():
        start = i
        while i < len(source) and source[i].isalnum():
            i += 1
        
        if source[start:i] == "true" or source[start:i] == "false":
            tokens.append(("BOOLEAN", source[start:i]))
        elif source[start:i+1].endswith("(") and not source[start:i] in keywords:
            tokens.append(("FUNCTION_CALL", source[start:i]))
        else:
            #print(f"Identified identifier: {source[start:i+1]}")
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

    raise UnexpectedTokenError(char)

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
    elif kind == "FUNCTION_CALL":
        parsed_tokens.append(Token(TokenKind.FUNCTION_CALL, value))
    else:
        raise UnexpectedTokenError(value)

# for token in parsed_tokens:
#     print(f"TokenKind: {token.kind}, Value: {token.value}")


