from Lexer import parsed_tokens


def parse_let(tokens, index):
    if tokens[index][0] != "KEYWORD" or tokens[index][1] != "let":
        raise Exception("Expected 'let'")

    index += 1

    if tokens[index][0] != "IDENTIFIER":
        raise Exception("Expected identifier after 'let'")


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

    return {
        "type": "VarDeclaration",
        "name": var_name,
        "value": value,
    }, index

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

    return {
        "type": "VarReassignment",
        "name": var_name,
        "value": value,
    }, index


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
    else:
        raise Exception(f"Unknown token: {parsed_tokens[index]}")

