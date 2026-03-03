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
from Lexer import Lexer
from Logger import get_logger
from Parser import Parser

logger = get_logger(__name__)


class Interpreter:
    def __init__(self, lexer: Lexer, parser: Parser):
        self.environment = Environment()
        self.parser = parser
        self.nodes = self.parser.nodes
        self.lexer = lexer

    def convert_input(self, value):
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            return value

    def eval_expression(self, expr, environment):
        if isinstance(expr, NumberLiteral):
            return expr.value
        if isinstance(expr, StringLiteral):
            return expr.value
        if isinstance(expr, BooleanLiteral):
            if expr.value == "true":
                return True
            elif expr.value == "false":
                return False
            elif expr.value == "null":
                return None
            else:
                raise ValueError(f"Invalid boolean value: {expr.value}")
        if isinstance(expr, Identifier):
            value = environment.get(expr.name)
            if isinstance(value, list) and len(value) == 2:
                return value[0]
            return value
        if isinstance(expr, BinaryExpression):
            left = self.eval_expression(expr.left, environment)
            right = self.eval_expression(expr.right, environment)

            if expr.operator == "+":
                try:
                    return left + right
                except TypeError:
                    if isinstance(right, tuple):
                        return (left + " ") + right[0]
                    elif isinstance(left, tuple):
                        return left[0] + (" " + right)
                    elif isinstance(left, str) and isinstance(right, str):
                        return left + " " + right
                    elif isinstance(left, tuple) and isinstance(right, tuple):
                        return left[0] + (" " + right[0])
                    elif isinstance(left, tuple) and isinstance(right, str):
                        return left[0] + (" " + right)
                    elif isinstance(left, str) and isinstance(right, tuple):
                        return left + (" " + right[0])
                    elif isinstance(left, tuple) and isinstance(right, tuple):
                        return left[0] + (" " + right[0])
            elif expr.operator == "-":
                return left - right
            elif expr.operator == "*":
                return left * right
            elif expr.operator == "/":
                return left / right
        if isinstance(expr, BooleanExpression):
            left = self.eval_expression(expr.left, environment)
            right = self.eval_expression(expr.right, environment)

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
            prompt = self.eval_expression(expr.value, environment)
            return self.convert_input(input(str(prompt)))
        if isinstance(expr, str):
            return expr
        if isinstance(expr, int) or isinstance(expr, float):
            return expr
        if isinstance(expr, bool):
            return expr

        raise InvalidBinaryOperation(expr, "UNKNOWN", None)

    global_environment = Environment()
    BREAK = object()

    def interpret_nodes(self, in_nodes, global_environment):
        """
        Execute a sequence of AST nodes in the given global environment.

        Processes each node in order, performing variable declarations and reassignments, printing outputs, evaluating conditionals, defining and calling functions, and running while/foreach loops. Side effects include mutating the provided environment and printing to stdout. Encountering a BreakStatement causes early exit and propagation of the break signal.

        Parameters:
            nodes (iterable): Sequence of AST node objects to execute.
            global_environment (Environment): The top-level Environment used as the parent scope for execution.

        Returns:
            The module-level BREAK sentinel if a BreakStatement was encountered and should propagate, otherwise None.
        """
        for node in in_nodes:
            # logger.debug("node=%r", node)
            if isinstance(node, BreakStatement):
                return self.BREAK
            if isinstance(node, VarDeclaration):
                if node.name in self.lexer.keywords:
                    raise CannotAssignToKeyword(node.name)

                global_environment.define(
                    node.name,
                    self.eval_expression(node.value, global_environment),
                    node.mutable,
                )
            elif isinstance(node, VarReassignment):
                global_environment.assign(
                    node.name, self.eval_expression(node.value, global_environment)
                )
            elif isinstance(node, OutputStatement):
                # print("Output statement called")
                # logger.debug(f"OutputStatement: {node.value}")
                print(self.eval_expression(node.value, global_environment))
            elif isinstance(node, IfStatement):
                result = None
                if self.eval_expression(node.condition, global_environment):
                    block_environment = Environment(parent=global_environment)
                    result = self.interpret_nodes(node.body, block_environment)
                elif node.else_body:
                    if isinstance(node.else_body, IfStatement):
                        result = self.interpret_nodes(
                            [node.else_body], global_environment
                        )
                    else:
                        block_environment = Environment(parent=global_environment)
                        result = self.interpret_nodes(node.else_body, block_environment)
                if result is self.BREAK:
                    return self.BREAK
            elif isinstance(node, Function):
                global_environment.define(node.name, node)
            elif isinstance(node, FunctionCall):
                function = global_environment.get(node.name)
                if not isinstance(function, Function):
                    raise NotCallableError(node.name)
                function_environment = Environment(parent=global_environment)
                self.interpret_nodes(function.body, function_environment)
            elif isinstance(node, WhileLoop):
                while self.eval_expression(node.condition, global_environment):
                    block_environment = Environment(parent=global_environment)
                    result = self.interpret_nodes(node.body, block_environment)
                    if result is self.BREAK:
                        break
            elif isinstance(node, ForeachLoop):
                collection = self.eval_expression(node.collection, global_environment)
                for item in collection:
                    block_environment = Environment(parent=global_environment)
                    block_environment.define(node.var_name, item)
                    result = self.interpret_nodes(node.body, block_environment)
                    if result is self.BREAK:
                        break
