from engine import convert, conversions

def main():
    print("\nAvailable Conversions:")
    for c in conversions.keys():
        print(" -", c)

    conversion_type = input("\nSelect conversion: ")
    value = float(input("Enter value: "))

    result = convert(value, conversion_type)
    print(f"\nResult: {result}")

if __name__ == "__main__":
    main()
