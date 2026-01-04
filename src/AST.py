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


class IfStatement(ASTNode):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body


class Function(ASTNode):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body


class Function_Call(ASTNode):
    def __init__(self, name, parameters=None):
        self.name = name
        self.parameters = parameters


class RequestStatement(ASTNode):
    def __init__(self, value):
        self.value = value


class WhileLoop(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class ForeachLoop(ASTNode):
    def __init__(self, var_name, collection, body):
        self.var_name = var_name
        self.collection = collection
        self.body = body
