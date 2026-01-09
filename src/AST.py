from __future__ import annotations


class ASTNode:
    pass


class Statement(ASTNode):
    pass


class Expression(ASTNode):
    pass


class VarDeclaration(Statement):
    def __init__(self, name: str, value: Expression, mutable: bool = True):
        self.name = name
        self.value = value
        self.mutable = mutable


class VarReassignment(Statement):
    def __init__(self, name: str, value: Expression):
        self.name = name
        self.value = value


class OutputStatement(Statement):
    def __init__(self, value: Expression):
        self.value = value


class RequestStatement(Expression, Statement):
    def __init__(self, value: Expression):
        self.value = value


class Identifier(Expression):
    def __init__(self, name: str):
        self.name = name


class NumberLiteral(Expression):
    def __init__(self, value: int):
        self.value = value


class StringLiteral(Expression):
    def __init__(self, value: str):
        self.value = value


class BooleanLiteral(Expression):
    def __init__(self, value: bool):
        self.value = value


class BinaryExpression(Expression):
    def __init__(self, left: Expression, operator: str, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right


class BooleanExpression(Expression):
    def __init__(
        self,
        left: Expression | None,
        operator: str,
        right: Expression | None,
    ):
        self.left = left
        self.operator = operator
        self.right = right


class FunctionCall(Expression, Statement):
    def __init__(self, name: str, arguments: list[Expression] | None = None):
        self.name = name
        self.arguments = arguments


class IfStatement(Statement):
    def __init__(
        self,
        condition: Expression,
        body: list[Statement],
        else_body: list[Statement] | IfStatement | None = None,
    ):
        self.condition = condition
        self.body = body
        self.else_body = else_body


class WhileLoop(Statement):
    def __init__(self, condition: Expression, body: list[Statement]):
        self.condition = condition
        self.body = body


class ForeachLoop(Statement):
    def __init__(
        self,
        var_name: str,
        collection: Expression,
        body: list[Statement],
    ):
        self.var_name = var_name
        self.collection = collection
        self.body = body


class Function(Statement):
    def __init__(
        self,
        name: str,
        parameters: list[str],
        body: list[Statement],
    ):
        self.name = name
        self.parameters = parameters
        self.body = body


class BreakStatement(Statement):
    def __init__(self):
        pass
