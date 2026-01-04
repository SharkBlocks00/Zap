from Errors.Errors import ZapError


class TypeError(ZapError):
    pass


class InvalidBinaryOperation(TypeError):
    def __init__(self, left, operator, right, **kwargs):
        super().__init__(
            f"Invalid operation: {type(left).__name__} {operator} {type(right).__name__}",
            **kwargs,
        )


class InvalidFunctionArgumentType(TypeError):
    def __init__(self, name, expected_type, received_type, **kwargs):
        super().__init__(
            f"Function '{name}' expected argument of type '{expected_type.__name__}', but received type '{received_type.__name__}'",
            **kwargs,
        )
