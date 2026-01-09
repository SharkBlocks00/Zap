from __future__ import annotations

from Errors.RuntimeErrors import CannotAssignToConstant, UndefinedVariableError


class Environment:
    def __init__(self, parent: Environment | None = None):
        """
        Initialize an Environment representing a lexical scope with an optional parent.
        
        Initializes an empty `variables` dictionary where each key is a variable name (str) and each value is a two-element list: `[value, mutable]` (the stored value and a boolean indicating mutability). Sets `parent` to the provided enclosing Environment or `None` for a top-level scope.
        
        Parameters:
            parent (Environment | None): Optional enclosing environment for nested scopes.
        """
        self.variables: dict[str, list[object]] = {}
        self.parent = parent

    def define(self, name: str, value: object, mutable: bool = True) -> None:
        """
        Declare a new variable in the current environment with an initial value and mutability.
        
        Parameters:
            name (str): The variable name to define.
            value (object): The initial value to assign to the variable.
            mutable (bool): If True, the variable can be reassigned later; if False, it is constant. Defaults to True.
        
        Raises:
            CannotAssignToConstant: If a variable with the same name already exists in the current environment.
        
        Notes:
            The variable is stored as a two-element list [value, mutable] in this environment.
        """
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