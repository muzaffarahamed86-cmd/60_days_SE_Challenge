import streamlit as st
from converters.currency import inr_to_usd, usd_to_inr
from converters.temperature import c_to_f, f_to_c
from converters.length import cm_to_inch, inch_to_cm
from converters.weight import kg_to_lb, lb_to_kg

st.set_page_config(page_title="Premium Unit Converter", layout="wide")

# ---------------------------
# DARK / LIGHT MODE TOGGLE
# ---------------------------
theme = st.sidebar.radio("🌓 Theme Mode", ["Light", "Dark"], index=0)

if theme == "Light":
    background = "#f7f7f7"
    card_bg = "linear-gradient(135deg, #ffffff, #f1f1f1)"
    text_color = "#222"
else:
    background = "#0f0f0f"
    card_bg = "linear-gradient(135deg, #1d1d1d, #2a2a2a)"
    text_color = "#f8f8f8"

# ---------------------------
# CUSTOM CSS
# ---------------------------
st.markdown(f"""
<style>
    body {{
        background-color: {background};
    }}

    .main .block-container {{
        background-color: {background};
        padding-top: 1rem;
    }}

    /* Card styling */
    .card {{
        background: {card_bg};
        padding: 20px 25px;
        border-radius: 18px;
        color: {text_color};
        box-shadow: 0 6px 18px rgba(0,0,0,0.15);
        margin-bottom: 22px;
        transition: all 0.3s ease-in-out;
        animation: fadein 0.8s ease;
    }}
    .card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 22px rgba(0,0,0,0.25);
    }}

    /* Fade-in animation */
    @keyframes fadein {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    h3 {{
        color: {text_color};
        margin-bottom: 10px;
        font-size: 1.3rem;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# HEADER
# ---------------------------
st.markdown(
    f"<h1 style='text-align:center; color:{text_color}; padding-bottom:10px;'>"
    "✨ Premium Unit Converter</h1>",
    unsafe_allow_html=True
)

st.markdown(
    f"<p style='text-align:center; color:{text_color}; font-size:17px;'>"
    "Smooth animations • Material design • Theme mode • Gradient UI</p>",
    unsafe_allow_html=True
)

st.write("")

# ---------------------------
# 2-COLUMN MAIN LAYOUT
# ---------------------------
left, right = st.columns(2)

# ---------------------------
# LEFT SIDE CARDS
# ---------------------------
with left:

    # Currency Card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 💰 Currency (INR ↔ USD)")
    inr = st.number_input("INR → USD", value=0.0, key="inr")
    st.write(f"USD: **{inr_to_usd(inr):,.4f}**")

    usd = st.number_input("USD → INR", value=0.0, key="usd")
    st.write(f"INR: **{usd_to_inr(usd):,.2f}**")
    st.markdown("</div>", unsafe_allow_html=True)

    # Temperature Card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 🌡 Temperature (°C ↔ °F)")
    c = st.number_input("Celsius → Fahrenheit", value=0.0, key="celsius")
    st.write(f"Fahrenheit: **{c_to_f(c):.2f}°F**")

    f = st.number_input("Fahrenheit → Celsius", value=0.0, key="fah")
    st.write(f"Celsius: **{f_to_c(f):.2f}°C**")
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------
# RIGHT SIDE CARDS
# ---------------------------
with right:

    # Length Card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📏 Length (cm ↔ inch)")
    cm = st.number_input("cm → inch", value=0.0, key="cm_box")
    st.write(f"Inch: **{cm_to_inch(cm):.4f}**")

    inch = st.number_input("inch → cm", value=0.0, key="inch_box")
    st.write(f"cm: **{inch_to_cm(inch):.3f}**")
    st.markdown("</div>", unsafe_allow_html=True)

    # Weight Card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### ⚖ Weight (kg ↔ lb)")
    kg = st.number_input("kg → lb", value=0.0, key="kg_box")
    st.write(f"lb: **{kg_to_lb(kg):.4f}**")

    lb = st.number_input("lb → kg", value=0.0, key="lb_box")
    st.write(f"kg: **{lb_to_kg(lb):.4f}**")
    st.markdown("</div>", unsafe_allow_html=True)
 