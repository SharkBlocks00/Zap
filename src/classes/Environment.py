from __future__ import annotations

from Errors.RuntimeErrors import CannotAssignToConstant, UndefinedVariableError


class Environment:
    def __init__(self, parent: Environment | None = None):
        self.variables: dict[str, tuple[object, bool]] = {}
        self.parent = parent

    def define(self, name: str, value: object, mutable: bool = True) -> None:
        if name in self.variables:
            raise CannotAssignToConstant(name)
        self.variables[name] = (value, mutable)

    def assign(self, name: str, value: object) -> None:
        if name in self.variables:
            if not self.variables[name][1]:
                raise CannotAssignToConstant(name)
            _, mutable = self.variables[name]
            self.variables[name] = (value, mutable)
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
