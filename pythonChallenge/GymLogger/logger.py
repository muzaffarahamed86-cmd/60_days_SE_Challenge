import streamlit as st
import pandas as pd
from datetime import date, datetime

# =========================================================
# Gym Workout Logger 🏋️‍♂️
# =========================================================
# RTCFR PROMPT EMBEDDED AS COMMENTS
# R (Role):   You are a Python + Streamlit workout logging app.
# T (Task):   Collect workout data, calculate total volume, store it, and show progress.
# C (Context): Beginner-friendly gym logger; no external database; single-page app.
# F (Format): Clean UI with form, table, and weekly progress graph.
# R (Rules):  Use st.session_state or pandas, calculate sets*reps*weight, update graph live.
# =========================================================


# ---------- Helpers: Session State & Data ----------

def init_session_state():
    """Initialize session_state for workout logs."""
    if "workout_logs" not in st.session_state:
        st.session_state.workout_logs = []  # list of dict rows


def add_log(exercise: str, sets: int, reps: int, weight: float, log_date: date):
    """Add a new workout log entry to session_state."""
    total_volume = sets * reps * weight

    st.session_state.workout_logs.append(
        {
            "Date": log_date,
            "Exercise": exercise,
            "Sets": sets,
            "Reps": reps,
            "Weight": weight,
            "Total Volume": total_volume,
        }
    )


def get_logs_df() -> pd.DataFrame:
    """Return the workout logs as a pandas DataFrame."""
    if "workout_logs" not in st.session_state or len(st.session_state.workout_logs) == 0:
        return pd.DataFrame(
            columns=["Date", "Exercise", "Sets", "Reps", "Weight", "Total Volume"]
        )
    df = pd.DataFrame(st.session_state.workout_logs)
    # Ensure Date is datetime-like for plotting
    df["Date"] = pd.to_datetime(df["Date"])
    return df


def load_sample_data():
    """Load some example workout data into session_state."""
    sample_logs = [
        {"Date": date(2025, 11, 17), "Exercise": "Squat",    "Sets": 4, "Reps": 8, "Weight": 80, "Total Volume": 4 * 8 * 80},
        {"Date": date(2025, 11, 18), "Exercise": "Bench",    "Sets": 3, "Reps": 10, "Weight": 60, "Total Volume": 3 * 10 * 60},
        {"Date": date(2025, 11, 19), "Exercise": "Deadlift", "Sets": 3, "Reps": 5, "Weight": 100,"Total Volume": 3 * 5 * 100},
        {"Date": date(2025, 11, 20), "Exercise": "OHP",      "Sets": 3, "Reps": 8, "Weight": 40, "Total Volume": 3 * 8 * 40},
        {"Date": date(2025, 11, 20), "Exercise": "Row",      "Sets": 4, "Reps": 10,"Weight": 50, "Total Volume": 4 * 10 * 50},
    ]
    st.session_state.workout_logs = sample_logs


# ---------- UI Components ----------

def render_header():
    st.title("🏋️‍♂️ Gym Workout Logger")
    st.caption(
        "Log your exercises, track total volume, and see your weekly progress. "
        "Beginner-friendly, no external database."
    )
    st.markdown("---")


def render_sidebar():
    with st.sidebar:
        st.header("⚙️ Options")
        st.write("Use these controls for quick testing or resetting the app.")

        if st.button("Load sample data"):
            load_sample_data()
            st.success("Sample data loaded!")

        if st.button("Clear all logs"):
            st.session_state.workout_logs = []
            st.info("All logs cleared.")

        st.markdown("---")
        st.markdown(
            "**Tips:**\n"
            "- Log consistently.\n"
            "- Watch your total volume trend over weeks.\n"
            "- Use meaningful exercise names (e.g., `Back Squat`, `Incline Bench`)."
        )


def render_log_form():
    st.subheader("📝 Add New Workout Log")

    with st.form("log_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            exercise = st.text_input("Exercise name", placeholder="e.g., Squat")
            log_date = st.date_input("Date", value=date.today())
        with col2:
            sets = st.number_input("Sets", min_value=1, max_value=20, value=3, step=1)
            reps = st.number_input("Reps", min_value=1, max_value=50, value=10, step=1)
            weight = st.number_input(
                "Weight per rep (kg)", min_value=0.0, max_value=1000.0, value=50.0, step=2.5
            )

        submitted = st.form_submit_button("Add to log")

        if submitted:
            if not exercise.strip():
                st.error("Please enter an exercise name.")
            else:
                add_log(exercise.strip(), int(sets), int(reps), float(weight), log_date)
                total_volume = int(sets) * int(reps) * float(weight)
                st.success(
                    f"Added: **{exercise}** | {sets}×{reps} @ {weight} kg "
                    f"(Total volume: **{total_volume}**) "
                    f"on {log_date.strftime('%Y-%m-%d')}."
                )


def render_logs_table(df: pd.DataFrame):
    st.subheader("📋 Logged Workouts")

    if df.empty:
        st.info("No workouts logged yet. Add your first entry above!")
        return

    # Sort by Date (descending) and show latest first
    df_sorted = df.sort_values("Date", ascending=False).reset_index(drop=True)

    st.dataframe(
        df_sorted,
        use_container_width=True,
        hide_index=True,
    )


def render_weekly_progress(df: pd.DataFrame):
    st.subheader("📈 Weekly Volume Progress")

    if df.empty:
        st.info("Not enough data yet. Add some logs to see your weekly progress.")
        return

    # Group by week (starting on Monday) and sum total volume
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    weekly = (
        df.groupby(pd.Grouper(key="Date", freq="W-MON"))["Total Volume"]
        .sum()
        .reset_index()
        .sort_values("Date")
    )

    if weekly.empty:
        st.info("No weekly data available yet.")
        return

    weekly = weekly.set_index("Date")

    st.line_chart(weekly["Total Volume"])

    # Small stats
    total_volume_all = int(df["Total Volume"].sum())
    last_week_volume = int(weekly["Total Volume"].iloc[-1])
    st.markdown(
        f"- **Total logged volume:** {total_volume_all}\n"
        f"- **Last week volume:** {last_week_volume}"
    )


# ---------- Main App ----------

def main():
    st.set_page_config(
        page_title="Gym Workout Logger",
        page_icon="🏋️‍♂️",
        layout="centered",
    )

    init_session_state()
    render_header()
    render_sidebar()

    # Layout main area
    st.markdown("### 🧱 Log & Review")
    log_col, table_col = st.columns((1, 1.2))

    with log_col:
        render_log_form()

    with table_col:
        df = get_logs_df()
        render_logs_table(df)

    st.markdown("---")
    render_weekly_progress(df)


if __name__ == "__main__":
    main()
