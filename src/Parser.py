from Lexer import parsed_tokens
from AST import VarReassignment, VarDeclaration, OutputStatement
from src.TokenKind import TokenKind


def parse_let(tokens, index):
    token = tokens[index]
    if token.kind != TokenKind.KEYWORD or token.value != "let":
        raise Exception("Expected 'let'")

    index += 1
    token = tokens[index]
    if token.kind == TokenKind.KEYWORD:
        raise Exception("Expected identifier after 'let'")


    var_name = token.value
    index += 1
    token = tokens[index]
    if token.kind != TokenKind.SYMBOL or token.value != "=":
        raise Exception("Expected '=' after identifier")

    index += 1
    token = tokens[index]
    if token.kind != TokenKind.NUMBER:
        raise Exception("Expected number after '='")
    token = tokens[index]
    value = token.value
    index += 1

    if token.kind != TokenKind.SYMBOL or token.value != ";":
        raise Exception("Expected ';' at end of let statement")

    index += 1

    return VarDeclaration(var_name, value), index

def parse_res(tokens, index):
    if tokens[index][0] != "IDENTIFIER":
        raise Exception("Expected identifier after 'res'")

    var_name = tokens[index][1]
    index += 1

    if tokens[index] != ("SYMBOL", "="):
        raise Exception("Expected '=' after identifier")

    index += 1

    if tokens[index][0] != "NUMBER":
        raise Exception("Expected number after '='")

    value = tokens[index][1]
    index += 1

    if tokens[index] != ("SYMBOL", ";"):
        raise Exception("Expected ';' at end of let statement")

    index += 1

    return  VarReassignment(var_name, value), index

def parse_output(tokens, index):

    index += 1

    if tokens[index] != ("SYMBOL", "("):
        raise Exception("Expected '(' to begin output statement")

    output_data = tokens[index + 1]
    index += 1
   # print(f"Output data: {output_data}")

    if tokens[index + 1] != ("SYMBOL", ")"):
        raise Exception("Expected ')' at end of output statement")

    index += 1

    #print(f"Token: {tokens[index + 1]}")
    if tokens[index + 1] != ("SYMBOL", ";"):
        raise Exception("Expected ';' at end of output statement")

    index += 2

    return OutputStatement(output_data), index



index = 0
nodes = []

while index < len(parsed_tokens):
   # print(parsed_tokens[index])

    if parsed_tokens[index] == ('KEYWORD', 'let'):
        node, index = parse_let(parsed_tokens, index)
        nodes.append(node)
    elif parsed_tokens[index][0] == "IDENTIFIER":
        node, index = parse_res(parsed_tokens, index)
        nodes.append(node)
    elif parsed_tokens[index] == ("KEYWORD", "output"):
        node, index = parse_output(parsed_tokens, index)
        nodes.append(node)
    else:
        raise Exception(f"Unknown token: {parsed_tokens[index]}")

