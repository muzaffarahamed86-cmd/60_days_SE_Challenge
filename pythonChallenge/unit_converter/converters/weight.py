"""Weight conversion utilities."""

# conversion factors to kilograms
_TO_KG = {
    "kg": 1.0,
    "g": 0.001,
    "mg": 1e-6,
    "lb": 0.45359237,
    "oz": 0.0283495231,
    "ton": 1000.0,
}


def convert_weight(value, from_unit, to_unit):
    fu = from_unit.lower()
    tu = to_unit.lower()
    if fu not in _TO_KG:
        raise ValueError(f"Unsupported weight unit: {from_unit}")
    if tu not in _TO_KG:
        raise ValueError(f"Unsupported weight unit: {to_unit}")

    kg = float(value) * _TO_KG[fu]
    result = kg / _TO_KG[tu]
    return round(result, 6)
