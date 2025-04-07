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


## Set Up a Virtual Environment (optional but recommended)

1. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   
Activate the Virtual Environment:
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Dependencies
pip install -r requirements.txt

Run the Application
streamlit run app.py

Usage
Register: Create a new account by providing a username, password, and role (admin, engineer, or manager).

Login: Log in with your credentials to access the dashboard.

Upload Data: Upload a CSV file containing telecom site data.

Filter Data: Use the sidebar filters to select a specific site and date range.

View Metrics: Explore the metrics, alerts, and visualizations based on your role.

Role-Based Access
Admin: Full access to all features, including predictive analytics and detailed charts. Can view and analyze data for all sites.

Engineer: Access to detailed metrics and visualizations for a specific site. Ideal for engineers who need granular insights into site performance.

Manager: Access to summary metrics and alerts. Designed for managers who need high-level oversight of site operations.

Contributing
We welcome contributions from the community! To contribute:

Fork the repository.

Create a new branch for your feature or bug fix:
git checkout -b feature-name

Commit your changes:
git commit -m "Add feature or fix"

Push to your branch:
git push origin feature-name

Submit a pull request describing your changes.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Support
If you encounter any issues or have questions, feel free to open an issue in the repository or contact the maintainers.

Acknowledgments
Built using Streamlit, Plotly, and Pandas.
Inspired by the need for efficient telecom site monitoring and analysis.

