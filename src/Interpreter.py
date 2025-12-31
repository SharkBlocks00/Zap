from Parser import nodes
from AST import VarDeclaration, VarReassignment, OutputStatement

environment = {}
for node in nodes:
    #print(node.name)
    if isinstance(node, VarDeclaration):
        environment[node.name] = node.value
    elif isinstance(node, VarReassignment):
        try:
            variable = environment[node.name]
        except KeyError:
            raise KeyError(f"Variable {node.name} not found")

        environment[node.name] = node.value
    elif isinstance(node, OutputStatement):
        print(node.value)


print(environment)