"""Length conversion utilities."""

# conversion factors to meters
_TO_M = {
    "m": 1.0,
    "cm": 0.01,
    "mm": 0.001,
    "km": 1000.0,
    "in": 0.0254,
    "ft": 0.3048,
    "yd": 0.9144,
    "mi": 1609.344,
}


def convert_length(value, from_unit, to_unit):
    fu = from_unit.lower()
    tu = to_unit.lower()
    if fu not in _TO_M:
        raise ValueError(f"Unsupported length unit: {from_unit}")
    if tu not in _TO_M:
        raise ValueError(f"Unsupported length unit: {to_unit}")

    meters = float(value) * _TO_M[fu]
    result = meters / _TO_M[tu]
    return round(result, 6)
