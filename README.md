# Telecom Site Monitoring Dashboard

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

The **Telecom Site Monitoring Dashboard** is an intuitive and efficient web application developed using **Streamlit**, designed to monitor, manage, and analyze the performance of telecom sites. The platform features role-based access control, providing tailored experiences for **Admins**, **Engineers**, and **Managers**. Key functionalities include real-time performance metrics, predictive analytics, customizable alerts, and interactive visualizations to assist with decision-making and operational optimization.

---

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Role-Based Access](#role-based-access)
6. [Contributing](#contributing)
7. [License](#license)

---

## Features

- **User Authentication**: Secure and straightforward user registration and login system with access tailored to specific roles.
- **Data Upload**: Seamlessly upload CSV files containing telecom site data for analysis.
- **Custom Filters**: Filter data based on site ID and date range to easily access relevant information.
- **Real-Time Performance Metrics**: View and track key performance indicators (KPIs) such as uptime, energy consumption, alarm counts, and signal strength.
- **Alerts & Notifications**: Receive timely alerts for critical issues such as low uptime, excessive energy consumption, or high alarm frequency.
- **Predictive Analytics**: Utilize linear regression models to predict future performance trends, such as uptime and energy consumption, for proactive management.
- **Dynamic Visualizations**: Leverage interactive charts (e.g., uptime trends, energy consumption over time) powered by **Plotly** for actionable insights.
- **Role-Based Customization**:
  - **Admin**: Full access to all features, including advanced analytics and system management.
  - **Engineer**: Access to detailed site-specific metrics and visualizations.
  - **Manager**: High-level views and alerts for monitoring site performance at a strategic level.

---

## Prerequisites

To run the **Telecom Site Monitoring Dashboard**, you will need:

- **Python 3.8+**
- The required Python libraries listed in `requirements.txt`
- A CSV file containing the following columns:
  - `site_id`: Unique identifier for each telecom site.
  - `timestamp`: The date and time of the data entry.
  - `uptime`: The percentage of uptime for the site.
  - `energy_consumption`: The energy usage in kilowatt-hours (kWh).
  - `alarm_count`: The number of alarms triggered for the site.
  - `signal_strength`: The signal strength in dBm.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/telecom-site-monitoring-dashboard.git
   cd telecom-site-monitoring-dashboard
