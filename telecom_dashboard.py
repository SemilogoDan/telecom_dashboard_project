import pandas as pd
import streamlit as st

import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np
import os
import json
import re  # For password strength check

# File to store user data
USER_FILE = "users.json"
REMEMBER_FILE = "remember.json"

# Load existing users or initialize an empty dictionary
if os.path.exists(USER_FILE):
    with open(USER_FILE, "r") as f:
        users = json.load(f)
else:
    users = {}

# Load remembered user
if os.path.exists(REMEMBER_FILE):
    with open(REMEMBER_FILE, "r") as f:
        remembered = json.load(f)
else:
    remembered = {}

# Save users to file
def save_users():
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# Save remember me choice
def save_remember():
    with open(REMEMBER_FILE, "w") as f:
        json.dump(remembered, f)

# Function to check password strength
def check_password_strength(password):
    if len(password) < 6:
        return "Password must be at least 6 characters long."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Password must contain at least one special character."
    return None

# Initialize session state for login/logout and data
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.uploaded_file = None
    st.session_state.df = pd.DataFrame()
    st.session_state.filtered_df = pd.DataFrame()
    st.session_state.selected_site = None
    st.session_state.date_range = None

# Initialize theme state
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

st.sidebar.button("Toggle Light/Dark Mode", on_click=toggle_theme)

# Apply theme
if st.session_state.theme == "dark":
    st.markdown(
        """
        <style>
        body {
            color: white;
            background-color: #1a1a1a;
        }
        .stApp {
            background-color: #1a1a1a;
        }
        .stSidebar {
            background-color: #262730;
            color: white;
        }
        .stButton>button {
            color: white;
            background-color: #4a4a59;
            border-color: #4a4a59;
        }
        .stTextInput>div>div>input {
            color: white;
            background-color: #333333;
            border-color: #555555;
        }
        .stSelectbox>div>div>div>div {
            color: white;
            background-color: #333333;
            border-color: #555555;
        }
        .stError {
            color: #e87979;
        }
        .stSuccess {
            color: #68d391;
        }
        .stWarning {
            color: #f6e05e;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
        </style>
        """,
        unsafe_allow_html=True,
    )

# Registration Form
st.sidebar.header(" Register")
new_username = st.sidebar.text_input("New Username", key="reg_username")
new_password = st.sidebar.text_input("New Password", type="password", key="reg_password")
new_role = st.sidebar.selectbox("Role", ["admin", "engineer", "manager"], key="reg_role")

if st.sidebar.button("Register"):
    password_strength_error = check_password_strength(new_password)
    if password_strength_error:
        st.sidebar.error(password_strength_error)
    elif new_username and new_password:
        if new_username in users:
            st.sidebar.error("Username already exists!")
        else:
            users[new_username] = {"password": new_password, "role": new_role}
            save_users()
            st.sidebar.success("Registration successful! You can now log in.")

# Login Form
st.sidebar.header(" Login")
username = st.sidebar.text_input("Username", key="login_username", value=remembered.get("username", ""))
password = st.sidebar.text_input("Password", type="password", key="login_password", value=remembered.get("password", ""))
remember_me = st.sidebar.checkbox("Remember me", value=bool(remembered))

if st.sidebar.button("Login"):
    if username and password:
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.sidebar.success(f"Logged in as {st.session_state.role.upper()}")
            if remember_me:
                remembered["username"] = username
                remembered["password"] = password
            else:
                remembered.pop("username", None)
                remembered.pop("password", None)
            save_remember()
            st.rerun() # Rerun to update the UI
        else:
            st.sidebar.error("Invalid credentials")
    else:
        st.sidebar.warning("Please enter both username and password.")

# Auto-login if "remember me" was checked and details are saved
if not st.session_state.logged_in and remembered.get("username") and remembered.get("password"):
    if remembered["username"] in users and users[remembered["username"]]["password"] == remembered["password"]:
        st.session_state.logged_in = True
        st.session_state.username = remembered["username"]
        st.session_state.role = users[remembered["username"]]["role"]
        st.sidebar.success(f"Logged in automatically as {st.session_state.role.upper()}")
        st.rerun() # Rerun to update the UI

# Logout Button
if st.session_state.logged_in:
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.session_state.uploaded_file = None
        st.session_state.df = pd.DataFrame()
        st.session_state.filtered_df = pd.DataFrame()
        st.session_state.selected_site = None
        st.session_state.date_range = None
        st.rerun()  # Restart the app to reflect logout and reset data

