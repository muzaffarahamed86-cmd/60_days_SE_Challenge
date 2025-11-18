"""Engine wrapper that routes conversion requests to the proper converter."""
from converters import (
    convert_currency,
    convert_temperature,
    convert_length,
    convert_weight,
)


def convert(category, value, from_unit, to_unit):
    """Generic convert function.

    category: 'currency', 'temperature', 'length', or 'weight'
    """
    category = category.lower()
    if category == "currency":
        return convert_currency(value, from_unit, to_unit)
    elif category == "temperature":
        return convert_temperature(value, from_unit, to_unit)
    elif category == "length":
        return convert_length(value, from_unit, to_unit)
    elif category == "weight":
        return convert_weight(value, from_unit, to_unit)
    else:
        raise ValueError(f"Unsupported category: {category}")
