from typing import List, Any

from Exceptions import *
from Variable import Variable

""" WORD OF NOTICE: 
    
    THIS IS EXTREMELY INEFFICIENT, AND REPEATS ITSELF MANY TIMES.
    IT IS NOT MEANT TO BE FAST OR GOOD.
    
    Also very messy soo..
"""
class Parser:
    def __init__(self):
        self.keywords: List[str] = ["let", "res", "output", "request", ";", "--"]

    def parse_value(self, raw_value: str) -> Any:
        if raw_value.isdigit():
            return int(raw_value)
        try:
            return float(raw_value)
        except ValueError:
            return raw_value.replace('"', "")

    def parse(self, source):
        source = source.strip()

        # Globals
        active_variables: dict[str, Variable] = {}

        for line_count, text in enumerate(source.splitlines(), start=1):

            if text.strip() == "":
                continue
            missing_keywords: int = 0
            for keyword in self.keywords:
                if keyword in text:
                    break
                if text.find(keyword) == -1:
                    missing_keywords += 1
                    if missing_keywords == len(self.keywords):
                        raise InvalidSyntax(f"Invalid syntax at line {line_count}: {text}")


            comment_pos: int = text.find("--")
            if comment_pos != -1:
                if not text[:comment_pos]:
                    continue
                text = text[:comment_pos]

            last_pos: int = text.rfind(";")
            if last_pos == -1:
                raise InvalidSyntax(f"';' Expected on line {line_count}.")
            if text[last_pos + 1:]:
                if text.rfind("--"):
                  #  print(f"Comment found on line {line_count}")
                   # print(text[text.rfind("--") - 1])
                    if text[:text.rfind("--")].strip().endswith(";"):
                       # print("Comment succesfully parsed.")
                        continue
                raise CharacterAfterEndOfLine(
                    f"Unexpected character/s after EOL at position {last_pos}: {text[last_pos:]} on line {line_count}"
                )

            output_pos: int = text.find("output")
            variable_declare_position: int = text.find("let")
            variable_assign_position: int = text.find("res")
            request_pos: int = text.find("request")

            if variable_declare_position == 0:
                variable_name: str = text[variable_declare_position + 3:].strip().split("=")[0].strip()
                raw_value: Any = text[text.rfind("=") + 1:].strip().strip(";") if request_pos == -1 else text[request_pos + 7:].strip(";")
                #print(f"Debug: Raw value: {raw_value}")

                if request_pos != -1:
                    start = text.find("(", request_pos)
                    end = text.rfind(")")

                    if start == -1 or end < start:
                        raise InvalidSyntax(
                            f"Expected a '(' to begin a request statement at position {request_pos + 7} on line {line_count}"
                        )
                    elif end == -1:
                        raise InvalidSyntax(
                            f"Expected a ')' to end a request statement on line {line_count}"
                        )

                    request_text: str = text[start + 1:end].strip()

                    if request_text.startswith('"') and request_text.endswith('"'):
                        request_text = request_text[1:-1]
                    else:
                        if request_text in active_variables:
                            request_text = active_variables[request_text].value
                        else:
                            raise InvalidSyntax(f"Cannot have empty request statement (line {line_count})")

                    raw_value = input(request_text)


                variable_value = self.parse_value(raw_value)

                if variable_name == "":
                    raise InvalidSyntax(
                        f"Cannot assign {variable_value} to a nil variable. (Line: {line_count})."
                    )
                if variable_name in active_variables:
                    raise InvalidSyntax(f"Variable '{variable_name}' already declared.")
                #print(f"Debug: Declared variable name: {variable_name} with value of: {variable_value}")

                if active_variables.__contains__(variable_value):
                    variable_value = active_variables[variable_value]
                    #print(f"Debug: Variable {variable_name} is taking value {variable_value}")

                active_variables[variable_name] = Variable(variable_name, variable_value)

               # print(f"Debug: Added variable: {variable_name} with value: {variable_value} to active variables. Active variables: {active_variables}")
                continue

            if variable_assign_position == 0:
                variable_name: str = text[variable_assign_position + 3:].strip().split("=")[0].strip()
                raw_value: Any = text[text.rfind("=") + 1:].strip().strip(";") if request_pos == -1 else text[request_pos + 7:].strip(";")
                #print(f"Debug: [reassignment] Raw value: {raw_value}")

                if request_pos != -1:
                    start = text.find("(", request_pos)
                    end = text.rfind(")")

                    if start == -1 or end < start:
                        raise InvalidSyntax(
                            f"Expected a '(' to begin a request statement at position {request_pos + 7} on line {line_count}"
                        )
                    elif end == -1:
                        raise InvalidSyntax(
                            f"Expected a ')' to end a request statement on line {line_count}"
                        )

                    request_text: str = text[start + 1:end].strip()

                    if request_text.startswith('"') and request_text.endswith('"'):
                        request_text = request_text[1:-1]
                    else:
                        if request_text in active_variables:
                            request_text = active_variables[request_text].value
                        else:
                            raise InvalidSyntax(f"Cannot have empty request statement (line {line_count})")
                    raw_value = input(request_text)

                variable_value = self.parse_value(raw_value)

                if variable_name == "":
                    raise InvalidSyntax(
                        f"Cannot do variable reassignment to a nil variable. (Line: {line_count})."
                    )
                if variable_name not in active_variables:
                    raise InvalidSyntax(
                        f"Cannot reassign variable values to an undefined variable (Line: {line_count})."
                    )

                if active_variables.__contains__(variable_value):
                    variable_value = active_variables[variable_value]
                   # print(f"Debug: [reassignment] Variable {variable_name} is taking value {variable_value}")

                active_variables[variable_name] = Variable(variable_name, variable_value)
                #print(f"Reassigning variable {variable_name}'s value to variable {variable_value}.")
                continue

            if output_pos != -1:
                start = text.find("(", output_pos)
                end = text.rfind(")")

                if start == -1 or end < start:
                    raise InvalidSyntax(
                        f"Expected a '(' to begin output statement at position {output_pos + 6} on line {line_count}"
                    )
                elif end == -1:
                    raise InvalidSyntax(
                        f"Expected a ')' to end output statement on line {line_count}"
                    )

                output_text: str = text[start + 1:end].strip()

                if output_text.startswith('"') and output_text.endswith('"'):
                    output_text = output_text[1:-1]
                else:
                    if output_text in active_variables:
                        output_text = active_variables[output_text].value
                    elif not output_text.strip() == "":
                        raise InvalidSyntax(f"Unknown variable '{output_text}' on line {line_count} position {output_pos + 7}")
                    else:
                        raise InvalidSyntax(f"Cannot have empty output statement (line {line_count})")

                print(output_text)
                continue


            left_bracket_count: int = 0
            right_bracket_count: int = 0

            for position, character in enumerate(text):
                #print(f"Character at position {position}: {character}")

                if character == "(":
                    if (position == 0 or text[position - 1] != '"') and (
                        position + 1 >= len(text) or text[position + 1] != '"'
                    ):
                        left_bracket_count += 1

                elif character == ")":
                    if (position == 0 or text[position - 1] != '"') and (
                        position + 1 >= len(text) or text[position + 1] != '"'
                    ):
                        right_bracket_count += 1

                    if position + 1 < len(text) and text[position + 1] == ";":
                        break

            #print(f"Parenthesis amounts: Left: {left_bracket_count}, Right: {right_bracket_count}")

            if left_bracket_count != right_bracket_count:
                raise InvalidSyntax(f"Unequal parentheses amounts on line {line_count}")

            raise ParseError(f"Error parsing code: {text}") # Fallback for if its not parsed


        #print(output_position)
       # print(last_pos)

        return source
