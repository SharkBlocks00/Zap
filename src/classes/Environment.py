from __future__ import annotations

from Errors.RuntimeErrors import UndefinedVariableError


class Environment:
    def __init__(self, parent: Environment | None = None):
        self.variables: dict[str, object] = {}
        self.parent = parent

    def define(self, name: str, value: object) -> None:
        self.variables[name] = value

    def assign(self, name: str, value: object) -> None:
        if name in self.variables:
            self.variables[name] = value
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
