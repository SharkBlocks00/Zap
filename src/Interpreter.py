from Parser import nodes
from AST import VarDeclaration, VarReassignment, OutputStatement, NumberLiteral, StringLiteral, Identifier, BinaryExpression

def eval_expression(expr, environment):
    if isinstance(expr, NumberLiteral):
        return expr.value
    if isinstance(expr, StringLiteral):
        return expr.value
    if isinstance(expr, Identifier):
        if expr.name not in environment:
            raise Exception(f"Undefined variable {expr.name}")
        return environment[expr.name]
    if isinstance(expr, BinaryExpression):
        left = eval_expression(expr.left, environment)
        right = eval_expression(expr.right, environment)

        if expr.operator == "+":
            return left + right 
        elif expr.operator == "-":
            return left - right
        elif expr.operator == "*":
            return left * right
        elif expr.operator == "/":
            return left / right
    raise Exception("Unknown operator type")


environment = {}
for node in nodes:
    #print(node.name)
    if isinstance(node, VarDeclaration):
        environment[node.name] = eval_expression(node.value, environment)
    elif isinstance(node, VarReassignment):
        environment[node.name] = eval_expression(node.value, environment)
    elif isinstance(node, OutputStatement):
        print(eval_expression(node.value, environment))


print(environment)