# Main App
if st.session_state.logged_in:
    role = st.session_state.role
    st.title(f"📡 Telecom Site Monitoring Dashboard ({role.capitalize()})")

    # File Upload
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="file_uploader")

    if uploaded_file is not None:
        if st.session_state.uploaded_file != uploaded_file:
            st.session_state.uploaded_file = uploaded_file
            try:
                # Load data
                st.session_state.df = pd.read_csv(uploaded_file)

                # Parse the 'timestamp' column as datetime
                if 'timestamp' in st.session_state.df.columns:
                    st.session_state.df['timestamp'] = pd.to_datetime(st.session_state.df['timestamp'], format='ISO8601', errors='coerce')
                    if st.session_state.df['timestamp'].isnull().any():
                        st.error("Some rows in the 'timestamp' column could not be parsed as dates. Please check the data.")
                        st.session_state.df = pd.DataFrame() # Reset df on error
                else:
                    st.error("No 'timestamp' column found in the uploaded file.")
                    st.session_state.df = pd.DataFrame() # Reset df on error
                    st.stop()
            except Exception as e:
                st.error(f"Error loading data: {e}")
                st.session_state.df = pd.DataFrame() # Reset df on error
                st.stop()

            # Validate required columns
            expected_columns = ['site_id', 'timestamp', 'uptime', 'energy_consumption', 'alarm_count', 'signal_strength']
            missing_columns = [col for col in expected_columns if col not in st.session_state.df.columns]
            if missing_columns:
                st.error(f"Missing required columns: {missing_columns}")
                st.session_state.df = pd.DataFrame() # Reset df on error
                st.stop()
        else:
            df = st.session_state.df # Use cached df

        if not st.session_state.df.empty:
            # Sidebar filters
            st.sidebar.header(" Filter Data")
            all_sites = st.session_state.df['site_id'].unique()
            default_site = st.session_state.selected_site if st.session_state.selected_site in all_sites else all_sites[0] if len(all_sites) > 0 else None
            st.session_state.selected_site = st.sidebar.selectbox("Select Site", options=all_sites, index=all_sites.tolist().index(default_site) if default_site else 0)

            if not st.session_state.df.empty:
                min_date = st.session_state.df['timestamp'].min().date()
                max_date = st.session_state.df['timestamp'].max().date()
                default_dates = st.session_state.date_range if st.session_state.date_range and len(st.session_state.date_range) == 2 else [min_date, max_date]

                st.session_state.date_range = st.sidebar.date_input(
                    "Select Date Range",
                    default_dates
                )

                if len(st.session_state.date_range) == 2:
                    start_date, end_date = st.session_state.date_range
                    # Filter dataset
                    st.session_state.filtered_df = st.session_state.df[
                        (st.session_state.df['site_id'] == st.session_state.selected_site) &
                        (st.session_state.df['timestamp'] >= pd.to_datetime(start_date)) &
                        (st.session_state.df['timestamp'] <= pd.to_datetime(end_date))
                    ].copy() # Use .copy() to avoid SettingWithCopyWarning
                    filtered_df = st.session_state.filtered_df
                else:
                    st.warning("Please select a valid date range.")
                    filtered_df = pd.DataFrame()
            else:
                filtered_df = pd.DataFrame()

            # Role-Based Interface Customization
            if role == "admin":
                # Admin View: Full access
                if not filtered_df.empty:
                    st.markdown(f"### Site: **{st.session_state.selected_site}**")

                    # Metrics
                    col1, col2 = st.columns(2)
                    avg_uptime = filtered_df['uptime'].mean()
                    col1.metric("Avg Uptime (%)", f"{avg_uptime:.2f}" if not pd.isna(avg_uptime) else "N/A")

                    total_energy = filtered_df['energy_consumption'].sum()
                    col2.metric("⚡ Total Energy Consumption (kWh)", f"{total_energy:.1f}" if not pd.isna(total_energy) else "N/A")

                    col3, col4 = st.columns(2)
                    total_alarms = filtered_df['alarm_count'].sum()
                    col3.metric("🚨 Total Alarms", f"{total_alarms}" if not pd.isna(total_alarms) else "N/A")

                    avg_signal = filtered_df['signal_strength'].mean()
                    col4.metric(" Avg Signal Strength (dBm)", f"{avg_signal:.1f}" if not pd.isna(avg_signal) else "N/A")

                    # Alerts Section
                    st.subheader("🚨 Alerts")
                    uptime_threshold = 95.0
                    energy_consumption_threshold = 700.0
                    alarm_count_threshold = 5

                    low_uptime = filtered_df[filtered_df['uptime'] < uptime_threshold]
                    high_energy = filtered_df[filtered_df['energy_consumption'] > energy_consumption_threshold]
                    high_alarms = filtered_df[filtered_df['alarm_count'] > alarm_count_threshold]

                    if not low_uptime.empty:
                        st.warning(f" Low Uptime Detected: {len(low_uptime)} occurrences below {uptime_threshold}%")
                    if not high_energy.empty:
                        st.warning(f"High Energy Consumption Detected: {len(high_energy)} occurrences above {energy_consumption_threshold} kWh")
                    if not high_alarms.empty:
                        st.warning(f"High Alarm Count Detected: {len(high_alarms)} occurrences above {alarm_count_threshold}")

                    # Predictive Analytics Section
                    st.subheader("🔮 Predictive Analytics")

                    if len(filtered_df) > 1:
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
                        st.warning("Not enough data for predictive analytics.")

                    # Charts
                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(
                            px.line(filtered_df, x='timestamp', y='uptime', title='Uptime Over Time'),
                            use_container_width=True
                        )
                    with col2:
                        st.plotly_chart(
                            px.bar(filtered_df, x='timestamp', y='energy_consumption', title='⚡ Energy Consumption Over Time'),
                            use_container_width=True
                        )
                else:
                    st.info("No data to display for the selected site and date range.")

            elif role == "engineer":
                # Engineer View: Detailed metrics but limited to their site
                if not filtered_df.empty:
                    st.markdown(f"### Site: **{st.session_state.selected_site}**")

                    # Metrics
                    col1, col2 = st.columns(2)
                    avg_uptime = filtered_df['uptime'].mean()
                    col1.metric("🔌 Avg Uptime (%)", f"{avg_uptime:.2f}" if not pd.isna(avg_uptime) else "N/A")

                    total_energy = filtered_df['energy_consumption'].sum()
                    col2.metric("⚡ Total Energy Consumption (kWh)", f"{total_energy:.1f}" if not pd.isna(total_energy) else "N/A")

                    col3, col4 = st.columns(2)
                    total_alarms = filtered_df['alarm_count'].sum()
                    col3.metric("🚨 Total Alarms", f"{total_alarms}" if not pd.isna(total_alarms) else "N/A")

                    avg_signal = filtered_df['signal_strength'].mean()
                    col4.metric(" Avg Signal Strength (dBm)", f"{avg_signal:.1f}" if not pd.isna(avg_signal) else "N/A")

