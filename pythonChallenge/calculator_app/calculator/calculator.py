"""Main calculator class."""

from .operations import Operations

class Calculator:
    def __init__(self):
        self.ops = Operations()

    def calculate(self, a, b, operation):
        if operation == "Addition":
            return self.ops.add(a, b)
        elif operation == "Subtraction":
            return self.ops.subtract(a, b)
        elif operation == "Multiplication":
            return self.ops.multiply(a, b)
        elif operation == "Division":
            return self.ops.divide(a, b)
        else:
            raise ValueError("Invalid operation")
