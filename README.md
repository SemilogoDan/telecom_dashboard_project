# Telecom Site Monitoring Dashboard

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

The **Telecom Site Monitoring Dashboard** is a Streamlit-based web application designed to monitor and analyze telecom site performance. It provides role-based access (Admin, Engineer, Manager) with features like real-time metrics, alerts, predictive analytics, and interactive visualizations.

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

- **User Authentication**: Secure registration and login system with role-based access.
- **File Upload**: Upload CSV files containing telecom site data for analysis.
- **Interactive Filters**: Filter data by site ID and date range.
- **Real-Time Metrics**: View key performance indicators such as uptime, energy consumption, alarm count, and signal strength.
- **Alerts**: Receive warnings for low uptime, high energy consumption, or excessive alarms.
- **Predictive Analytics**: Predict future uptime and energy consumption trends using linear regression.
- **Visualizations**: Interactive charts (e.g., uptime trends, energy consumption over time) powered by Plotly.
- **Role-Based Customization**:
  - **Admin**: Full access to all features, including predictive analytics.
  - **Engineer**: Detailed metrics and visualizations for specific sites.
  - **Manager**: Summary metrics and alerts for high-level monitoring.

---

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.8 or higher
- Required Python libraries (see `requirements.txt`)
- A CSV file with the required columns: `site_id`, `timestamp`, `uptime`, `energy_consumption`, `alarm_count`, `signal_strength`

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/telecom-site-monitoring-dashboard.git
   cd telecom-site-monitoring-dashboard