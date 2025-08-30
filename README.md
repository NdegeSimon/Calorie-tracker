# ECOTRACKER

## Overview

EcoTracker is an open-source platform designed to empower individuals, households, and businesses to monitor, analyze, and reduce their environmental impact. By tracking key metrics such as carbon footprint, energy consumption, water usage, and waste production, EcoTracker provides actionable insights through intuitive data visualizations and goal-setting tools. Whether you’re an environmentally conscious individual aiming to live more sustainably or an organization striving to meet ESG (Environmental, Social, and Governance) targets, EcoTracker offers flexible solutions via a command-line interface (CLI) and a web application.

The project is built with a modular architecture, leveraging Python and SQLAlchemy for the CLI and backend, and React with Node.js for the web interface. It supports local data storage with SQLite and optional cloud-based database integration for scalability. EcoTracker is designed to be extensible, making it an excellent starting point for developers interested in sustainability-focused applications.

## Features

- **Automatic Emission Calculations:** Compute carbon emissions using built-in emission factors (e.g., kg CO2 per kilometer driven) based on industry-standard databases.
- **Data Visualization:** Generate interactive charts (bar, line, or pie) to visualize your environmental impact over time, available in the web app and as CLI-generated plots using Matplotlib.
- **Sustainability Goals:** Set and track personalized eco-friendly goals, such as reducing carbon emissions by 15% or cutting energy usage by 20 kWh per month.
- **Multi-Platform Support:** Access EcoTracker via a web interface (React-based), iOS/Android apps (in development), or a powerful CLI for advanced users and automation.
- **User Management:** Manage multiple users with distinct profiles, ideal for households or teams, with support for role-based access in the web app.

## Installation

### Prerequisites

To set up EcoTracker, ensure you have the following installed:

- **Python:** Version 3.8 or higher (for CLI and backend)
- **pip:** Python package manager
- **npm:** Node package manager
- **Virtualenv (optional, recommended):** For isolated Python environments
- **Web Browser:** Chrome, Firefox, or Safari (latest versions for web app)
- **Git:** For cloning the repository
- **SQLite:** Included with Python, but ensure compatibility for database operations
- **Optional:** PostgreSQL or MySQL for advanced database configurations

### Setup Instructions

Follow these steps to get EcoTracker up and running locally:

#### 1. Clone the Repository

```bash
git clone https://github.com/eco-tracker/ecotracker.git
cd ecotracker
```
This downloads the EcoTracker source code to your local machine. Ensure you have Git installed (`git --version` to verify).

#### 2. Set Up the CLI Environment

Create and activate a virtual environment to isolate dependencies:

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:
```
sqlalchemy==2.0.0
click==8.1.3
python-dotenv==1.0.0
```

DATABASE_URL=sqlite:///ecotracker.db
API_KEY=your_api_key_here
WEB_PORT=3000
API_PORT=5000
```

For PostgreSQL/MySQL, update `DATABASE_URL` (e.g., `postgresql://user:password@localhost:5432/ecotracker`).

#### 5. Initialize the Database

Run the database setup script to create tables for users and activities:

```bash
python scripts/init_db.py
```

#### 6. Launch the Application

**Start the Backend (CLI and API):**
```bash
cd backend
python main.py
```
This starts the Python backend server, typically on http://localhost:5000.


**Run CLI Commands:**
```bash
python ecotrack.py --help
```
This displays available CLI commands for direct interaction.

#### 7. Access EcoTracker

- **Web Interface:** Open [http://localhost:3000](http://localhost:3000) in your browser.
- **API:** Test endpoints at [http://localhost:5000/api](http://localhost:5000/api) (e.g., `/api/users`).
- **CLI:** Use commands like `python ecotrack.py add_user --name "John Doe"`.

## Usage

### CLI Usage

The CLI provides a powerful way to interact with EcoTracker. Below are common commands:

- **Add a User:**
  ```bash
  python ecotrack.py add_user --name "John Doe" 
  ```
  Creates a new user profile with a unique ID.

- **Log an Activity:**
  ```bash
  python ecotrack.py add_activity --user_id 1 --type "driving" --quantity 50
  ```
  Logs an activity (e.g., 50 km driven) and calculates emissions automatically.

- **List Users or Activities:**
  ```bash
  python ecotrack.py list_users
  python ecotrack.py list_activities --user_id 1
  ```
  Displays all users or a user’s activities.

- **Visualize Data:**
  ```bash
  python ecotrack.py show_chart --user_id 1
  ```
  Generates a Matplotlib bar chart of emissions by activity type.

- **Set a Goal:**
  ```bash
  python ecotrack.py set_goal --user_id 1 --type "carbon" --target 1000
  ```
  Sets a goal (e.g., limit carbon emissions to 1000 kg/year).



#### Example Workflow

- **Day 1:** Add a user (`add_user`), log 20 km of driving (`add_activity`), and view emissions (`show_chart`).
- **Day 2:** Set a goal to reduce emissions by 10% (`set_goal`) and check progress on the web dashboard.
- **Day 3:** Export your data (`export_data`) for a sustainability report.

## Project Structure

```
ecotracker/                 # Python backend (API and CLI logic)
├── main.py              # Main backend script
├── models.py            # SQLAlchemy models (User, Activity)
├── operations.py
|── requirements.txt         # Python dependencies
├── .env                     # Environment variables            # Template for .env
└── README.md                # This file
```

## License

EcoTracker is licensed under the MIT License. See the LICENSE file for full details.

## Contact

- **Email:** support@ecotracker.org
- **GitHub:** [EcoTracker Issues](https://github.com/eco-tracker/ecotracker/issues)
- **Community Forum:** Join discussions at [community.ecotracker.org](https://community.ecotracker.org)
- **Twitter:** Follow us at [@EcoTrackerApp](https://twitter.com/EcoTrackerApp)

