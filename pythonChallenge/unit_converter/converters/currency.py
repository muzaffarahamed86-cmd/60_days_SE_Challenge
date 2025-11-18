"""Simple currency converter with fixed demo rates.

Note: This uses hard-coded example rates (relative to USD) for offline/demo use.
For production use, wire this to a live rates API.
"""

RATES_TO_USD = {
    "USD": 1.0,
    "EUR": 1.1,   # 1 EUR = 1.1 USD (example)
    "GBP": 1.28,  # 1 GBP = 1.28 USD
    "INR": 0.012, # 1 INR = 0.012 USD
    "JPY": 0.0070,
}


def convert_currency(amount, from_currency, to_currency):
    """Convert `amount` from `from_currency` to `to_currency` using RATES_TO_USD.

    Raises ValueError for unknown currencies.
    """
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency not in RATES_TO_USD:
        raise ValueError(f"Unsupported currency: {from_currency}")
    if to_currency not in RATES_TO_USD:
        raise ValueError(f"Unsupported currency: {to_currency}")

    # Convert from source to USD, then USD to target
    amount_usd = float(amount) * RATES_TO_USD[from_currency]
    result = amount_usd / RATES_TO_USD[to_currency]
    return round(result, 4)
