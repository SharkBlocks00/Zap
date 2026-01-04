from Errors.Errors import ZapError


class TypeError(ZapError):
    pass


class InvalidBinaryOperation(TypeError):
    def __init__(
        self,
        left: object,
        operator: str,
        right: object,
        *,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(
            f"Invalid operation: {type(left).__name__} {operator} {type(right).__name__}",
            line=line,
            column=column,
        )


class InvalidFunctionArgumentType(TypeError):
    def __init__(
        self,
        name: str,
        expected_type: type,
        received_type: type,
        *,
        line: int | None = None,
        column: int | None = None,
    ):
        super().__init__(
            f"Function '{name}' expected argument of type '{expected_type.__name__}', but received type '{received_type.__name__}'",
            line=line,
            column=column,
        )
