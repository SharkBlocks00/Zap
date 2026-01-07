from typing import TypeAlias

from AST import (
    BinaryExpression,
    BooleanExpression,
    BooleanLiteral,
    Expression,
    ForeachLoop,
    Function,
    FunctionCall,
    Identifier,
    IfStatement,
    NumberLiteral,
    OutputStatement,
    RequestStatement,
    Statement,
    StringLiteral,
    VarDeclaration,
    VarReassignment,
    WhileLoop,
)
from Errors.ParseErrors import ExpectedTokenError, ParseError, UnexpectedTokenError
from Lexer import parsed_tokens
from Logger import get_logger
from Token import Token
from TokenKind import TokenKind

logger = get_logger(__name__)

# unions so everything is wayyy cleaner in return signatures instead of a wall of text in every function definition
ASTExpression: TypeAlias = Expression

ASTStatement: TypeAlias = Statement | None | str


def parse_statement(tokens: list[Token], index: int) -> tuple[ASTStatement, int]:
    # logger.debug(
    #     f"Parsing statement at index {index}: TokenKind={tokens[index].kind}, Value={tokens[index].value}"
    # )
    # for token in tokens:
    #     logger.debug(f"TokenKind: {token.kind}, Value: {token.value}")
    token = tokens[index]
    node: ASTStatement = None  # see coz if we didnt have ASTStatement we would have to do a bunch of type checks

    if token.kind == TokenKind.KEYWORD and token.value == "let":
        node, index = parse_let(parsed_tokens, index)
    elif (
        token.kind == TokenKind.IDENTIFIER
        and tokens[index + 1].kind == TokenKind.SYMBOL
        and tokens[index + 1].value == "("
    ):
        node, index = parse_function(parsed_tokens, index)
    elif token.kind == TokenKind.KEYWORD and token.value == "const":
        node, index = parse_const(parsed_tokens, index)
    elif token.kind == TokenKind.IDENTIFIER:
        # logger.debug(f"Parsed identifier token: {parsed_tokens[index].value}")
        node, index = parse_res(parsed_tokens, index)
    elif token.kind == TokenKind.KEYWORD and token.value == "output":
        node, index = parse_output(parsed_tokens, index)
    elif token.kind == TokenKind.KEYWORD and token.value == "if":
        node, index = parse_if(parsed_tokens, index)
    elif token.kind == TokenKind.KEYWORD and token.value == "elseif":
        raise UnexpectedTokenError("elseif")
    elif token.kind == TokenKind.KEYWORD and token.value == "else":
        raise UnexpectedTokenError("else")
    elif token.kind == TokenKind.KEYWORD and token.value == "func":
        node, index = parse_function(parsed_tokens, index)
    elif token.kind == TokenKind.KEYWORD and token.value == "define":
        raise UnexpectedTokenError("define")
    elif token.kind == TokenKind.FunctionCall:
        node, index = parse_FunctionCall(parsed_tokens, index)
    elif token.kind == TokenKind.KEYWORD and token.value == "request":
        node, index = parse_request(parsed_tokens, index)
        # logger.debug(f"Parsed request statement: {node.value.value}")
    elif token.kind == TokenKind.KEYWORD and token.value == "while":
        node, index = parse_while(parsed_tokens, index)
    elif token.kind == TokenKind.KEYWORD and token.value == "break":
        index += 1
        token = tokens[index]
        if token.kind != TokenKind.SYMBOL or token.value != ";":
            raise ExpectedTokenError(";", token.value if token else "end of input")
        index += 1
        node = "break"
    elif token.kind == TokenKind.KEYWORD and token.value == "foreach":
        node, index = parse_foreach(parsed_tokens, index)
    else:
        raise UnexpectedTokenError(parsed_tokens[index].value)
    return node, index


def parse_expression(tokens: list[Token], index: int) -> tuple[Expression | None, int]:
    return parse_comparison(tokens, index)


