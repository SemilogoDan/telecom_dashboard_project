import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np
import os
import json

# File to store user data
USER_FILE = "users.json"

# Load existing users or initialize an empty dictionary
if os.path.exists(USER_FILE):
    with open(USER_FILE, "r") as f:
        users = json.load(f)
else:
    users = {}

# Save users to file
def save_users():
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# Initialize session state for login/logout
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None

# Registration Form
st.sidebar.header("📝 Register")
new_username = st.sidebar.text_input("New Username", key="reg_username")
new_password = st.sidebar.text_input("New Password", type="password", key="reg_password")
new_role = st.sidebar.selectbox("Role", ["admin", "engineer", "manager"], key="reg_role")

if st.sidebar.button("Register"):
    if new_username and new_password:
        if new_username in users:
            st.sidebar.error("Username already exists!")
        else:
            users[new_username] = {"password": new_password, "role": new_role}
            save_users()
            st.sidebar.success("Registration successful! You can now log in.")

# Login Form
st.sidebar.header("🔒 Login")
username = st.sidebar.text_input("Username", key="login_username")
password = st.sidebar.text_input("Password", type="password", key="login_password")

if st.sidebar.button("Login"):
    if username and password:
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.sidebar.success(f"Logged in as {st.session_state.role.upper()}")
        else:
            st.sidebar.error("Invalid credentials")
    else:
        st.sidebar.warning("Please enter both username and password.")

# Logout Button
if st.session_state.logged_in:
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.rerun()  # Restart the app to reflect logout

# Main App
if st.session_state.logged_in:
    role = st.session_state.role
    st.title(f"📡 Telecom Site Monitoring Dashboard ({role.capitalize()})")

    # File Upload
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            # Load data
            df = pd.read_csv(uploaded_file)

            # Parse the 'timestamp' column as datetime
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

            # Role-Based Interface Customization
            if role == "admin":
                # Admin View: Full access
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

                # Alerts Section
                st.subheader("🚨 Alerts")
                uptime_threshold = 95.0
                energy_consumption_threshold = 700.0
                alarm_count_threshold = 5

                low_uptime = filtered_df[filtered_df['uptime'] < uptime_threshold]
                high_energy = filtered_df[filtered_df['energy_consumption'] > energy_consumption_threshold]
                high_alarms = filtered_df[filtered_df['alarm_count'] > alarm_count_threshold]

                if not low_uptime.empty:
                    st.warning(f"⚠️ Low Uptime Detected: {len(low_uptime)} occurrences below {uptime_threshold}%")
                if not high_energy.empty:
                    st.warning(f"⚠️ High Energy Consumption Detected: {len(high_energy)} occurrences above {energy_consumption_threshold} kWh")
                if not high_alarms.empty:
                    st.warning(f"⚠️ High Alarm Count Detected: {len(high_alarms)} occurrences above {alarm_count_threshold}")

                # Predictive Analytics Section
                st.subheader("🔮 Predictive Analytics")

                if not filtered_df.empty:
                    X = np.array(range(len(filtered_df))).reshape(-1, 1)
                    y_uptime = filtered_df['uptime'].values
                    y_energy = filtered_df['energy_consumption'].values

                    model_uptime = LinearRegression().fit(X, y_uptime)
                    model_energy = LinearRegression().fit(X, y_energy)

                    next_index = len(filtered_df)
                    predicted_uptime = model_uptime.predict(np.array([[next_index]]))[0]
                    predicted_energy = model_energy.predict(np.array([[next_index]]))[0]

                    col1, col2 = st.columns(2)
                    col1.metric("Predicted Uptime (%)", f"{predicted_uptime:.2f}")
                    col2.metric("Predicted Energy Consumption (kWh)", f"{predicted_energy:.1f}")
                else:
                    st.warning("No data available for predictive analytics.")

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

            elif role == "engineer":
                # Engineer View: Detailed metrics but limited to their site
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

                # Alerts Section
                st.subheader("🚨 Alerts")
                uptime_threshold = 95.0
                energy_consumption_threshold = 700.0
                alarm_count_threshold = 5

                low_uptime = filtered_df[filtered_df['uptime'] < uptime_threshold]
                high_energy = filtered_df[filtered_df['energy_consumption'] > energy_consumption_threshold]
                high_alarms = filtered_df[filtered_df['alarm_count'] > alarm_count_threshold]

                if not low_uptime.empty:
                    st.warning(f"⚠️ Low Uptime Detected: {len(low_uptime)} occurrences below {uptime_threshold}%")
                if not high_energy.empty:
                    st.warning(f"⚠️ High Energy Consumption Detected: {len(high_energy)} occurrences above {energy_consumption_threshold} kWh")
                if not high_alarms.empty:
                    st.warning(f"⚠️ High Alarm Count Detected: {len(high_alarms)} occurrences above {alarm_count_threshold}")

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

            elif role == "manager":
                # Manager View: Summary metrics only
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

                # Alerts Section
                st.subheader("🚨 Alerts")
                uptime_threshold = 95.0
                energy_consumption_threshold = 700.0
                alarm_count_threshold = 5

                low_uptime = filtered_df[filtered_df['uptime'] < uptime_threshold]
                high_energy = filtered_df[filtered_df['energy_consumption'] > energy_consumption_threshold]
                high_alarms = filtered_df[filtered_df['alarm_count'] > alarm_count_threshold]

                if not low_uptime.empty:
                    st.warning(f"⚠️ Low Uptime Detected: {len(low_uptime)} occurrences below {uptime_threshold}%")
                if not high_energy.empty:
                    st.warning(f"⚠️ High Energy Consumption Detected: {len(high_energy)} occurrences above {energy_consumption_threshold} kWh")
                if not high_alarms.empty:
                    st.warning(f"⚠️ High Alarm Count Detected: {len(high_alarms)} occurrences above {alarm_count_threshold}")
    else:
        st.info("Please upload a valid CSV file to proceed.")
else:
    st.info("Please log in to proceed.")