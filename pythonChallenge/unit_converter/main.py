"""Simple CLI for the unit_converter engine.

Examples:
  python main.py currency 100 USD EUR
  python main.py temperature 100 C F
  python main.py length 10 km mi
  python main.py weight 5 kg lb
"""
import argparse
from engine import convert


def main():
    parser = argparse.ArgumentParser(description="Unit converter CLI")
    parser.add_argument("category", help="Category: currency|temperature|length|weight")
    parser.add_argument("value", help="Numeric value to convert")
    parser.add_argument("from_unit", help="Source unit/currency")
    parser.add_argument("to_unit", help="Target unit/currency")
    args = parser.parse_args()

    try:
        result = convert(args.category, args.value, args.from_unit, args.to_unit)
        print(result)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