def parse_addition(tokens: list[Token], index: int) -> tuple[Expression | None, int]:
    left, index = parse_multiplication(tokens, index)

    while (
        index < len(tokens)
        and tokens[index].kind == TokenKind.SYMBOL
        and tokens[index].value in "+-"
    ):
        operator = tokens[index].value
        right, index = parse_multiplication(tokens, index + 1)
        assert left is not None  # doing this to make the type checker happy
        assert right is not None
        left = BinaryExpression(left, operator, right)

    return left, index


def parse_multiplication(
    tokens: list[Token], index: int
) -> tuple[Expression | None, int]:
    left, index = parse_primary(tokens, index)

    while (
        index < len(tokens)
        and tokens[index].kind == TokenKind.SYMBOL
        and tokens[index].value in "*/"
    ):
        operator = tokens[index].value
        right, index = parse_primary(tokens, index + 1)
        assert left is not None
        assert right is not None
        left = BinaryExpression(left, operator, right)

    return left, index


def parse_comparison(tokens: list[Token], index: int) -> tuple[Expression | None, int]:
    left, index = parse_addition(tokens, index)
    while (
        index < len(tokens)
        and tokens[index].kind == TokenKind.SYMBOL
        and tokens[index].value in ["==", "!=", "<", ">", "<=", ">=", "&&", "||"]
    ):
        # logger.debug(f"Token: {tokens[index].value}")
        operator = tokens[index].value
        right, index = parse_addition(tokens, index + 1)
        left = BooleanExpression(left, operator, right)

    return left, index


def parse_primary(tokens: list[Token], index: int) -> tuple[Expression | None, int]:
    # logger.debug(f"Token before: {tokens[index-1].value if index > 0 else 'None'}, Current: {tokens[index].value}, Next: {tokens[index+1].value if index + 1 < len(tokens) else 'None'}")
    token = tokens[index]

    if token.kind == TokenKind.NUMBER:
        return NumberLiteral(int(token.value)), index + 1
    if token.kind == TokenKind.BOOLEAN:
        return BooleanLiteral(bool(token.value)), index + 1
    if token.kind == TokenKind.STRING:
        return StringLiteral(token.value), index + 1
    if token.kind == TokenKind.IDENTIFIER:
        return Identifier(token.value), index + 1

    if token.kind == TokenKind.KEYWORD and token.value == "request":
        return parse_request(tokens, index)

    if token.kind == TokenKind.SYMBOL and token.value == "(":
        expr, index = parse_expression(tokens, index + 1)

        if tokens[index].kind != TokenKind.SYMBOL or tokens[index].value != ")":
            raise UnexpectedTokenError(tokens[index].value)

        return expr, index

    raise UnexpectedTokenError(token.value)


def parse_let(tokens: list[Token], index: int) -> tuple[VarDeclaration, int]:
    # logger.debug(tokens[index])
    token = tokens[index]
    if token.kind != TokenKind.KEYWORD or token.value != "let":
        raise ExpectedTokenError("let", token.value if token else "end of input")

    index += 1
    token = tokens[index]
    if token.kind != TokenKind.IDENTIFIER:
        raise ExpectedTokenError("identifier", token.value)

    var_name = token.value
    # logger.debug(f"Variable {var_name}")
    index += 1
    token = tokens[index]
    # logger.debug(f"Token: {token.kind}, Value: {token.value}")
    if token.kind != TokenKind.SYMBOL or token.value != "=":
        raise ExpectedTokenError("=", token.value)

    index += 1
    value, index = parse_expression(tokens, index)

    # logger.debug(f"Parsed value for variable '{var_name}': {value}")
    # logger.debug(f"Token: {tokens[index].kind}, Value: {tokens[index].value}")
    token = tokens[index]
    # logger.debug(f"Token at end of let: {token.kind}, Value: {token.value}")
    if token.kind != TokenKind.SYMBOL or token.value != ";":
        raise ExpectedTokenError(";", token.value)

    index += 1
    assert value is not None
    return VarDeclaration(var_name, value), index


