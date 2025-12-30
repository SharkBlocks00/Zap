from typing import Any


class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.type = self.get_type(value)
        #print(f"Type: {self.type}")

    def get_type(self, value) -> Any:
        return type(value)

    def get_value(self) -> Any:
        return self.value

    def __str__(self):
        return f"{self.value}"