# Alerts Section
                    st.subheader("🚨 Alerts")
                    uptime_threshold = 95.0
                    energy_consumption_threshold = 700.0
                    alarm_count_threshold = 5

                    low_uptime = filtered_df[filtered_df['uptime'] < uptime_threshold]
                    high_energy = filtered_df[filtered_df['energy_consumption'] > energy_consumption_threshold]
                    high_alarms = filtered_df[filtered_df['alarm_count'] > alarm_count_threshold]

                    if not low_uptime.empty:
                        st.warning(f"Low Uptime Detected: {len(low_uptime)} occurrences below {uptime_threshold}%")
                    if not high_energy.empty:
                        st.warning(f"High Energy Consumption Detected: {len(high_energy)} occurrences above {energy_consumption_threshold} kWh")
                    if not high_alarms.empty:
                        st.warning(f"High Alarm Count Detected: {len(high_alarms)} occurrences above {alarm_count_threshold}")

                    # Charts
                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(
                            px.line(filtered_df, x='timestamp', y='uptime', title=' Uptime Over Time'),
                            use_container_width=True
                        )
                    with col2:
                        st.plotly_chart(
                            px.bar(filtered_df, x='timestamp', y='energy_consumption', title='⚡ Energy Consumption Over Time'),
                            use_container_width=True
                        )
                else:
                    st.info("No data to display for the selected site and date range.")

            elif role == "manager":
                # Manager View: Summary metrics only
                if not filtered_df.empty:
                    st.markdown(f"### Site: **{st.session_state.selected_site}**")

                    # Metrics
                    col1, col2 = st.columns(2)
                    avg_uptime = filtered_df['uptime'].mean()
                    col1.metric(" Avg Uptime (%)", f"{avg_uptime:.2f}" if not pd.isna(avg_uptime) else "N/A")

                    total_energy = filtered_df['energy_consumption'].sum()
                    col2.metric("⚡ Total Energy Consumption (kWh)", f"{total_energy:.1f}" if not pd.isna(total_energy) else "N/A")

                    col3, col4 = st.columns(2)
                    total_alarms = filtered_df['alarm_count'].sum()
                    col3.metric("🚨 Total Alarms", f"{total_alarms}" if not pd.isna(total_alarms) else "N/A")

                    avg_signal = filtered_df['signal_strength'].mean()
                    col4.metric("Avg Signal Strength (dBm)", f"{avg_signal:.1f}" if not pd.isna(avg_signal) else "N/A")

                    # Alerts Section
                    st.subheader("🚨 Alerts")
                    uptime_threshold = 95.0
                    energy_consumption_threshold = 700.0
                    alarm_count_threshold = 5

                    low_uptime = filtered_df[filtered_df['uptime'] < uptime_threshold]
                    high_energy = filtered_df[filtered_df['energy_consumption'] > energy_consumption_threshold]
                    high_alarms = filtered_df[filtered_df['alarm_count'] > alarm_count_threshold]

                    if not low_uptime.empty:
                        st.warning(f"Low Uptime Detected: {len(low_uptime)} occurrences below {uptime_threshold}%")
                    if not high_energy.empty:
                        st.warning(f" High Energy Consumption Detected: {len(high_energy)} occurrences above {energy_consumption_threshold} kWh")
                    if not high_alarms.empty:
                        st.warning(f"High Alarm Count Detected: {len(high_alarms)} occurrences above {alarm_count_threshold}")
                else:
                    st.info("No data to display for the selected site and date range.")
        else:
            st.info("Please upload a valid CSV file to proceed.")
else:
    st.info("Please log in to proceed.")