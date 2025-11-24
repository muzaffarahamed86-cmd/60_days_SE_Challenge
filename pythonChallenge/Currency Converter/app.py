import streamlit as st
import requests

def get_exchange_rates():
    """Fetches exchange rates from a free API."""
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["rates"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching rates: {e}")
        return None

def convert_currency(amount, from_currency, to_currency, rates):
    """Converts currency using the provided rates dictionary."""
    if not rates:
        return 0.0
    
    # Extract code from "🇮🇳 INR" -> "INR"
    from_code = from_currency.split(" ")[1]
    to_code = to_currency.split(" ")[1]
    
    rate_from = rates.get(from_code)
    rate_to = rates.get(to_code)
    
    if rate_from is None or rate_to is None:
        st.error("Currency rate not found.")
        return 0.0

    amount_in_usd = amount / rate_from
    converted_amount = amount_in_usd * rate_to
    
    return converted_amount

def main():
    st.set_page_config(page_title="Currency Converter", page_icon="💱", layout="centered")
    
    # Custom CSS for specific elements only (Header and Result)
    st.markdown("""
        <style>
        .stApp {
            background-color: #f8f9fa;
        }
        .header-title {
            text-align: center;
            color: #0d6efd;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin-bottom: 10px;
        }
        .header-subtitle {
            text-align: center;
            color: #6c757d;
            margin-bottom: 30px;
        }
        .result-box {
            background-color: #d1e7dd;
            color: #0f5132;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
            border: 1px solid #badbcc;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("<h1 class='header-title'>💱 Currency Converter</h1>", unsafe_allow_html=True)
    st.markdown("<p class='header-subtitle'>Real-time exchange rates at your fingertips</p>", unsafe_allow_html=True)
    
    # Fetch rates
    with st.spinner("Fetching latest rates..."):
        rates = get_exchange_rates()
    
    if not rates:
        st.warning("Using fallback static rates due to API error.")
        rates = {"USD": 1.0, "INR": 84.0, "EUR": 0.92, "GBP": 0.77}
    
    currencies = ["🇮🇳 INR", "🇺🇸 USD", "🇪🇺 EUR", "🇬🇧 GBP"]
    
    # Main Card using native container with border
    with st.container(border=True):
        st.markdown("### 🔢 Convert")
        
        amount = st.number_input("Amount", min_value=0.0, value=1.0, step=0.1, format="%.2f")
        
        st.write("") # Spacer
        
        col1, col2 = st.columns(2)
        
        with col1:
            from_currency = st.selectbox("From", currencies, index=1) # Default USD
        
        with col2:
            to_currency = st.selectbox("To", currencies, index=0) # Default INR
            
        result = convert_currency(amount, from_currency, to_currency, rates)
        
        # Display Result
        st.markdown(
            f"""
            <div class="result-box">
                {amount} {from_currency.split(" ")[1]} = {result:.2f} {to_currency.split(" ")[1]}
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    st.markdown("<div style='text-align: center; margin-top: 20px; color: #aaa; font-size: 0.8em;'>Rates sourced from open.er-api.com</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
