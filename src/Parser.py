from Lexer import parsed_tokens
from AST import VarReassignment, VarDeclaration, OutputStatement
from src.TokenKind import TokenKind


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
    token = tokens[index]
    #print(f"Token: {token.kind}")
    if token.kind != TokenKind.NUMBER and token.kind != TokenKind.STRING:
        raise Exception("Expected value after '='")
    token = tokens[index]
    value = token.value
    index += 1
    #print(f"Value: {value}")

    token = tokens[index]
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
    token = tokens[index]
    if token.kind != TokenKind.NUMBER and token.kind != TokenKind.STRING:
        raise Exception(f"Expected value after '='. Token: {token.value}, TokenKind: {token.kind}")

    value = token.value
    index += 1
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
    output_data = token.value
    #print(f"Output: {output_data}")
    index += 1
    token = tokens[index]
   # print(f"Output data: {output_data}")

    if token.kind != TokenKind.SYMBOL or token.value != ")":
        raise Exception("Expected ')' at end of output statement")

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

