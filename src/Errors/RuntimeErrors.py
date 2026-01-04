from Errors.Errors import ZapError


class RuntimeError(ZapError):
    pass


class UndefinedVariableError(RuntimeError):
    def __init__(
        self, name: str, *, line: int | None = None, column: int | None = None
    ):
        super().__init__(f"Undefined variable '{name}'", line=line, column=column)


class InvalidAssignmentError(RuntimeError):
    def __init__(
        self, name: str, *, line: int | None = None, column: int | None = None
    ):
        super().__init__(
            f"Cannot assign to undefined variable '{name}'", line=line, column=column
        )


class NotCallableError(RuntimeError):
    def __init__(
        self, name: str, *, line: int | None = None, column: int | None = None
    ):
        super().__init__(f"'{name}' is not callable", line=line, column=column)
