class ASTNode:
    pass

class VarDeclaration(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class VarReassignment(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class OutputStatement(ASTNode):
    def __init__(self, data):
        self.data = data

class Expression(ASTNode):
    def __init__(self, expression):
        self.expression = expression