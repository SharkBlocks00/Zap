from Errors.Errors import ZapError


class RuntimeError(ZapError):
    pass


class UndefinedVariableError(RuntimeError):
    def __init__(self, name, **kwargs):
        super().__init__(f"Undefined variable '{name}'", **kwargs)


class InvalidAssignmentError(RuntimeError):
    def __init__(self, name, **kwargs):
        super().__init__(f"Cannot assign to undefined variable'{name}'", **kwargs)


class NotCallableError(RuntimeError):
    def __init__(self, name, **kwargs):
        super().__init__(f"'{name}' is not callable", **kwargs)
