"""Main application entry point for the calculator app."""

import streamlit as st
from calculator.calculator import Calculator
from utils.validators import validate_number

st.set_page_config(page_title="OOP Calculator", page_icon="🧮")

st.title("🧮 Calculator Powered by Streamlit")

calc = Calculator()

num1 = st.text_input("Enter first number:")
num2 = st.text_input("Enter second number:")

operation = st.selectbox(
    "Select operation:",
    ["Addition", "Subtraction", "Multiplication", "Division"]
)

if st.button("Calculate"):
    try:
        a = validate_number(num1)
        b = validate_number(num2)
        result = calc.calculate(a, b, operation)

        st.success(f"Result: **{result}**")

    except Exception as e:
        st.error(str(e))
