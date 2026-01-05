from TokenKind import TokenKind


class Token:
    def __init__(self, kind: TokenKind, value: str):
        self.kind = kind
        self.value = value
