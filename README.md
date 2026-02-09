# Chemical Equipment Parameter Visualizer

A hybrid **Web + Desktop** application for uploading, analyzing, and visualizing chemical equipment data. Built with a shared Django REST backend consumed by both a React web frontend and a PyQt5 desktop frontend.

**Live Web App:** [https://reactometrix.vercel.app](https://reactometrix.vercel.app)

---

## Tech Stack

| Layer              | Technology                     | Purpose                         |
| ------------------ | ------------------------------ | ------------------------------- |
| Frontend (Web)     | React.js + Chart.js            | Interactive web dashboard       |
| Frontend (Desktop) | PyQt5 + Matplotlib             | Native desktop visualization    |
| Backend            | Django + Django REST Framework  | REST API, auth, data processing |
| Data Handling      | Pandas                         | CSV parsing and analytics       |
| Database           | SQLite                         | Stores last 5 uploaded datasets |
| Version Control    | Git + GitHub                   | Source code management          |

---

## Key Features

1. **CSV Upload** — Upload equipment data via web or desktop; the backend validates columns, data types, and value ranges.
2. **Data Summary API** — Returns total count, averages (flowrate, pressure, temperature), and equipment type distribution.
3. **Visualization** — Bar charts, pie charts, and line charts rendered with Chart.js (web) and Matplotlib (desktop).
4. **History Management** — Keeps the last 5 uploaded datasets per user with full CRUD support.
5. **PDF Report Generation** — Download a formatted PDF report for any dataset.
6. **Authentication** — Token-based registration, login, and logout via Django REST Framework.

---

## Prerequisites

Install these before proceeding:

| Tool       | Minimum Version | Download                                      |
| ---------- | --------------- | --------------------------------------------- |
| Python     | 3.9+            | [python.org/downloads](https://www.python.org/downloads/) |
| Node.js    | 18+             | [nodejs.org](https://nodejs.org/)              |
| Git        | any recent      | [git-scm.com](https://git-scm.com/)           |

Verify installations:

```bash
python --version
node --version
npm --version
git --version
```

---

## Setup Instructions

### Step 0 — Clone the Repository

```bash
git clone https://github.com/Haarya/Chemical-Equipment-Parameter-Visualizer.git
cd Chemical-Equipment-Parameter-Visualizer
```

---

### Step 1 — Backend (Django REST API)

```bash
# Move into the backend folder
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows (PowerShell):
.\venv\Scripts\activate
# Windows (CMD):
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create the database tables
python manage.py migrate

# (Optional) Create an admin superuser
python manage.py createsuperuser

# Start the backend server
python manage.py runserver
```

The API is now running at **http://127.0.0.1:8000**.

#### Backend Environment Variables (optional for local dev)

Copy the example file and edit if needed:

```bash
copy .env.example .env
```

Key variables inside `.env`:

| Variable      | Default                          | Description                          |
| ------------- | -------------------------------- | ------------------------------------ |
| `SECRET_KEY`  | auto-generated insecure default  | Django secret key                    |
| `DEBUG`       | `True`                           | Set `False` in production            |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1`          | Comma-separated allowed hostnames    |

> For local development the defaults work out of the box — no `.env` file is strictly required.

---

### Step 2 — Web Frontend (React)

> **Prerequisite:** The backend server must be running (Step 1).

```bash
# Open a new terminal, then:
cd frontend-web

# Install Node.js dependencies
npm install

# Start the React development server
npm start
```

The web app opens at **http://localhost:3000** and connects to the backend at `http://127.0.0.1:8000` by default.

#### Changing the Backend URL

Edit `frontend-web/.env` (create it if missing):

```
REACT_APP_API_URL=http://127.0.0.1:8000
```

Restart the React dev server after changing this value.

---

### Step 3 — Desktop Frontend (PyQt5)

> **Prerequisite:** The backend server must be running (Step 1).

```bash
# Open a new terminal, then:
cd frontend-desktop

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows (PowerShell):
.\venv\Scripts\activate
# Windows (CMD):
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Launch the desktop application
python main.py
```

The desktop app connects to `http://127.0.0.1:8000` by default. Make sure the backend is running before launching.

> **Note:** After registering a new account in the desktop app, close and restart the application (`python main.py`) to log in and begin using it.

---

## Sample Data

A sample CSV file is included at `sample_data/sample_equipment_data.csv`.

Expected CSV format:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Compressor-1,Compressor,95,8.4,95
Valve-1,Valve,60,4.1,105
HeatExchanger-1,HeatExchanger,150,6.2,130
```

Upload this file through the web or desktop interface to test the full workflow.

---

## API Endpoints

All `/api/` endpoints use **Token Authentication** (`Authorization: Token <key>`).

| Method | Endpoint                          | Description                      |
| ------ | --------------------------------- | -------------------------------- |
| POST   | `/api/auth/register/`             | Register a new user              |
| POST   | `/api/auth/login/`                | Login and receive auth token     |
| POST   | `/api/auth/logout/`               | Logout and invalidate token      |
| GET    | `/api/auth/user/`                 | Get current user info            |
| POST   | `/api/upload/`                    | Upload a CSV file                |
| GET    | `/api/datasets/`                  | List datasets (last 5 per user)  |
| GET    | `/api/datasets/<id>/`             | Get full dataset with records    |
| GET    | `/api/datasets/<id>/summary/`     | Get summary statistics           |
| GET    | `/api/datasets/<id>/report/pdf/`  | Download PDF report              |
| DELETE | `/api/datasets/<id>/delete/`      | Delete a dataset                 |

---

## Deployment

| Component  | Platform | URL |
| ---------- | -------- | --- |
| Web Frontend | Vercel | [https://reactometrix.vercel.app](https://reactometrix.vercel.app) |
| Backend API  | Render | [https://chemical-equipment-parameter-visualizer-sias.onrender.com](https://chemical-equipment-parameter-visualizer-sias.onrender.com) |

---

