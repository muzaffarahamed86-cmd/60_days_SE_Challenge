"""Input validation utilities."""


def validate_number(value):
    try:
        return float(value)
    except ValueError:
        raise ValueError("Input must be a number")

