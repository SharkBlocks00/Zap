class ZapError(Exception):
    def __init__(
        self, message: str, *, line: int | None = None, column: int | None = None
    ):
        self.message = message
        self.line: int | None = line
        self.column: int | None = column
        super().__init__(self.__str__())

    def __str__(self):
        location = ""
        if self.line is not None:
            location += f"Line {self.line}"
            if self.column is not None:
                location += f", Column {self.column}"
            location += ": "
        return f"{location}{self.message}"
