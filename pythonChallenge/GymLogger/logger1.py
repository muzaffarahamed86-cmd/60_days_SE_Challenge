import streamlit as st
import pandas as pd
from datetime import date, datetime
import altair as alt

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Gym Workout Logger",
    page_icon="🏋️‍♂️",
    layout="wide",
)


# --------------------------------------------------
# Helpers: session state & data
# --------------------------------------------------
def init_session_state():
    """Initialize the workouts DataFrame in session_state."""
    if "workouts" not in st.session_state:
        st.session_state.workouts = pd.DataFrame(
            columns=[
                "date",
                "name",
                "exercise",
                "sets",
                "reps",
                "weight",
                "volume",
            ]
        )


def add_workout_entry(date_value, name, exercise, sets, reps, weight):
    """Add a single workout entry to the session_state DataFrame."""
    volume = float(sets) * float(reps) * float(weight)

    new_row = pd.DataFrame(
        {
            "date": [pd.to_datetime(date_value)],
            "name": [name.strip()],
            "exercise": [exercise.strip()],
            "sets": [int(sets)],
            "reps": [int(reps)],
            "weight": [float(weight)],
            "volume": [volume],
        }
    )

    st.session_state.workouts = pd.concat(
        [st.session_state.workouts, new_row], ignore_index=True
    )

    return volume


def load_sample_data():
    demo = [
        ("2025-10-20", "Alex", "Bench Press", 4, 8, 60),
        ("2025-10-27", "Alex", "Squat", 5, 5, 80),
        ("2025-11-03", "Muz", "Deadlift", 3, 5, 100),
        ("2025-11-10", "Muz", "Shoulder Press", 3, 10, 20),
        ("2025-11-17", "Alex", "Lat Pulldown", 4, 12, 40),
    ]

    rows = []
    for d, n, ex, s, r, w in demo:
        volume = s * r * w
        rows.append(
            {
                "date": pd.to_datetime(d),
                "name": n,
                "exercise": ex,
                "sets": s,
                "reps": r,
                "weight": float(w),
                "volume": float(volume),
            }
        )

    st.session_state.workouts = pd.DataFrame(rows)



def get_weekly_volume(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate total volume per week."""
    if df.empty:
        return pd.DataFrame(columns=["week_start", "total_volume"])

    temp = df.copy()
    temp["date"] = pd.to_datetime(temp["date"])
    temp = temp.set_index("date")

    weekly = (
        temp["volume"]
        .resample("W-MON")
        .sum()
        .reset_index()
    )
    weekly.rename(columns={"date": "week_start", "volume": "total_volume"}, inplace=True)
    return weekly


# --------------------------------------------------
# UI helpers
# --------------------------------------------------
def inject_css():
    st.markdown(
        """
        <style>
        .main {
            background-color: #f7f8fa;
        }
        .app-header h1 {
            font-size: 2.3rem;
            margin-bottom: 0.2rem;
        }
        .app-header p {
            color: #6b7280;
            margin-top: 0;
        }
        .card {
            background-color: #ffffff;
            padding: 1.25rem 1.5rem;
            border-radius: 0.9rem;
            border: 1px solid #e5e7eb;
            box-shadow: 0 2px 4px rgba(15,23,42,0.04);
        }
        .section-title {
            font-weight: 600;
            font-size: 1.05rem;
            margin-bottom: 0.3rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    st.markdown(
        """
        <div class="app-header">
            <h1>🏋️‍♂️ Gym Workout Logger</h1>
            <p>Log your workouts, track weekly volume, and visualize your progress over time.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_log_form():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">➕ Log a new workout</div>', unsafe_allow_html=True)

    with st.form("log_form", clear_on_submit=True):
        row1_col1, row1_col2 = st.columns([1, 1])
        with row1_col1:
            date_value = st.date_input("Date", value=date.today())
        with row1_col2:
            name = st.text_input("Name", placeholder="Your name")

        row2_col1, row2_col2 = st.columns([2, 1])
        with row2_col1:
            exercise = st.text_input("Exercise", placeholder="e.g. Bench Press")
        with row2_col2:
            sets = st.number_input("Sets", min_value=1, value=3)

        row3_col1, row3_col2 = st.columns([1, 1])
        with row3_col1:
            reps = st.number_input("Reps", min_value=1, value=10)
        with row3_col2:
            weight = st.number_input("Weight (kg)", min_value=0.0, value=20.0, step=0.5)

        submit, sample = st.columns([1, 1])
        submitted = submit.form_submit_button("Add workout")
        load_demo_clicked = sample.form_submit_button("Load sample data")

        if load_demo_clicked:
            load_sample_data()
            st.success("Sample data loaded.")

        if submitted:
            if not name or not exercise:
                st.warning("Please fill in Name and Exercise.")
            else:
                volume = add_workout_entry(date_value, name, exercise, sets, reps, weight)
                st.success(
                    f"Added: {exercise} — {sets} × {reps} @ {weight} kg (volume: {volume:.1f})"
                )

    st.markdown("</div>", unsafe_allow_html=True)


def render_summary_cards(df):
    total_logs = len(df)
    total_volume = df["volume"].sum() if not df.empty else 0
    total_exercises = df["exercise"].nunique() if not df.empty else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Total logs", total_logs)
    c2.metric("Total volume (kg)", f"{total_volume:,.1f}")
    c3.metric("Exercises logged", total_exercises)


def render_log_table(df):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Recent workout logs</div>', unsafe_allow_html=True)

    if df.empty:
        st.info("No logs yet.")
    else:
        df_display = df.copy().sort_values("date", ascending=False)
        df_display["date"] = df_display["date"].dt.date
        st.dataframe(df_display, hide_index=True, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


def render_weekly_chart(df):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Weekly volume progress</div>', unsafe_allow_html=True)

    weekly = get_weekly_volume(df)

    if weekly.empty:
        st.info("Log workouts to see weekly progress.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # Ensure correct datetime format
    weekly["week_start"] = pd.to_datetime(weekly["week_start"])

    chart = (
        alt.Chart(weekly)
        .mark_area(
            line={"color": "#3b82f6", "strokeWidth": 3},
            color=alt.Gradient(
                gradient="linear",
                stops=[
                    {"offset": 0, "color": "#3b82f622"},
                    {"offset": 1, "color": "#3b82f600"},
                ],
                x1=0, x2=0, y1=1, y2=0,
            ),
        )
        .encode(
            x=alt.X("week_start:T", title="Week Starting"),
            y=alt.Y("total_volume:Q", title="Total Volume (kg)"),
            tooltip=[
                alt.Tooltip("week_start:T", title="Week"),
                alt.Tooltip("total_volume:Q", title="Volume (kg)"),
            ],
        )
        .properties(height=300)
    )

    st.altair_chart(chart, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------------------------
# Main App
# --------------------------------------------------
def main():
    inject_css()
    init_session_state()

    render_header()

    form_col, summary_col = st.columns([2, 1])
    with form_col:
        render_log_form()
    with summary_col:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Summary</div>', unsafe_allow_html=True)
        render_summary_cards(st.session_state.workouts)
        st.markdown("</div>", unsafe_allow_html=True)

    table_col, chart_col = st.columns([1.4, 1.6])
    with table_col:
        render_log_table(st.session_state.workouts)
    with chart_col:
        render_weekly_chart(st.session_state.workouts)


if __name__ == "__main__":
    main()
