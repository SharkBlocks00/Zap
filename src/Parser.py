from types import NoneType
from typing import TypeAlias

from AST import (
    AssertStatement,
    BinaryExpression,
    BooleanExpression,
    BooleanLiteral,
    BreakStatement,
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
from Errors.RuntimeErrors import InvalidAssertStatementError
from Lexer import Lexer
from Logger import get_logger
from Token import Token
from TokenKind import TokenKind

logger = get_logger(__name__)

# unions so everything is wayyy cleaner in return signatures instead of a wall of text in every function definition
ASTExpression: TypeAlias = Expression

ASTStatement: TypeAlias = Statement | None | str


class Parser:
    def __init__(self, source: str, lexer: Lexer):
        self.lexer = lexer
        self.tokens = self.lexer.lexate(source)
        self.index = 0
        self.nodes = []

    def parse_statement(
        self, tokens: list[Token], index: int
    ) -> tuple[ASTStatement, int]:
        # logger.debug(
        #     f"Parsing statement at index {index}: TokenKind={tokens[index].kind}, Value={tokens[index].value}"
        # )
        # for token in tokens:
        #     logger.debug(f"TokenKind: {token.kind}, Value: {token.value}")
        """
        Parse a single statement beginning at the given token index and produce its AST node and the next token position.

        Parameters:
            tokens (list[Token]): The token list to parse from.
            index (int): The current position in `tokens` to start parsing.

        Returns:
            tuple[ASTStatement, int]: `(node, index)` where `node` is the parsed statement AST node (or `None` for empty/no-op statements) and `index` is the token position immediately after the parsed statement.

        Raises:
            UnexpectedTokenError: If the token at `index` is not a valid statement start or an unexpected keyword is encountered.
        """
        token = tokens[index]
        node: ASTStatement = None  # see coz if we didnt have ASTStatement we would have to do a bunch of type checks

        if token.kind == TokenKind.KEYWORD and token.value == "let":
            node, index = self.parse_let(self.tokens, index)
        elif (
            token.kind == TokenKind.IDENTIFIER
            and tokens[index + 1].kind == TokenKind.SYMBOL
            and tokens[index + 1].value == "("
        ):
            node, index = self.parse_function(self.tokens, index)
        elif token.kind == TokenKind.KEYWORD and token.value == "const":
            node, index = self.parse_const(self.tokens, index)
        elif token.kind == TokenKind.IDENTIFIER:
            # logger.debug(f"Parsed identifier token: {parsed_tokens[index].value}")
            node, index = self.parse_res(self.tokens, index)
        elif token.kind == TokenKind.KEYWORD and token.value == "output":
            node, index = self.parse_output(self.tokens, index)
        elif token.kind == TokenKind.KEYWORD and token.value == "if":
            node, index = self.parse_if(self.tokens, index)
        elif token.kind == TokenKind.KEYWORD and token.value == "elseif":
            raise UnexpectedTokenError("elseif")
        elif token.kind == TokenKind.KEYWORD and token.value == "else":
            raise UnexpectedTokenError("else")
        elif token.kind == TokenKind.KEYWORD and token.value == "func":
            node, index = self.parse_function(self.tokens, index)
        elif token.kind == TokenKind.KEYWORD and token.value == "define":
            raise UnexpectedTokenError("define")
        elif token.kind == TokenKind.FunctionCall:
            node, index = self.parse_FunctionCall(self.tokens, index)
        elif token.kind == TokenKind.KEYWORD and token.value == "request":
            node, index = self.parse_request(self.tokens, index)
            # logger.debug(f"Parsed request statement: {node.value.value}")
        elif token.kind == TokenKind.KEYWORD and token.value == "while":
            node, index = self.parse_while(self.tokens, index)
        elif token.kind == TokenKind.BREAK:
            node, index = self.parse_Break(self.tokens, index)
        elif token.kind == TokenKind.KEYWORD and token.value == "foreach":
            node, index = self.parse_foreach(self.tokens, index)
        elif token.kind == TokenKind.KEYWORD and token.value == "assert":
            node, index = self.parse_assert(self.tokens, index)
        else:
            raise UnexpectedTokenError(tokens[index].value)
        return node, index

    def parse_expression(
        self, tokens: list[Token], index: int
    ) -> tuple[Expression | None, int]:
        return self.parse_comparison(tokens, index)

    def parse_addition(
        self, tokens: list[Token], index: int
    ) -> tuple[Expression | None, int]:
        left, index = self.parse_multiplication(tokens, index)

        while (
            index < len(tokens)
            and tokens[index].kind == TokenKind.SYMBOL
            and tokens[index].value in "+-"
        ):
            operator = tokens[index].value
            right, index = self.parse_multiplication(tokens, index + 1)
            assert left is not None  # doing this to make the type checker happy
            assert right is not None
            left = BinaryExpression(left, operator, right)

        return left, index

    def parse_multiplication(
        self, tokens: list[Token], index: int
    ) -> tuple[Expression | None, int]:
        left, index = self.parse_primary(tokens, index)

        while (
            index < len(tokens)
            and tokens[index].kind == TokenKind.SYMBOL
            and tokens[index].value in "*/"
        ):
            operator = tokens[index].value
            right, index = self.parse_primary(tokens, index + 1)
            assert left is not None
            assert right is not None
            left = BinaryExpression(left, operator, right)

        return left, index

    def parse_comparison(
        self, tokens: list[Token], index: int
    ) -> tuple[Expression | None, int]:
        left, index = self.parse_addition(tokens, index)
        while (
            index < len(tokens)
            and tokens[index].kind == TokenKind.SYMBOL
            and tokens[index].value in ["==", "!=", "<", ">", "<=", ">=", "&&", "||"]
        ):
            # logger.debug(f"Token: {tokens[index].value}")
            operator = tokens[index].value
            right, index = self.parse_addition(tokens, index + 1)
            left = BooleanExpression(left, operator, right)

        return left, index

    def parse_primary(
        self, tokens: list[Token], index: int
    ) -> tuple[Expression | None, int]:
        # logger.debug(f"Token before: {tokens[index-1].value if index > 0 else 'None'}, Current: {tokens[index].value}, Next: {tokens[index+1].value if index + 1 < len(tokens) else 'None'}")
        token = tokens[index]

        if token.kind == TokenKind.NUMBER:
            return NumberLiteral(int(token.value)), index + 1
        if token.kind == TokenKind.BOOLEAN:
            return BooleanLiteral(str(token.value).lower()), index + 1
        if token.kind == TokenKind.STRING:
            return StringLiteral(token.value), index + 1
        if token.kind == TokenKind.IDENTIFIER:
            return Identifier(token.value), index + 1

        if token.kind == TokenKind.KEYWORD and token.value == "request":
            return self.parse_request(tokens, index)

        if token.kind == TokenKind.SYMBOL and token.value == "(":
            expr, index = self.parse_expression(tokens, index + 1)

            if tokens[index].kind != TokenKind.SYMBOL or tokens[index].value != ")":
                raise UnexpectedTokenError(tokens[index].value)

            return expr, index

        raise UnexpectedTokenError(token.value)

    def parse_let(self, tokens: list[Token], index: int) -> tuple[VarDeclaration, int]:
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
            logger.debug("215")
            raise ExpectedTokenError("=", token.value)

        index += 1
        value, index = self.parse_expression(tokens, index)

        # logger.debug(f"Parsed value for variable '{var_name}': {value}")
        # logger.debug(f"Token: {tokens[index].kind}, Value: {tokens[index].value}")
        token = tokens[index]
        # logger.debug(f"Token at end of let: {token.kind}, Value: {token.value}")
        if token.kind != TokenKind.SYMBOL or token.value != ";":
            raise ExpectedTokenError(";", token.value)

        index += 1
        assert value is not None
        return VarDeclaration(var_name, value), index

    def parse_const(
        self, tokens: list[Token], index: int
    ) -> tuple[VarDeclaration, int]:
        """
        Parse a constant variable declaration starting at the current `const` token.

        Parses an identifier, an equals sign, and an expression, and returns a VarDeclaration node marked immutable along with the index positioned after the terminating token.

        Returns:
            tuple[VarDeclaration, int]: A tuple containing the `VarDeclaration` for the declared constant and the updated token index (position after the declaration).

        Raises:
            ExpectedTokenError: If an identifier or the '=' symbol is not found where expected.
        """
        index += 1
        token = tokens[index]
        if token.kind != TokenKind.IDENTIFIER:
            raise ExpectedTokenError("identifier", token.value)

        var_name = token.value
        index += 1
        token = tokens[index]

        if token.kind != TokenKind.SYMBOL or token.value != "=":
            logger.debug("256")
            raise ExpectedTokenError("=", token.value)

        index += 1
        value, index = self.parse_expression(tokens, index)
        assert value is not None
        # logger.debug(f"Parsed value for constant '{var_name}': {value}")
        index += 1
        return VarDeclaration(var_name, value, mutable=False), index

    def parse_res(self, tokens: list[Token], index: int) -> tuple[VarReassignment, int]:
        token = tokens[index]
        if token.kind != TokenKind.IDENTIFIER:
            raise ExpectedTokenError("identifier", token.value)

        var_name = token.value
        index += 1
        token = tokens[index]
        operator = None

        if token.kind != TokenKind.SYMBOL or token.value != "=":
            if token.kind == TokenKind.SYMBOL and token.value == "+=":
                operator = "+="
            elif token.kind == TokenKind.SYMBOL and token.value == "-=":
                operator = "-="
            elif token.kind == TokenKind.SYMBOL and token.value == "*=":
                operator = "*="
            elif token.kind == TokenKind.SYMBOL and token.value == "/=":
                operator = "/="
            elif token.kind == TokenKind.SYMBOL and token.value == "%=":
                operator = "%="
            else:
                logger.debug("276")
                raise ExpectedTokenError("=", token.value)

        index += 1
        value, index = self.parse_expression(tokens, index)
        token = tokens[index]

        if token.kind != TokenKind.SYMBOL or token.value != ";":
            raise ExpectedTokenError(";", token.value)

        index += 1
        assert value is not None
        return VarReassignment(var_name, value, operator), index

    def parse_output(
        self, tokens: list[Token], index: int
    ) -> tuple[OutputStatement, int]:
        # print("Parsing output statement")
        index += 1
        token = tokens[index]
        if token.kind != TokenKind.SYMBOL or token.value != "(":
            raise ExpectedTokenError("(", token.value if token else "end of input")

        index += 1
        token = tokens[index]
        # logger.debug(f"Token at start of output expression: {token.value}, TokenKind: {token.kind}")
        output_data, index = self.parse_expression(tokens, index)
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

    def parse_request(
        self, tokens: list[Token], index: int
    ) -> tuple[RequestStatement, int]:
        index += 1
        # logger.debug(f"Tokens: {tokens[index+1:]}")
        token = tokens[index]
        if token.kind != TokenKind.SYMBOL or token.value != "(":
            raise ExpectedTokenError("(", token.value if token else "end of input")
        index += 1
        token = tokens[index]
        request_data, index = self.parse_expression(tokens, index)
        token = tokens[index]
        if token.kind != TokenKind.SYMBOL or token.value != ")":
            raise ExpectedTokenError(")", token.value if token else "end of input")
        index += 1
        assert request_data is not None
        return RequestStatement(request_data), index

    def parse_while(self, tokens: list[Token], index: int) -> tuple[WhileLoop, int]:
        index += 1
        token = tokens[index]
        if token.kind != TokenKind.SYMBOL or token.value != "(":
            raise ExpectedTokenError("(", token.value if token else "end of input")
        index += 1
        token = tokens[index]
        condition, index = self.parse_expression(tokens, index)
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
            stmt, index = self.parse_statement(tokens, index)
            body_nodes.append(stmt)
            token = tokens[index]
        index += 1
        assert condition is not None
        return WhileLoop(condition, body_nodes), index

    def parse_assert(
        self, tokens: list[Token], index: int
    ) -> tuple[AssertStatement, int]:
        index += 1
        token = tokens[index]
        if token.kind != TokenKind.SYMBOL or token.value != "(":
            raise ExpectedTokenError("(", token.value if token else "end of input")
        index += 1
        condition, index = self.parse_expression(tokens, index)
        if not condition:
            raise InvalidAssertStatementError("")
        token = tokens[index]
        if token.kind != TokenKind.SYMBOL or token.value != ",":
            index += 1
            message = None
        else:
            index += 1
            token = tokens[index]
            if token.kind != TokenKind.STRING:
                raise ExpectedTokenError('"', token.value if token else "end of input")
            message = token.value
            index += 1
            token = tokens[index]
        token = tokens[index]
        if token.kind != TokenKind.SYMBOL or token.value != ")":
            if token.kind == TokenKind.SYMBOL and token.value == ";":
                assert condition is not None
                return AssertStatement(condition, message), index + 1
            else:
                raise ExpectedTokenError(")", token.value if token else "end of input")

        index += 1
        token = tokens[index]
        index += 1
        assert condition is not None
        return AssertStatement(condition, message), index

    def parse_foreach(self, tokens: list[Token], index: int) -> tuple[ForeachLoop, int]:
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
        collection, index = self.parse_expression(tokens, index)
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
            stmt, index = self.parse_statement(tokens, index)
            body_nodes.append(stmt)
            token = tokens[index]
        index += 1
        assert collection is not None
        return ForeachLoop(var_name, collection, body_nodes), index

    def parse_if(self, tokens: list[Token], index: int) -> tuple[IfStatement, int]:
        index += 1
        token = tokens[index]
        if token.kind != TokenKind.SYMBOL or token.value != "(":
            raise ExpectedTokenError("(", token.value if token else "end of input")

        index += 1
        token = tokens[index]
        condition, index = self.parse_expression(tokens, index)

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
            stmt, index = self.parse_statement(tokens, index)
            body_nodes.append(stmt)
            token = tokens[index]
        index += 1

        else_branch = None

        if (
            index < len(tokens)
            and tokens[index].kind == TokenKind.KEYWORD
            and tokens[index].value == "elseif"
        ):
            else_branch, index = self.parse_if(tokens, index)
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
                stmt, index = self.parse_statement(tokens, index)
                else_body.append(stmt)
                token = tokens[index]
            index += 1
            else_branch = else_body
            assert condition is not None
            return IfStatement(condition, body_nodes, else_branch), index
        assert condition is not None
        return IfStatement(condition, body_nodes, None), index

    def parse_function(self, tokens: list[Token], index: int) -> tuple[Function, int]:
        # logger.debug(f"Parsing function at index {index}: TokenKind={tokens[index].kind}, Value={tokens[index].value}")
        index += 1
        try:
            token = tokens[index]
        except IndexError:
            raise ParseError("Unexpected end of input while parsing function") from None
        if token.kind != TokenKind.IDENTIFIER:
            raise ExpectedTokenError(
                "identifier", token.value if token else "end of input"
            )
        func_name = token.value
        index += 1
        token = tokens[index]
        if token.kind != TokenKind.SYMBOL or token.value != "=":
            logger.debug("514")
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
            stmt, index = self.parse_statement(tokens, index)
            body_nodes.append(stmt)
            token = tokens[index]
        index += 1
        return Function(func_name, [], body_nodes), index

    def parse_FunctionCall(
        self, tokens: list[Token], index: int
    ) -> tuple[FunctionCall, int]:
        """
        Parse a function call starting at the given token index and return the corresponding AST node and the next index after the call.

        Parameters:
            tokens (list[Token]): Sequence of tokens produced by the lexer.
            index (int): Current index in `tokens` pointing at the function name.

        Returns:
            tuple[FunctionCall, int]: A FunctionCall AST node for the parsed call and the updated token index positioned after the terminating semicolon.

        Raises:
            ExpectedTokenError: If the expected "(", ")", or ";" tokens are not found at the appropriate positions.
        """
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

    def parse_Break(
        self, tokens: list[Token], index: int
    ) -> tuple[BreakStatement, int]:
        """
        Parse a `break` statement and advance the token index past its terminating semicolon.

        Returns:
            tuple(BreakStatement, int): The parsed BreakStatement node and the next token index (position after the semicolon).

        Raises:
            ParseError: If input ends unexpectedly while parsing the break.
            ExpectedTokenError: If the token following `break` is not a semicolon (`";"`).
        """
        index += 1
        if index >= len(tokens):
            raise ParseError("Unexpected end of input while parsing break") from None
        token = tokens[index]
        if token.kind != TokenKind.SYMBOL or token.value != ";":
            raise ExpectedTokenError(";", token.value if token else "end of input")
        index += 1
        return BreakStatement(), index

    def parse(self, tokens: list[Token], index: int) -> tuple[list[ASTStatement], int]:
        """
        Parse a list of statements starting at the given token index and return the corresponding AST nodes and the next index after the last statement.

        Args:
            tokens (list[Token]): The list of tokens to parse.
            index (int): The starting index in the token list.

        Returns:
            tuple[list[ASTStatement], int]: The parsed AST nodes and the next token index (position after the last statement).

        Raises:
            ParseError: If input ends unexpectedly while parsing the statements.
            ExpectedTokenError: If a statement is not followed by a semicolon (`";"`).
        """
        self.nodes: list[ASTStatement] = []
        while index < len(tokens):
            # logger.debug(f"Parsed tokens: {parsed_tokens}")
            # logger.debug(parsed_tokens[index].kind, parsed_tokens[index].value)
            node, index = self.parse_statement(tokens, index)
            self.nodes.append(node)
        return self.nodes, index
