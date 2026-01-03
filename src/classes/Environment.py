from Errors.RuntimeErrors import UndefinedVariableError

class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent 

    def define(self, name, value):
        self.variables[name] = value 

    def assign(self, name, value):
        if name in self.variables:
            self.variables[name] = value
        elif self.parent:
            self.parent.assign(name, value)
        else:
            raise UndefinedVariableError(name)
    
    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise UndefinedVariableError(name)
