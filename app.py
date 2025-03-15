import streamlit as st
import pandas as pd

# Streamlit Page Title
st.title("📊 System Logs Analysis Dashboard")

# Upload CSV file
uploaded_file = st.file_uploader("📂 Upload Log File", type=["csv", "xls"])

if uploaded_file is not None:
    # Read CSV file
    df = pd.read_csv(uploaded_file)

    # Ensure column names are cleaned
    df.columns = df.columns.str.strip()

    # Convert timestamp column
    df["Time Stamp"] = pd.to_datetime(df["Time Stamp"], errors="coerce", format="%y-%m-%d %H:%M:%S")

    # Drop rows where timestamp conversion failed
    df = df.dropna(subset=["Time Stamp"])

    # Set timestamp as index
    df.set_index("Time Stamp", inplace=True)
    df = df.sort_index()

    # Extract log level
    df["log_level"] = df["Info"].str.extract(r"(INFO|WARN|ERROR)")

    # Resample logs daily
    df_daily = df.resample("D").count()

    # Set correct min/max dates
    if not df.empty:
        min_date = df.index.min()
        max_date = df.index.max()
    else:
        min_date = pd.to_datetime("2023-01-01")
        max_date = pd.to_datetime("2023-12-31")

    # Date Selection
    st.subheader("📅 Select Date Range for Analysis")
    start_date, end_date = st.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

    # Convert to datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Apply date filtering
    df_filtered = df.loc[start_date:end_date]

    if df_filtered.empty:
        st.warning("No logs found in the selected date range.")
    else:
        # Log Level Distribution
        st.subheader("📌 Log Level Distribution")
        log_counts = df_filtered["log_level"].value_counts()

        # Using Streamlit's bar chart to visualize log level distribution
        st.bar_chart(log_counts)

        # Daily Log Trends
        st.subheader("📈 Daily Log Trends")
        df_daily_filtered = df_filtered.resample("D").count()

        # Using Streamlit's line chart to visualize daily log trends
        st.line_chart(df_daily_filtered["log_level"])

        # Show recent logs
        st.subheader("📜 Recent Log Entries")
        st.dataframe(df_filtered.tail(10))
