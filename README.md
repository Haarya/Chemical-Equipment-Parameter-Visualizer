# Chemical Equipment Parameter Visualizer

> A hybrid Web + Desktop application for analyzing and visualizing chemical equipment data with CSV upload, interactive charts, and PDF reporting.

---

## 📋 Project Overview

This application enables users to upload CSV files containing chemical equipment parameters, perform statistical analysis, and visualize the results through both a web interface and desktop application.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Backend** | Django + Django REST Framework | RESTful API server |
| **Frontend (Web)** | React.js + Chart.js | Web dashboard with charts |
| **Frontend (Desktop)** | PyQt5 + Matplotlib | Desktop application |
| **Data Processing** | Pandas | CSV parsing & analytics |
| **Database** | SQLite | Store last 5 datasets |
| **Security** | Token Authentication, Rate Limiting, Input Validation | OWASP best practices |

---

## ✨ Key Features

- 📁 **CSV Upload** - Upload chemical equipment data files
- 📊 **Data Visualization** - Interactive charts (web) and plots (desktop)
- 📈 **Analytics** - Automatic calculation of averages and distributions
- 📄 **PDF Reports** - Generate downloadable reports
- 🔐 **Authentication** - Secure user registration and login
- 💾 **History Management** - Automatically keeps last 5 uploaded datasets
- 🌐 **Dual Interface** - Access via web browser or desktop app

---

## 🔒 Security Features

✅ Rate limiting on all endpoints (IP + user-based)  
✅ Strict input validation and sanitization  
✅ Environment-based secrets management (.env)  
✅ CSRF and XSS protection  
✅ Secure file upload validation  
✅ Token-based authentication  

---

## 📁 Project Structure

```
FOSSEE/
├── backend/                    # Django REST API
│   ├── config/                 # Django project settings
│   ├── equipment/              # Main app (models, views, serializers)
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # Environment variables (not tracked)
│
├── frontend-web/               # React.js web application
│   ├── public/                 # Static files
│   ├── src/                    # React components
│   │   ├── components/         # Reusable components
│   │   ├── pages/              # Page components
│   │   ├── services/           # API service layer
│   │   └── context/            # React context providers
│   └── package.json            # Node dependencies
│
├── frontend-desktop/           # PyQt5 desktop application
│   ├── main.py                 # Application entry point
│   ├── ui/                     # UI components
│   ├── services/               # API service layer
│   ├── charts/                 # Matplotlib chart widgets
│   └── requirements.txt        # Python dependencies
│
├── sample_data/                # Sample CSV files for testing
│   └── sample_equipment_data.csv
│
├── .gitignore                  # Git ignore rules
├── implementation_plan.md      # Detailed development plan
├── prerequisites.md            # Installation requirements
└── README.md                   # This file
```

---

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:
- Python 3.9+
- Node.js 18+
- Git

📖 See [prerequisites.md](prerequisites.md) for detailed installation instructions.

---

## 📝 Setup Instructions

### 1. Backend Setup (Django)

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Backend will run at: `http://localhost:8000`

---

### 2. Web Frontend Setup (React)

```bash
# Navigate to frontend-web folder
cd frontend-web

# Install dependencies
npm install

# Start development server
npm start
```

Web app will run at: `http://localhost:3000`

---

### 3. Desktop Frontend Setup (PyQt5)

```bash
# Navigate to frontend-desktop folder
cd frontend-desktop

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

---

## 🌐 Deployment

- **Backend**: PythonAnywhere / Railway / Render
- **Web Frontend**: Vercel / Netlify
- **Desktop App**: Packaged with PyInstaller

---

## 📊 Sample Data

Sample CSV file format:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
P-101,Pump,150.5,15.2,65.0
R-201,Reactor,80.0,25.5,180.0
E-301,Heat Exchanger,200.0,10.0,120.0
```

See `sample_data/sample_equipment_data.csv` for full example.

---

## 🎯 Development Status

Project is currently under active development following the [implementation plan](implementation_plan.md).

- [x] Phase 1: Project Setup ✅
- [ ] Phase 2: Backend API Development (In Progress)
- [ ] Phase 3: React Web Frontend
- [ ] Phase 4: PyQt5 Desktop Frontend
- [ ] Phase 5: PDF Report Generation
- [ ] Phase 6: Testing & Finalization
- [ ] Phase 7: Deployment & Documentation

---

## 📄 License

MIT License

---

## 👤 Author

**AARYA**  
FOSSEE Internship Project - 2026

---

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

*Last Updated: February 2026*
