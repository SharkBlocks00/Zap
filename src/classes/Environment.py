from __future__ import annotations

from Errors.RuntimeErrors import CannotAssignToConstant, UndefinedVariableError


class Environment:
    def __init__(self, parent: Environment | None = None):
        """
        Create a new Environment representing a variable scope, optionally nested under a parent scope.

        Initializes an empty `variables` mapping from variable name to a `(value, mutable)` tuple and stores the optional parent environment.

        Parameters:
            parent (Environment | None): Optional parent Environment that will be consulted for lookups and assignments when a name is not found in this scope. Defaults to `None`.
        """
        self.variables: dict[str, tuple[object, bool]] = {}
        self.parent = parent

    def define(self, name: str, value: object, mutable: bool = True) -> None:
        """
        Define a new variable in the current environment.

        Parameters:
                name (str): Variable name to create.
                value (object): Initial value to associate with the name.
                mutable (bool): Whether the variable may be reassigned after definition (defaults to True).

        Raises:
                CannotAssignToConstant: If a variable with the given name already exists in this environment.
        """
        if name in self.variables:
            raise CannotAssignToConstant(name)
        self.variables[name] = (value, mutable)

    def assign(self, name: str, value: object) -> None:
        """
        Assigns a new value to an existing variable in this environment or an enclosing parent.

        If the variable exists in the current environment, its mutability is checked; assignment replaces the stored value while preserving the variable's mutability. If the variable is not found locally, the assignment is delegated to the parent environment. If no enclosing environment defines the variable, an UndefinedVariableError is raised.

        Parameters:
            name (str): The variable name to assign.
            value (object): The new value to store for the variable.

        Raises:
            CannotAssignToConstant: If the variable exists locally and is not mutable.
            UndefinedVariableError: If the variable is not found in this environment or any parent.
        """
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
