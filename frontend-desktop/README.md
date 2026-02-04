# Chemical Equipment Parameter Visualizer - Desktop Application

## Project Structure

```
frontend-desktop/
├── main.py                  # Entry point
├── venv/                    # Virtual environment
├── ui/                      # UI components
│   ├── __init__.py
│   └── main_window.py      # Main application window
├── services/                # API communication
│   ├── __init__.py
│   └── api_service.py      # Django backend API client
├── charts/                  # Matplotlib charts
│   ├── __init__.py
│   └── base_chart.py       # Base chart class
└── requirements.txt         # Python dependencies
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Django backend running on http://localhost:8000

### Installation

1. Create virtual environment (already done):
```bash
python -m venv venv
```

2. Activate virtual environment:
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies (already done):
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
# Make sure backend is running first
cd backend
python manage.py runserver

# In another terminal, run the desktop app
cd frontend-desktop
.\venv\Scripts\python.exe main.py
```

## Dependencies

- **PyQt5 (5.15.11)**: Desktop GUI framework
- **matplotlib (3.10.8)**: Data visualization and charts
- **pandas (3.0.0)**: Data analysis and CSV handling
- **requests (2.32.5)**: HTTP client for API calls
- **numpy (2.4.2)**: Numerical computing (matplotlib dependency)

## Features (To Be Implemented)

- [x] User authentication (login/register)
- [x] CSV file upload with preview
- [x] Interactive Matplotlib charts:
  - [x] Pie chart for equipment type distribution
  - [x] Bar chart for parameter comparisons
  - [x] Line chart for parameter trends
- [x] Summary cards with key metrics
- [ ] Data table with sorting and filtering
- [ ] Dataset history management
- [ ] PDF report generation
- [ ] Export functionality

## Development Status

✅ Project structure created
✅ Virtual environment set up
✅ Dependencies installed
✅ Base files created:
  - main.py (entry point)
  - main_window.py (main window with menus)
  - api_service.py (API client)
  - base_chart.py (chart base class)
  - login_dialog.py (authentication)
  - register_dialog.py (user registration)
  - upload_widget.py (CSV upload with preview)
  - pie_chart.py (equipment type distribution)
  - bar_chart.py (average parameters comparison)
  - parameter_chart.py (parameter trends with filters)
  - summary_widget.py (dataset summary cards)

🚧 Next steps:
  - Create data table widget (Step 4.5)
  - Implement dashboard tab with all widgets (Step 4.8)
  - Create history tab (Step 4.9)
  - Integrate all components

## Tech Stack

- **Frontend**: PyQt5
- **Charts**: Matplotlib
- **Data Processing**: Pandas
- **API Communication**: Requests
- **Backend**: Django REST API

## Notes

- The application connects to Django backend at http://localhost:8000
- Authentication uses token-based auth (Django REST Framework)
- All API endpoints are defined in `services/api_service.py`
- Chart styling follows a consistent theme using the base chart class
