from Errors.Errors import ZapError


class ParseError(ZapError):
    pass


class UnexpectedTokenError(ParseError):
    def __init__(
        self, token: str, *, line: int | None = None, column: int | None = None
    ):
        super().__init__(f"Unexpected token: '{token}'", line=line, column=column)


class UnterminatedStringError(ParseError):
    def __init__(self, *, line: int | None = None, column: int | None = None):
        super().__init__("Unterminated string literal", line=line, column=column)


class ExpectedTokenError(ParseError):
    def __init__(
        self,
        expected: str,
        found: str,
        *,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(
            f"Expected token: '{expected}', but found: '{found}'",
            line=line,
            column=column,
        )
