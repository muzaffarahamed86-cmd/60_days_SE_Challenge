import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import openai

# --------------------------
# APP CONFIG
# --------------------------
st.set_page_config(page_title="🧠 AI Data Analyzer", layout="wide")
st.title("🧠 AI Data Analyzer")
st.write("Upload your CSV file and let AI analyze it automatically.")

# --------------------------
# SIDEBAR CONFIG
# --------------------------
st.sidebar.header("⚙️ Configuration")
openai_api_key = st.sidebar.text_input("Enter OpenAI API Key (Optional)", type="password")

# --------------------------
# FILE UPLOAD
# --------------------------
uploaded_file = st.file_uploader("📂 Upload a CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()
    
    st.success("✅ File uploaded successfully!")
    
    # --------------------------
    # DATA PREVIEW
    # --------------------------
    st.subheader("📊 Data Preview")
    st.dataframe(df.head(10), use_container_width=True)
    st.markdown(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")

    # --------------------------
    # DATA INFO
    # --------------------------
    st.subheader("🔍 Data Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Column Types:**")
        st.dataframe(pd.DataFrame(df.dtypes, columns=["Data Type"]))
    with col2:
        st.write("**Missing Values:**")
        st.dataframe(pd.DataFrame(df.isnull().sum(), columns=["Missing Count"]))
    
    # --------------------------
    # NUMERIC SUMMARY
    # --------------------------
    st.subheader("📈 Statistical Summary")
    st.dataframe(df.describe().T)

    # --------------------------
    # CORRELATION ANALYSIS
    # --------------------------
    numeric_df = df.select_dtypes(include=[np.number])
    if not numeric_df.empty:
        st.subheader("🧮 Correlation Heatmap")
        corr = numeric_df.corr()
        fig_corr = px.imshow(
            corr, text_auto=True, aspect="auto",
            title="Correlation Matrix", color_continuous_scale="RdBu_r"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.warning("No numeric columns available for correlation heatmap.")

    # --------------------------
    # VISUALIZATION TOOL
    # --------------------------
    st.subheader("📊 Quick Visualization")
    all_cols = df.columns.tolist()
    x_axis = st.selectbox("X-Axis", all_cols)
    y_axis = st.selectbox("Y-Axis", all_cols)
    chart_type = st.radio("Chart Type", ["Scatter", "Bar", "Box", "Histogram"], horizontal=True)

    if st.button("Generate Chart"):
        try:
            if chart_type == "Scatter":
                fig = px.scatter(df, x=x_axis, y=y_axis, color=x_axis, title=f"{y_axis} vs {x_axis}")
            elif chart_type == "Bar":
                fig = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
            elif chart_type == "Box":
                fig = px.box(df, x=x_axis, y=y_axis, title=f"Distribution of {y_axis} by {x_axis}")
            elif chart_type == "Histogram":
                fig = px.histogram(df, x=x_axis, title=f"Histogram of {x_axis}")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error generating chart: {e}")
        # --------------------------
    # AUTO CHART GENERATOR
    # --------------------------
    st.subheader("🤖 Auto Chart Generator (AI decides best chart)")

    if st.button("Generate Auto Chart"):
        try:
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            categorical_cols = df.select_dtypes(exclude=np.number).columns.tolist()

            # Basic logic to decide chart type
            chart_type = None
            x_col, y_col = None, None

            if len(numeric_cols) == 1 and len(categorical_cols) == 0:
                chart_type = "Histogram"
                x_col = numeric_cols[0]
            elif len(numeric_cols) >= 2:
                chart_type = "Scatter"
                x_col, y_col = numeric_cols[:2]
            elif len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
                chart_type = "Bar"
                x_col, y_col = categorical_cols[0], numeric_cols[0]
            elif len(categorical_cols) >= 1:
                chart_type = "Pie"
                x_col = categorical_cols[0]
            else:
                st.warning("Not enough data variety for auto charting.")
                chart_type = None

            if chart_type == "Histogram":
                fig = px.histogram(df, x=x_col, title=f"📊 Auto: Histogram of {x_col}")
            elif chart_type == "Scatter":
                fig = px.scatter(df, x=x_col, y=y_col, title=f"📈 Auto: {y_col} vs {x_col}")
            elif chart_type == "Bar":
                fig = px.bar(df, x=x_col, y=y_col, title=f"📊 Auto: {y_col} by {x_col}")
            elif chart_type == "Pie":
                pie_counts = df[x_col].value_counts().reset_index()
                pie_counts.columns = [x_col, "count"]
                fig = px.pie(pie_counts, names=x_col, values="count", title=f"🥧 Auto: Distribution of {x_col}")
            else:
                fig = None

            if fig:
                st.plotly_chart(fig, use_container_width=True)

                # Optional AI Explanation (if key provided)
                if openai_api_key:
                    openai.api_key = openai_api_key
                    prompt = f"""
                    You are a data visualization expert.
                    The dataset columns are: {list(df.columns)}.
                    The chosen chart type is: {chart_type}.
                    Explain briefly why this chart type is appropriate
                    and what kind of insight a user might get from it.
                    """

                    with st.spinner("🤖 AI explaining chart choice..."):
                        try:
                            response = openai.ChatCompletion.create(
                                model="gpt-3.5-turbo",
                                messages=[
                                    {"role": "system", "content": "You are a professional data visualization coach."},
                                    {"role": "user", "content": prompt}
                                ],
                                max_tokens=120,
                                temperature=0.4,
                            )
                            explanation = response["choices"][0]["message"]["content"]
                            st.info(f"💡 {explanation}")
                        except Exception as e:
                            st.warning(f"AI explanation failed: {e}")
                else:
                    st.caption("💡 Add your OpenAI key to get AI explanations for chart selection.")

        except Exception as e:
            st.error(f"Error in Auto Chart Generator: {e}")


    # --------------------------
    # AI INSIGHTS (OPTIONAL)
    # --------------------------
    st.subheader("🤖 AI Insights")

    if openai_api_key:
        openai.api_key = openai_api_key
        st.info("AI is analyzing your dataset. This may take a few seconds...")

        sample_data = df.head(20).to_csv(index=False)
        prompt = f"""
        You are a data analyst. Analyze the following CSV data and give key insights in bullet points.
        Focus on:
        - Data quality issues
        - Distribution observations
        - Correlations or patterns
        - Possible business insights

        Data:
        {sample_data}
        """

        if st.button("Generate AI Insights"):
            with st.spinner("Generating insights using OpenAI..."):
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are an expert data analyst."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=300,
                        temperature=0.3,
                    )
                    insights = response["choices"][0]["message"]["content"]
                    st.markdown("### 📋 Key AI Insights")
                    st.success(insights)
                except Exception as e:
                    st.error(f"OpenAI API call failed: {e}")
    else:
        st.info("💡 Enter an OpenAI API key in the sidebar to get AI-generated insights.")

else:
    st.info("👆 Upload a CSV file to begin analysis.")
