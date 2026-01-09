from AST import (
    BinaryExpression,
    BooleanExpression,
    BooleanLiteral,
    BreakStatement,
    ForeachLoop,
    Function,
    FunctionCall,
    Identifier,
    IfStatement,
    NumberLiteral,
    OutputStatement,
    RequestStatement,
    StringLiteral,
    VarDeclaration,
    VarReassignment,
    WhileLoop,
)
from classes.Environment import Environment
from Errors.Errors import ZapError
from Errors.RuntimeErrors import CannotAssignToKeyword, NotCallableError
from Errors.TypeErrors import InvalidBinaryOperation
from Lexer import keywords
from Logger import get_logger
from Parser import nodes

logger = get_logger(__name__)


def convert_input(value):
    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except ValueError:
        return value


def eval_expression(expr, environment):
    if isinstance(expr, NumberLiteral):
        return expr.value
    if isinstance(expr, StringLiteral):
        return expr.value
    if isinstance(expr, BooleanLiteral):
        return expr.value
    if isinstance(expr, Identifier):
        value = environment.get(expr.name)
        if isinstance(value, list) and len(value) == 2:
            return value[0]
        return value
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
        elif expr.operator == "&&":
            return left and right
        elif expr.operator == "||":
            return left or right

    if isinstance(expr, RequestStatement):
        prompt = eval_expression(expr.value, environment)
        return convert_input(input(str(prompt)))
    if isinstance(expr, str):
        return expr
    if isinstance(expr, int) or isinstance(expr, float):
        return expr
    if isinstance(expr, bool):
        return expr

    raise InvalidBinaryOperation(expr, "UNKNOWN", None)


global_environment = Environment()


def interpret_nodes(nodes, global_environment):
    """
    Interpret a sequence of AST nodes within the given environment, executing side-effecting statements and managing nested scopes.
    
    This function walks the provided nodes in order, evaluating and executing each node according to its kind (variable declarations and reassignment, output, conditionals, function definitions and calls, while and foreach loops, and break handling). It creates new child environments for block scopes (if/else bodies, loop iterations, and function bodies) so that declarations inside those blocks do not leak into the provided global environment. When a BreakStatement is encountered inside the current or any nested block, the function propagates a sentinel return value to signal the break to the caller.
    
    Parameters:
        nodes (Iterable[ASTNode]): Sequence of AST nodes to interpret.
        global_environment (Environment): The environment used as the surrounding scope for interpretation; child environments are created for block scopes.
    
    Returns:
        str or None: The string "BREAK" if a BreakStatement was encountered and propagated out of the interpreted node sequence, otherwise None.
    """
    for node in nodes:
        logger.debug(
            node.value
            if hasattr(node, "value")
            else node.name
            if hasattr(node, "name")
            else type(node)
        )
        if isinstance(node, BreakStatement):
            return "BREAK"
        if isinstance(node, VarDeclaration):
            if node.name in keywords:
                raise CannotAssignToKeyword(node.name)

            global_environment.define(
                node.name, eval_expression(node.value, global_environment), node.mutable
            )
        elif isinstance(node, VarReassignment):
            global_environment.assign(
                node.name, eval_expression(node.value, global_environment)
            )
        elif isinstance(node, OutputStatement):
            # logger.debug(f"OutputStatement: {node.value}")
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
        elif isinstance(node, FunctionCall):
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
        elif isinstance(node, ForeachLoop):
            collection = eval_expression(node.collection, global_environment)
            for item in collection:
                block_environment = Environment(parent=global_environment)
                block_environment.define(node.var_name, item)
                result = interpret_nodes(node.body, block_environment)
                if result == "BREAK":
                    break


try:
    interpret_nodes(nodes, global_environment)
except ZapError as error:
    print(f"Zap {error.__class__.__name__}:\n{error}")
# logger.debug(global_environment)