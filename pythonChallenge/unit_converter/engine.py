from converters.currency import inr_to_usd, usd_to_inr
from converters.temperature import c_to_f, f_to_c
from converters.length import cm_to_inch, inch_to_cm
from converters.weight import kg_to_lb, lb_to_kg

conversions = {
    "INR to USD": inr_to_usd,
    "USD to INR": usd_to_inr,
    "Celsius to Fahrenheit": c_to_f,
    "Fahrenheit to Celsius": f_to_c,
    "cm to inch": cm_to_inch,
    "inch to cm": inch_to_cm,
    "kg to lb": kg_to_lb,
    "lb to kg": lb_to_kg
}

def convert(value, conversion_type):
    if conversion_type not in conversions:
        raise ValueError("Unsupported conversion type")
    return conversions[conversion_type](value)
