from __future__ import annotations

from Errors.RuntimeErrors import UndefinedVariableError, CannotAssignToConstant


class Environment:
    def __init__(self, parent: Environment | None = None):
        self.variables: dict[str, list[object, bool]] = {}
        self.parent = parent

    def define(self, name: str, value: object, mutable: bool = True) -> None:
        if name in self.variables:
            raise CannotAssignToConstant(name)
        self.variables[name] = [value, mutable]

    def assign(self, name: str, value: object) -> None:
        if name in self.variables:
            if not self.variables[name][1]:
                raise CannotAssignToConstant(name)
            self.variables[name][0] = value
        elif self.parent is not None:
            self.parent.assign(name, value)
        else:
            raise UndefinedVariableError(name)

    def get(self, name: str) -> object:
        if name in self.variables:
            return self.variables[name]
        elif self.parent is not None:
            return self.parent.get(name)
        else:
            raise UndefinedVariableError(name)
