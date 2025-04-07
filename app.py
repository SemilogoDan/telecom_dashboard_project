import pandas as pd
import streamlit as st
import plotly.express as px

# Load the data dynamically via file upload
st.title("📡 Telecom Site Monitoring Dashboard")
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Attempt to load the CSV file
        df = pd.read_csv(uploaded_file)

        # Debugging: Print column names
        # st.write("Columns in the uploaded file:", df.columns)

        # Parse the 'timestamp' column as datetime (automatically detect format)
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], format='ISO8601', errors='coerce')
            if df['timestamp'].isnull().any():
                st.error("Some rows in the 'timestamp' column could not be parsed as dates. Please check the data.")
        else:
            st.error("No 'timestamp' column found in the uploaded file.")
            st.stop()

    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

    # Validate required columns
    expected_columns = ['site_id', 'timestamp', 'uptime', 'energy_consumption', 'alarm_count', 'signal_strength']
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Missing required columns: {missing_columns}")
        st.stop()

    # Sidebar filters
    st.sidebar.header("📊 Filter Data")
    selected_site = st.sidebar.selectbox("Select Site", options=df['site_id'].unique())

    # Validate date range
    if df.empty:
        st.error("No data available to filter.")
    else:
        date_range = st.sidebar.date_input(
            "Select Date Range",
            [df['timestamp'].min().date(), df['timestamp'].max().date()]
        )

        if len(date_range) == 2:
            start_date, end_date = date_range
        else:
            st.warning("Please select a valid date range.")
            start_date, end_date = df['timestamp'].min().date(), df['timestamp'].max().date()

        # Filter dataset
        filtered_df = df[
            (df['site_id'] == selected_site) &
            (df['timestamp'] >= pd.to_datetime(start_date)) &
            (df['timestamp'] <= pd.to_datetime(end_date))
        ]

        # Main Dashboard
        st.markdown(f"### Site: **{selected_site}**")

        # Metrics
        col1, col2 = st.columns(2)
        avg_uptime = filtered_df['uptime'].mean() if not filtered_df.empty else 0
        col1.metric("🔌 Avg Uptime (%)", f"{avg_uptime:.2f}")

        total_energy = filtered_df['energy_consumption'].sum() if not filtered_df.empty else 0
        col2.metric("⚡ Total Energy Consumption (kWh)", f"{total_energy:.1f}")

        col3, col4 = st.columns(2)
        total_alarms = filtered_df['alarm_count'].sum() if not filtered_df.empty else 0
        col3.metric("🚨 Total Alarms", f"{total_alarms}")

        avg_signal = filtered_df['signal_strength'].mean() if not filtered_df.empty else 0
        col4.metric("📶 Avg Signal Strength (dBm)", f"{avg_signal:.1f}")

        # Charts
        if not filtered_df.empty:
            st.plotly_chart(
                px.line(filtered_df, x='timestamp', y='uptime', title='📈 Uptime Over Time'),
                use_container_width=True
            )
            st.plotly_chart(
                px.bar(filtered_df, x='timestamp', y='energy_consumption', title='⚡ Energy Consumption Over Time'),
                use_container_width=True
            )
        else:
            st.warning("No data available to plot after filtering.")
else:
    st.info("Please upload a valid CSV file to proceed.")