from enum import Enum


class TokenKind(Enum):
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    SYMBOL = "SYMBOL"
    EOF = "EOF"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    FUNCTION_CALL = "FUNCTION_CALL"
