import streamlit as st

# --------------------------
# APP CONFIG
# --------------------------
st.set_page_config(page_title="Greeting Form", page_icon="👋", layout="centered")

st.title("👋 Welcome! Let's Get to Know You")

st.write("Fill in your details below and get a fun, personalized greeting! 🎉")

# --------------------------
# FORM INPUTS
# --------------------------
with st.form("greeting_form"):
    name = st.text_input("Enter your name:")
    age = st.slider("Select your age:", min_value=1, max_value=100, value=25)
    submit = st.form_submit_button("Show Greeting")

# --------------------------
# FUNCTION: Emoji Based on Age
# --------------------------
def get_age_emoji(age):
    if age < 13:
        return "🎈 Kid"
    elif age < 20:
        return "🧢 Teen"
    elif age < 40:
        return "🔥 Adult"
    elif age < 60:
        return "🧠 Experienced"
    else:
        return "👴 Senior"

# --------------------------
# OUTPUT
# --------------------------
if submit:
    if name.strip() == "":
        st.warning("Please enter your name 🙏")
    else:
        emoji_label = get_age_emoji(age)
        st.success(f"Hello **{name}!** You are **{age} years old** — {emoji_label} 😄")

