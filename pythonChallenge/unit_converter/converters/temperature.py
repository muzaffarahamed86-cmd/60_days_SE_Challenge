"""Temperature conversion utilities."""

VALID = {"C", "F", "K"}


def convert_temperature(value, from_unit, to_unit):
    """Convert temperature between C, F, and K.

    from_unit/to_unit are one of 'C', 'F', 'K' (case-insensitive).
    """
    f = from_unit.upper()
    t = to_unit.upper()
    if f not in VALID or t not in VALID:
        raise ValueError("Units must be one of 'C', 'F', 'K'.")

    v = float(value)
    # normalize to Celsius
    if f == "C":
        c = v
    elif f == "F":
        c = (v - 32.0) * 5.0 / 9.0
    else:  # K
        c = v - 273.15

    # to target
    if t == "C":
        return round(c, 4)
    elif t == "F":
        return round((c * 9.0 / 5.0) + 32.0, 4)
    else:  # K
        return round(c + 273.15, 4)