def parse_const(tokens: list[Token], index: int) -> tuple[VarDeclaration, int]:
    index += 1
    token = tokens[index]
    if token.kind != TokenKind.IDENTIFIER:
        raise ExpectedTokenError("identifier", token.value)

    var_name = token.value
    index += 1
    token = tokens[index]

    if token.kind != TokenKind.SYMBOL or token.value != "=":
        raise ExpectedTokenError("=", token.value)

    index += 1
    value, index = parse_expression(tokens, index)
    assert value is not None
    #logger.debug(f"Parsed value for constant '{var_name}': {value}")
    index += 1
    return VarDeclaration(var_name, value, mutable=False), index


def parse_res(tokens: list[Token], index: int) -> tuple[VarReassignment, int]:
    token = tokens[index]
    if token.kind != TokenKind.IDENTIFIER:
        raise ExpectedTokenError("identifier", token.value)

    var_name = token.value
    index += 1
    token = tokens[index]

    if token.kind != TokenKind.SYMBOL or token.value != "=":
        raise ExpectedTokenError("=", token.value)

    index += 1
    value, index = parse_expression(tokens, index)
    token = tokens[index]

    if token.kind != TokenKind.SYMBOL or token.value != ";":
        raise ExpectedTokenError(";", token.value)

    index += 1
    assert value is not None
    return VarReassignment(var_name, value), index


def parse_output(tokens: list[Token], index: int) -> tuple[OutputStatement, int]:
    index += 1
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != "(":
        raise ExpectedTokenError("(", token.value if token else "end of input")

    index += 1
    token = tokens[index]
    # logger.debug(f"Token at start of output expression: {token.value}, TokenKind: {token.kind}")
    output_data, index = parse_expression(tokens, index)
    # logger.debug(f"Output data parsed: {output_data}")
    token = tokens[index]
    # logger.debug(f"Token: {token.value}, TokenKind: {token.kind}")

    if token.kind != TokenKind.SYMBOL or token.value != ")":
        raise ExpectedTokenError(")", token.value if token else "end of input")

    index += 1
    token = tokens[index]

    # logger.debug(f"Token: {tokens[index + 1]}")
    if token.kind != TokenKind.SYMBOL or token.value != ";":
        raise ExpectedTokenError(";", token.value if token else "end of input")

    index += 1
    assert output_data is not None
    return OutputStatement(output_data), index


def parse_request(tokens: list[Token], index: int) -> tuple[RequestStatement, int]:
    index += 1
    # logger.debug(f"Tokens: {tokens[index+1:]}")
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != "(":
        raise ExpectedTokenError("(", token.value if token else "end of input")
    index += 1
    token = tokens[index]
    request_data, index = parse_expression(tokens, index)
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != ")":
        raise ExpectedTokenError(")", token.value if token else "end of input")
    index += 1
    assert request_data is not None
    return RequestStatement(request_data), index


def parse_while(tokens: list[Token], index: int) -> tuple[WhileLoop, int]:
    index += 1
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != "(":
        raise ExpectedTokenError("(", token.value if token else "end of input")
    index += 1
    token = tokens[index]
    condition, index = parse_expression(tokens, index)
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != ")":
        raise ExpectedTokenError(")", token.value if token else "end of input")
    index += 1
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != "{":
        raise ExpectedTokenError("{", token.value if token else "end of input")
    index += 1
    body_nodes = []
    token = tokens[index]

    while token.value != "}":
        stmt, index = parse_statement(tokens, index)
        body_nodes.append(stmt)
        token = tokens[index]
    index += 1
    assert condition is not None
    return WhileLoop(condition, body_nodes), index


def parse_foreach(tokens: list[Token], index: int) -> tuple[ForeachLoop, int]:
    index += 1
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != "(":
        raise ExpectedTokenError("(", token.value if token else "end of input")
    index += 1
    token = tokens[index]
    var_name = token.value
    index += 1
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != ":":
        raise ExpectedTokenError(":", token.value if token else "end of input")
    index += 1
    token = tokens[index]
    collection, index = parse_expression(tokens, index)
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != ")":
        raise ExpectedTokenError(")", token.value if token else "end of input")
    index += 1
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != "{":
        raise ExpectedTokenError("{", token.value if token else "end of input")
    index += 1
    body_nodes = []
    token = tokens[index]

    while token.value != "}":
        stmt, index = parse_statement(tokens, index)
        body_nodes.append(stmt)
        token = tokens[index]
    index += 1
    assert collection is not None
    return ForeachLoop(var_name, collection, body_nodes), index


