import streamlit as st
import streamlit.components.v1 as components
from math import pi, sin, cos

st.set_page_config(page_title="BMI Calculator", layout="wide", page_icon="⚖️")

# Remove Streamlit padding
st.markdown("""
<style>
.block-container { padding-top: 0rem !important; }
header, .stApp header { height:0; opacity:0; }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# BMI LOGIC + CATEGORY
# ---------------------------------------------------------
def bmi_value(h, w):
    try:
        return round(w / ((h / 100)**2), 2)
    except:
        return None


def bmi_category(bmi):
    if bmi is None:
        return "", "#999999"
    if bmi < 18.5:
        return "Underweight", "#3B82F6"
    if bmi < 25:
        return "Normal", "#10B981"
    if bmi < 30:
        return "Overweight", "#F59E0B"
    if bmi < 35:
        return "Obese", "#F97316"
    return "Extremely Obese", "#EF4444"


# Map BMI → angle (BOTTOM START ARC)
def bmi_to_angle_bottom(bmi, min_bmi=0, max_bmi=40):
    if bmi is None:
        return 180
    v = max(min_bmi, min(max_bmi, bmi))
    return 180 + ((v - min_bmi) / (max_bmi - min_bmi)) * 180


# ---------------------------------------------------------
# CLEAN SEMICIRCLE GAUGE (No 3D, No fancy effects)
# ---------------------------------------------------------
def build_semicircle_bottom(bmi):

    CX = 250
    CY = 250
    R = 200

    # Perfect pivot (corrected)
    PIVOT_Y = CY - (R * 0.10)

    display = bmi if bmi is not None else "--"

    # Color zones
    segments = [
        (0, 18.5, "#3B82F6"),
        (18.5, 25, "#10B981"),
        (25, 30, "#F59E0B"),
        (30, 35, "#F97316"),
        (35, 40, "#EF4444")
    ]

    seg_paths = ""
    for s, e, color in segments:
        a1 = 180 + (s / 40) * 180
        a2 = 180 + (e / 40) * 180
        r1 = pi * a1 / 180
        r2 = pi * a2 / 180

        x1 = CX + R * cos(r1)
        y1 = CY + R * sin(r1)
        x2 = CX + R * cos(r2)
        y2 = CY + R * sin(r2)

        seg_paths += f'''
            <path d="M {x1:.2f} {y1:.2f}
                     A {R} {R} 0 0 1 {x2:.2f} {y2:.2f}"
                  stroke="{color}"
                  stroke-width="40"
                  stroke-linecap="round"
                  fill="none"/>
        '''

    # Background arc
    bg_arc = f'''
        <path d="M {CX-R} {CY}
                 A {R} {R} 0 0 1 {CX+R} {CY}"
              stroke="#E5E7EB"
              stroke-width="48"
              stroke-linecap="round"
              fill="none"
              opacity="0.8"/>
    '''

    # Ticks
    ticks = ""
    for m in [0, 10, 20, 25, 30, 35, 40]:
        ang = 180 + (m / 40) * 180
        rad = ang * pi / 180

        xi = CX + (R - 35) * cos(rad)
        yi = CY + (R - 35) * sin(rad)
        xo = CX + (R + 10) * cos(rad)
        yo = CY + (R + 10) * sin(rad)

        ticks += f'''
            <line x1="{xi:.2f}" y1="{yi:.2f}"
                  x2="{xo:.2f}" y2="{yo:.2f}"
                  stroke="#374151"
                  stroke-width="1.6"/>
        '''

        xl = CX + (R - 75) * cos(rad)
        yl = CY + (R - 75) * sin(rad)

        ticks += f'''
            <text x="{xl:.2f}" y="{yl:.2f}"
                  font-size="13"
                  text-anchor="middle"
                  fill="#374151">{m}</text>
        '''

    # Needle (hidden when BMI = None)
    angle = bmi_to_angle_bottom(bmi)

    needle = f'''
        <g transform="translate({CX},{PIVOT_Y}) rotate({angle})"
           style="transition: transform 900ms cubic-bezier(.2,.9,.3,1);">

            <line x1="0" y1="0"
                  x2="0" y2="-150"
                  stroke="#064E3B"
                  stroke-width="10"
                  stroke-linecap="round"/>

            <circle cx="0" cy="-150" r="14" fill="#064E3B"/>
            <circle cx="0" cy="0" r="14" fill="#064E3B"/>
        </g>
    '''

    show_needle = needle if bmi is not None else ""

    # Final SVG
    svg = f'''
        <div style="display:flex; justify-content:center;">
        <svg width="100%" height="420" viewBox="0 0 500 350">

            {bg_arc}
            {seg_paths}
            {ticks}
            {show_needle}

            <text x="{CX}" y="{PIVOT_Y - 20}"
                  text-anchor="middle"
                  font-size="32"
                  font-weight="700">{display}</text>

        </svg>
        </div>
    '''
    return svg


# ---------------------------------------------------------
# UI
# ---------------------------------------------------------
with st.sidebar:
    st.title("BMI Calculator")
    name = st.text_input("Name", "Muzaffar Ahamed")
    h = st.number_input("Height (cm)", 50.0, 250.0, 170.0)
    w = st.number_input("Weight (kg)", 10.0, 300.0, 70.0)

    if st.button("Calculate BMI"):
        st.session_state.bmi = bmi_value(h, w)

    if st.button("Reset"):
        st.session_state.bmi = None


st.markdown("<h1>⚖️ BMI Calculator</h1>", unsafe_allow_html=True)

bmi = st.session_state.get("bmi")
cat, col = bmi_category(bmi)

left, right = st.columns([2, 1])

with left:
    st.subheader("Visual BMI Gauge")
    svg = build_semicircle_bottom(bmi)
    components.html(svg, height=430, scrolling=False)

with right:
    st.subheader("Result")
    if bmi is not None:
        st.write(f"### Hello, {name}")
        st.write(f"## BMI: {bmi}")

        st.markdown(
            f"""
            <div style='padding:8px 14px;
                        background:{col};
                        color:white;
                        width:max-content;
                        border-radius:8px;
                        font-size:18px;
                        font-weight:600'>
                {cat}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info("Enter your height and weight, then click **Calculate BMI**.")
