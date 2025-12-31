from Lexer import parsed_tokens
from AST import BinaryExpression, VarReassignment, VarDeclaration, OutputStatement, NumberLiteral, StringLiteral, Identifier, Expression
from TokenKind import TokenKind

def parse_expression(tokens, index):
    left, index = parse_primary(tokens, index)

    while (index < len(tokens)and tokens[index].kind == TokenKind.SYMBOL and tokens[index].value in "+-*/"):
        operator = tokens[index].value
        right, index = parse_primary(tokens, index + 1)
        left = BinaryExpression(left, operator, right)

    return left, index


def parse_primary(tokens, index):
    token = tokens[index]

    if token.kind == TokenKind.NUMBER:
        return NumberLiteral(token.value), index + 1
    if token.kind == TokenKind.STRING:
        return StringLiteral(token.value), index + 1
    if token.kind == TokenKind.IDENTIFIER:
        return Identifier(token.value), index + 1

    if token.kind == TokenKind.SYMBOL and token.value == "(":
        expr, index = parse_expression(tokens, index + 1)

        if tokens[index].kind != TokenKind.SYMBOL or tokens[index].value != ")":
            raise Exception("Unexpected token")

        return expr, index 

    raise Exception("Unexpected token")    

def parse_let(tokens, index):
    #print(tokens[index])
    token = tokens[index]
    if token.kind != TokenKind.KEYWORD or token.value != "let":
        raise Exception("Expected 'let'")

    index += 1
    token = tokens[index]
    if token.kind == TokenKind.KEYWORD:
        raise Exception("Expected identifier after 'let'")


    var_name = token.value
    #print(f"Variable {var_name}")
    index += 1
    token = tokens[index]
    #print(f"Token: {token.kind}, Value: {token.value}")
    if token.kind != TokenKind.SYMBOL or token.value != "=":
        raise Exception("Expected '=' after identifier")

    index += 1
    value, index = parse_expression(tokens, index)

    token = tokens[index]
    #print(f"Token at end of let: {token.kind}, Value: {token.value}")
    if token.kind != TokenKind.SYMBOL or token.value != ";":
        raise Exception("Expected ';' at end of let statement")

    index += 1

    return VarDeclaration(var_name, value), index

def parse_res(tokens, index):
    token = tokens[index]
    if token.kind != TokenKind.IDENTIFIER:
        raise Exception("Expected identifier after 'res'")

    var_name = token.value
    index += 1
    token = tokens[index]

    if token.kind != TokenKind.SYMBOL or token.value != "=":
        raise Exception("Expected '=' after identifier")

    index += 1
    value, index = parse_expression(tokens, index)
    token = tokens[index]

    if token.kind != TokenKind.SYMBOL or token.value != ";":
        raise Exception("Expected ';' at end of let statement")

    index += 1

    return  VarReassignment(var_name, value), index

def parse_output(tokens, index):

    index += 1
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != "(":
        raise Exception("Expected '(' to begin output statement")

    index += 1
    token = tokens[index]
    output_data, index = parse_expression(tokens, index)
    token = tokens[index]
    #print(f"Token: {token.value}, TokenKind: {token.kind}")

    if token.kind != TokenKind.SYMBOL or token.value != ")":
        raise Exception("Expected a ')' to end output statement")
    
    index += 1
    token = tokens[index]

    #print(f"Token: {tokens[index + 1]}")
    if token.kind != TokenKind.SYMBOL or token.value != ";":
        raise Exception("Expected ';' at end of output statement")

    index += 1

    return OutputStatement(output_data), index



index = 0
nodes = []

while index < len(parsed_tokens):
    #print(f"Parsed tokens: {parsed_tokens}")
    #print(parsed_tokens[index].kind, parsed_tokens[index].value)
    token = parsed_tokens[index]
    if token.kind == TokenKind.KEYWORD and token.value == "let":
        node, index = parse_let(parsed_tokens, index)
        nodes.append(node)
    elif token.kind == TokenKind.IDENTIFIER:
       # print(f"Parsed identifier token: {parsed_tokens[index].value}")
        node, index = parse_res(parsed_tokens, index)
        nodes.append(node)
    elif token.kind == TokenKind.KEYWORD and token.value == "output":
        node, index = parse_output(parsed_tokens, index)
        nodes.append(node)
    else:
        raise Exception(f"Unknown token: {parsed_tokens[index]}")

