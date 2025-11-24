import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import datetime

# ------------------------------
# SESSION STATE INITIALIZATION
# ------------------------------
if "water_data" not in st.session_state:
    st.session_state.water_data = pd.DataFrame(columns=["date", "amount"])

st.set_page_config(page_title="Water Intake Tracker", layout="centered")

st.title("💧 Water Intake Tracker")

water_data = st.session_state.water_data

# ----------------------------------
# INPUT FORM
# ----------------------------------
st.subheader("Add Water Intake")

with st.form("water_form"):
    intake_date = st.date_input("Select Date", value=date.today())
    intake_amount = st.number_input("Enter Amount (ml)", min_value=100, max_value=2000, step=50)
    add = st.form_submit_button("Add")

if add:
    new_row = pd.DataFrame([{"date": intake_date, "amount": intake_amount}])
    st.session_state.water_data = pd.concat([water_data, new_row], ignore_index=True)
    st.success("Water intake logged successfully!")
    water_data = st.session_state.water_data

# ----------------------------------
# DAILY SUMMARY
# ----------------------------------
st.subheader("Daily Summary")

daily_total = water_data.groupby("date")["amount"].sum().reset_index()
goal = 3000

for _, row in daily_total.iterrows():
    achieved = row["amount"] >= goal
    color = "green" if achieved else "red"
    st.markdown(
        f"📅 **{row['date']}** → "
        f"<span style='color:{color}; font-weight:bold;'>{row['amount']} ml</span> "
        f"/ {goal} ml",
        unsafe_allow_html=True
    )

# ----------------------------------
# WEEKLY WATER INTAKE TREND
# ----------------------------------
st.subheader("📉 Weekly Water Intake Trend")

df = water_data.copy()

if not df.empty:
    df["date"] = pd.to_datetime(df["date"])

    today = datetime.date.today()
    last_7_days = [today - datetime.timedelta(days=i) for i in range(6, -1, -1)]

    weekly_data = []
    for d in last_7_days:
        total = df[df["date"].dt.date == d]["amount"].sum()
        weekly_data.append(total)

    # Plot chart
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(last_7_days, weekly_data, marker="o")

    # Highlight today
    today_index = last_7_days.index(today)
    ax.plot(
        last_7_days[today_index],
        weekly_data[today_index],
        marker="o",
        markersize=12,
        color="red"
    )

    # Goal line (3000 ml)
    ax.axhline(3000, linestyle="--", linewidth=1.5, color="gray")

    ax.set_title("Weekly Water Intake Trend (Goal = 3000 ml)")
    ax.set_ylabel("Water Intake (ml)")
    ax.set_xlabel("Date")
    plt.xticks(rotation=45)

    st.pyplot(fig)

else:
    st.info("Add water logs to show weekly trend.")

# ----------------------------------
# PIE CHART: DATE WISE DISTRIBUTION
# ----------------------------------
st.subheader("🥤 Daily Intake vs Goal")

if not daily_total.empty:
    for _, row in daily_total.iterrows():
        day = str(row["date"])
        intake = row["amount"]
        goal = 3000
        remaining = max(goal - intake, 0)

        fig, ax = plt.subplots(figsize=(5,5))
        ax.pie(
            [intake, remaining],
            labels=[f"Intake: {intake} ml", f"Remaining: {remaining} ml"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax.set_title(f"Water Intake Percentage for {day}")

        st.pyplot(fig)

else:
    st.info("No data available for pie chart.")