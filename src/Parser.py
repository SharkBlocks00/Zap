from Lexer import parsed_tokens
from AST import BinaryExpression, BooleanLiteral, VarReassignment, VarDeclaration, OutputStatement, RequestStatement, NumberLiteral, StringLiteral, IfStatement, Function, Identifier, Expression, BooleanExpression, Function_Call, WhileLoop
from TokenKind import TokenKind
from Errors.ParseErrors import UnexpectedTokenError, ExpectedTokenError, ParseError

def parse_statement(tokens, index): 
    # print(f"Parsing statement at index {index}: TokenKind={tokens[index].kind}, Value={tokens[index].value}")
    # for token in tokens:
    #     print(f"TokenKind: {token.kind}, Value: {token.value}")
    token = tokens[index]
    if token.kind == TokenKind.KEYWORD and token.value == "let":
        node, index = parse_let(parsed_tokens, index)
    elif token.kind == TokenKind.IDENTIFIER and tokens[index + 1].kind == TokenKind.SYMBOL and tokens[index + 1].value == "(":
        node, index - parse_function(parsed_tokens, index)
    elif token.kind == TokenKind.IDENTIFIER:
       #print(f"Parsed identifier token: {parsed_tokens[index].value}")
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
    elif token.kind == TokenKind.FUNCTION_CALL: 
        node, index = parse_function_call(parsed_tokens, index)
    elif token.kind == TokenKind.KEYWORD and token.value == "request":
        node, index = parse_request(parsed_tokens, index)
        #print(f"Parsed request statement: {node.value.value}")
    elif token.kind == TokenKind.KEYWORD and token.value == "while":
        node, index = parse_while(parsed_tokens, index)
    elif token.kind == TokenKind.KEYWORD and token.value == "break":
        index += 1
        token = tokens[index]
        if token.kind != TokenKind.SYMBOL or token.value != ";":
            raise ExpectedTokenError(";", token.value if token else "end of input")
        index += 1
        node = "break"
    else:
        raise UnexpectedTokenError(parsed_tokens[index].value)
    return node, index

def parse_expression(tokens, index):
    return parse_comparison(tokens, index)

def parse_addition(tokens, index):
    left, index = parse_multiplication(tokens, index)

    while (index < len(tokens) and tokens[index].kind == TokenKind.SYMBOL and tokens[index].value in "+-"):
        operator = tokens[index].value
        right, index = parse_multiplication(tokens, index + 1)
        left = BinaryExpression(left, operator, right)

    return left, index

def parse_multiplication(tokens, index):
    left, index = parse_primary(tokens, index)

    while ( index < len(tokens) and tokens[index].kind == TokenKind.SYMBOL and tokens[index].value in "*/"):
        operator = tokens[index].value
        right, index = parse_primary(tokens, index + 1)
        left = BinaryExpression(left, operator, right)

    return left, index

def parse_comparison(tokens, index):
    left, index = parse_addition(tokens, index)

    while (index < len(tokens) and tokens[index].kind == TokenKind.SYMBOL and tokens[index].value in ["==", "!=", "<", ">", "<=", ">="]):
        operator = tokens[index].value
        right, index = parse_addition(tokens, index + 1)
        left = BooleanExpression(left, operator, right)

    return left, index


def parse_primary(tokens, index):
    #print(f"Debug: Token before: {tokens[index-1].value if index > 0 else 'None'}, Current: {tokens[index].value}, Next: {tokens[index+1].value if index + 1 < len(tokens) else 'None'}")
    token = tokens[index]

    if token.kind == TokenKind.NUMBER:
        return NumberLiteral(token.value), index + 1
    if token.kind == TokenKind.BOOLEAN:
        return BooleanLiteral(token.value), index + 1
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

def parse_let(tokens, index):
    #print(tokens[index])
    token = tokens[index]
    if token.kind != TokenKind.KEYWORD or token.value != "let":
        raise ExpectedTokenError("let", token.value if token else "end of input")

    index += 1
    token = tokens[index]
    if token.kind != TokenKind.IDENTIFIER:
        raise ExpectedTokenError("identifier", token.value)


    var_name = token.value
    #print(f"Variable {var_name}")
    index += 1
    token = tokens[index]
    #print(f"Token: {token.kind}, Value: {token.value}")
    if token.kind != TokenKind.SYMBOL or token.value != "=":
        raise ExpectedTokenError("=", token.value)

    index += 1 
    value, index = parse_expression(tokens, index)

    #print(f"Parsed value for variable '{var_name}': {value}")
    #print(f"Token: {tokens[index].kind}, Value: {tokens[index].value}")
    token = tokens[index]
    #print(f"Token at end of let: {token.kind}, Value: {token.value}")
    if token.kind != TokenKind.SYMBOL or token.value != ";":
        raise ExpectedTokenError(";", token.value)

    index += 1

    return VarDeclaration(var_name, value), index

def parse_res(tokens, index):
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

    return  VarReassignment(var_name, value), index

def parse_output(tokens, index):

    index += 1
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != "(":
        raise ExpectedTokenError("(", token.value if token else "end of input")

    index += 1
    token = tokens[index]
    #print(f"Token at start of output expression: {token.value}, TokenKind: {token.kind}")
    output_data, index = parse_expression(tokens, index)
    #print(f"Output data parsed: {output_data}")
    token = tokens[index]
    #print(f"Token: {token.value}, TokenKind: {token.kind}")

    if token.kind != TokenKind.SYMBOL or token.value != ")":
        raise ExpectedTokenError(")", token.value if token else "end of input")
    
    index += 1
    token = tokens[index]

    #print(f"Token: {tokens[index + 1]}")
    if token.kind != TokenKind.SYMBOL or token.value != ";":
        raise ExpectedTokenError(";", token.value if token else "end of input")

    index += 1

    return OutputStatement(output_data), index

def parse_request(tokens, index):
    index += 1
    #print(f"Tokens: {tokens[index+1:]}")
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
    return RequestStatement(request_data), index

def parse_while(tokens, index):
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
    return WhileLoop(condition, body_nodes), index

def parse_if(tokens, index):
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


    if index < len(tokens) and tokens[index].kind == TokenKind.KEYWORD and tokens[index].value == "elseif":
        else_branch, index = parse_if(tokens, index)
        return IfStatement(condition, body_nodes, else_branch), index

    elif index < len(tokens) and tokens[index].kind == TokenKind.KEYWORD and tokens[index].value == "else":
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
        return IfStatement(condition, body_nodes, else_branch), index
    return IfStatement(condition, body_nodes, None), index

def parse_function(tokens, index):
    #print(f"Parsing function at index {index}: TokenKind={tokens[index].kind}, Value={tokens[index].value}")
    index += 1
    try:
        token = tokens[index]
    except IndexError:
        raise ParseError("Unexpected end of input while parsing function")
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

def parse_function_call(tokens, index):
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
    return Function_Call(function_name), index

index = 0
nodes = []

while index < len(parsed_tokens):
    #print(f"Parsed tokens: {parsed_tokens}")
    #print(parsed_tokens[index].kind, parsed_tokens[index].value)
    node, index = parse_statement(parsed_tokens, index)
    nodes.append(node)