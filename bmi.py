import streamlit as st

# --------------------
# PAGE CONFIG
# --------------------
st.set_page_config(
    page_title="BMI Calculator",
    page_icon="🏋️",
    layout="centered"
)

# --------------------
# HEADER
# --------------------
st.title("🏋️ BMI Calculator")
st.write("Enter your height and weight to calculate your BMI.")

# --------------------
# INPUT SECTION
# --------------------
col1, col2 = st.columns(2)

with col1:
    height = st.number_input("Height (cm)", min_value=50.0, max_value=300.0, step=0.1)

with col2:
    weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0, step=0.1)

# --------------------
# BMI LOGIC
# --------------------
def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    if bmi < 18.5:
        category = "Underweight"
        color = "blue"
    elif bmi < 25:
        category = "Normal"
        color = "green"
    elif bmi < 30:
        category = "Overweight"
        color = "orange"
    else:
        category = "Obese"
        color = "red"

    return round(bmi, 2), category, color


# --------------------
# BUTTON + OUTPUT
# --------------------
if st.button("Calculate BMI"):
    if height == 0 or weight == 0:
        st.warning("Please enter valid height and weight.")
    else:
        bmi, category, color = calculate_bmi(height, weight)

        st.markdown(f"### 📊 Your BMI: **{bmi}**")
        st.markdown(
            f"<h3 style='color:{color};'>Category: {category}</h3>",
            unsafe_allow_html=True
        )

        # Extra suggestion
        if category == "Underweight":
            st.info("Try to increase caloric intake and consult a nutrition expert.")
        elif category == "Normal":
            st.success("Great! Maintain this with a balanced diet and regular exercise.")
        elif category == "Overweight":
            st.warning("Consider improving diet & activity level.")
        else:
            st.error("High risk! Consider medical advice and lifestyle changes.")
