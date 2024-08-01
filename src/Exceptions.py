ERROR_STACK = []

class ParserException(Exception):
    def __init__(self, message):
        super().__init__(message)