def parse_if(tokens: list[Token], index: int) -> tuple[IfStatement, int]:
    index += 1
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != "(":
        raise ExpectedTokenError("(", token.value if token else "end of input")

    index += 1
    token = tokens[index]
    condition, index = parse_expression(tokens, index)

    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != ")":
        raise ExpectedTokenError(")", token.value if token else "end of input")
    index += 1
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != "{":
        raise ExpectedTokenError("{", token.value if token else "end of input")
    index += 1
    body_nodes = []
    token = tokens[index]

    while token.value != "}":
        stmt, index = parse_statement(tokens, index)
        body_nodes.append(stmt)
        token = tokens[index]
    index += 1

    else_branch = None

    if (
        index < len(tokens)
        and tokens[index].kind == TokenKind.KEYWORD
        and tokens[index].value == "elseif"
    ):
        else_branch, index = parse_if(tokens, index)
        assert condition is not None
        return IfStatement(condition, body_nodes, else_branch), index

    elif (
        index < len(tokens)
        and tokens[index].kind == TokenKind.KEYWORD
        and tokens[index].value == "else"
    ):
        index += 1
        token = tokens[index]
        if token.kind != TokenKind.SYMBOL or token.value != "{":
            raise ExpectedTokenError("{", token.value if token else "end of input")
        index += 1
        else_body = []
        token = tokens[index]

        while token.value != "}":
            stmt, index = parse_statement(tokens, index)
            else_body.append(stmt)
            token = tokens[index]
        index += 1
        else_branch = else_body
        assert condition is not None
        return IfStatement(condition, body_nodes, else_branch), index
    assert condition is not None
    return IfStatement(condition, body_nodes, None), index


def parse_function(tokens: list[Token], index: int) -> tuple[Function, int]:
    # logger.debug(f"Parsing function at index {index}: TokenKind={tokens[index].kind}, Value={tokens[index].value}")
    index += 1
    try:
        token = tokens[index]
    except IndexError:
        raise ParseError("Unexpected end of input while parsing function") from None
    if token.kind != TokenKind.IDENTIFIER:
        raise ExpectedTokenError("identifier", token.value if token else "end of input")
    func_name = token.value
    index += 1
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != "=":
        raise ExpectedTokenError("=", token.value if token else "end of input")

    index += 1
    token = tokens[index]
    if token.kind != TokenKind.KEYWORD or token.value != "define":
        raise ExpectedTokenError("define", token.value if token else "end of input")
    index += 1
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != "(":
        raise ExpectedTokenError("(", token.value if token else "end of input")
    index += 1
    # TODO LATER: Allow paramaters
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != ")":
        raise ExpectedTokenError(")", token.value if token else "end of input")
    index += 1
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != "{":
        raise ExpectedTokenError("{", token.value if token else "end of input")
    index += 1
    body_nodes = []
    token = tokens[index]
    while token.value != "}":
        stmt, index = parse_statement(tokens, index)
        body_nodes.append(stmt)
        token = tokens[index]
    index += 1
    return Function(func_name, [], body_nodes), index


def parse_FunctionCall(tokens: list[Token], index: int) -> tuple[FunctionCall, int]:
    token = tokens[index]
    function_name = token.value
    index += 1
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != "(":
        raise ExpectedTokenError("(", token.value if token else "end of input")
    index += 1
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != ")":
        raise ExpectedTokenError(")", token.value if token else "end of input")
    index += 1
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != ";":
        raise ExpectedTokenError(";", token.value if token else "end of input")
    index += 1
    return FunctionCall(function_name), index


index = 0
nodes: list[ASTStatement] = []

while index < len(parsed_tokens):
    # logger.debug(f"Parsed tokens: {parsed_tokens}")
    # logger.debug(parsed_tokens[index].kind, parsed_tokens[index].value)
    node, index = parse_statement(parsed_tokens, index)
    nodes.append(node)
