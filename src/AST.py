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
    def __init__(self, value):
        self.value = value

class Expression(ASTNode):
    def __init__(self, expression):
        self.expression = expression

class BinaryExpression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class NumberLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

class StringLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class BooleanLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

class BooleanExpression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right