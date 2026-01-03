from Parser import nodes
from AST import VarDeclaration, VarReassignment, OutputStatement, NumberLiteral, StringLiteral, RequestStatement, Identifier, BinaryExpression, IfStatement, BooleanLiteral, BooleanExpression, Function, Function_Call, WhileLoop
from classes.Environment import Environment
from Errors.Errors import ZapError
from Errors.RuntimeErrors import UndefinedVariableError, InvalidAssignmentError, NotCallableError
from Errors.TypeErrors import InvalidBinaryOperation, InvalidFunctionArgumentType


def convert_input(value):
    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except:
        return value

def eval_expression(expr, environment):
    if isinstance(expr, NumberLiteral):
        return expr.value
    if isinstance(expr, StringLiteral):
        return expr.value
    if isinstance(expr, BooleanLiteral):
        return expr.value.lower() == "true"
    if isinstance(expr, Identifier):
        return environment.get(expr.name)
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
    if isinstance(expr, BooleanExpression):
        left = eval_expression(expr.left, environment)
        right = eval_expression(expr.right, environment)
        
        if expr.operator == "==":
            return left == right 
        elif expr.operator == "<":
            return left < right 
        elif expr.operator == ">":
            return left > right 
        elif expr.operator == "<=":
            return left <= right 
        elif expr.operator == ">=":
            return left >= right
        elif expr.operator == "!=":
            return left != right
        
    if isinstance(expr, RequestStatement):
        return convert_input(input(expr.value.value))
    if isinstance(expr, str):
        return expr
    if isinstance(expr, int) or isinstance(expr, float):
        return expr 
    if isinstance(expr, bool):
        return expr
    
    raise InvalidBinaryOperation(expr, "UNKNOWN", None)

global_environment = Environment()
def interpret_nodes(nodes, global_environment):
    for node in nodes:
        #print(node.value if hasattr(node, 'value') else node.name if hasattr(node, 'name') else type(node))
        if node == "break":
            return "BREAK"
        if isinstance(node, VarDeclaration):
            global_environment.define(node.name, eval_expression(node.value, global_environment))
        elif isinstance(node, VarReassignment):
            global_environment.assign(node.name, eval_expression(node.value, global_environment))
        elif isinstance(node, OutputStatement):
            print(eval_expression(node.value, global_environment))
        elif isinstance(node, IfStatement):
            result = None
            if eval_expression(node.condition, global_environment):
                block_environment = Environment(parent=global_environment)
                result = interpret_nodes(node.body, block_environment)
            elif node.else_body:
                if isinstance(node.else_body, IfStatement):
                    result = interpret_nodes([node.else_body], global_environment)
                else:
                    block_environment = Environment(parent=global_environment)
                    result = interpret_nodes(node.else_body, block_environment)
            if result == "BREAK":
                return "BREAK"
        elif isinstance(node, Function):
            global_environment.define(node.name, node)
        elif isinstance(node, Function_Call):
            function = global_environment.get(node.name)
            if not isinstance(function, Function):
                raise NotCallableError(node.name)
            function_environment = Environment(parent=global_environment)
            interpret_nodes(function.body, function_environment)
        elif isinstance(node, WhileLoop):
            while eval_expression(node.condition, global_environment):
                block_environment = Environment(parent=global_environment)
                result = interpret_nodes(node.body, block_environment)
                if result == "BREAK":
                    break

try:
    interpret_nodes(nodes, global_environment)
except ZapError as error:
    print(f"Zap runtime error:\n{error}")
#print(environment)