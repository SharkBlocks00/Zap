from Errors.Errors import ZapError


class ParseError(ZapError):
    pass


class UnexpectedTokenError(ParseError):
    def __init__(self, token, **kwargs):
        super().__init__(f"Unexpected token: '{token}'", **kwargs)


class UnterminatedStringError(ParseError):
    def __init__(self, **kwargs):
        super().__init__("Unterminated string literal", **kwargs)


class ExpectedTokenError(ParseError):
    def __init__(self, expected, found, **kwargs):
        super().__init__(
            f"Expected token: '{expected}', but found: '{found}'", **kwargs
        )
