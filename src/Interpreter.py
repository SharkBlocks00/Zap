from Parser import nodes
from AST import VarDeclaration, VarReassignment, OutputStatement, NumberLiteral, StringLiteral, Identifier, BinaryExpression, IfStatement, BooleanLiteral, BooleanExpression

def eval_expression(expr, environment):
    if isinstance(expr, NumberLiteral):
        return expr.value
    if isinstance(expr, StringLiteral):
        return expr.value
    if isinstance(expr, BooleanLiteral):
        value = expr.value[0].upper()
        value += expr.value[1:]
        expr.value = value 
        return expr.value == "True"
    if isinstance(expr, Identifier):
        if expr.name not in environment:
            raise Exception(f"Undefined variable {expr.name}")
        return environment[expr.name]
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
        

    raise Exception("Unknown operator type")

environment = {}
def interpret_nodes(nodes):
    for node in nodes:
    #print(node.name)
        if isinstance(node, VarDeclaration):
            environment[node.name] = eval_expression(node.value, environment)
        elif isinstance(node, VarReassignment):
            environment[node.name] = eval_expression(node.value, environment)
        elif isinstance(node, OutputStatement):
            print(eval_expression(node.value, environment))
        elif isinstance(node, IfStatement):
            condition_value = eval_expression(node.condition, environment)
            #print(f"If condition evaluated to: {condition_value}")
            if condition_value:
                for stmt in node.body:
                    if isinstance(stmt, VarDeclaration):
                        environment[stmt.name] = eval_expression(stmt.value, environment)
                    elif isinstance(stmt, VarReassignment):
                        environment[stmt.name] = eval_expression(stmt.value, environment)
                    elif isinstance(stmt, OutputStatement):
                        print(eval_expression(stmt.value, environment))
                    elif isinstance(stmt, IfStatement):
                        interpret_nodes([stmt])
            if node.else_body and not condition_value:
                for stmt in node.else_body:
                    if isinstance(stmt, VarDeclaration):
                        environment[stmt.name] = eval_expression(stmt.value, environment)
                    elif isinstance(stmt, VarReassignment):
                        environment[stmt.name] = eval_expression(stmt.value, environment)
                    elif isinstance(stmt, OutputStatement):
                        print(eval_expression(stmt.value, environment))
                    elif isinstance(stmt, IfStatement):
                        interpret_nodes([stmt])
interpret_nodes(nodes)

#print(environment)