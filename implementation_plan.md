# Chemical Equipment Parameter Visualizer - Implementation Plan

## Project Overview
A hybrid application (Web + Desktop) for uploading CSV files containing chemical equipment data, performing analytics, and visualizing results.

---

## Tech Stack (As Per Requirements)
| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend (Web) | React.js + Chart.js | Show table + charts |
| Frontend (Desktop) | PyQt5 + Matplotlib | Same visualization in desktop |
| Backend | Python Django + Django REST Framework | Common backend API |
| Data Handling | Pandas | Reading CSV & analytics |
| Database | SQLite | Store last 5 uploaded datasets |
| Version Control | Git & GitHub | Collaboration & submission |

---

## Phase 1: Project Setup & Backend Foundation

### Step 1.1: Initialize Project Structure
**Objective:** Create the base folder structure for all components.

**Prompt:**
```
Create the complete project folder structure for the Chemical Equipment Parameter Visualizer:
- backend/ (Django project)
- frontend-web/ (React app)
- frontend-desktop/ (PyQt5 app)
- sample_data/ (CSV files)
- Initialize Git repository
- Create .gitignore file for Python, Node.js, and common IDE files
```

**Expected Output:**
```
FOSSEE/
├── backend/
├── frontend-web/
├── frontend-desktop/
├── sample_data/
├── .gitignore
└── README.md
```

---

### Step 1.2: Create Sample CSV Data
**Objective:** Generate the sample_equipment_data.csv file for testing.

**Prompt:**
```
Create sample_equipment_data.csv in the sample_data folder with the following specifications:
- Columns: Equipment Name, Type, Flowrate, Pressure, Temperature
- Include 25-30 rows of realistic chemical equipment data
- Equipment Types: Pump, Reactor, Heat Exchanger, Compressor, Distillation Column, Storage Tank
- Flowrate: realistic values in m³/h (range 10-500)
- Pressure: realistic values in bar (range 1-50)
- Temperature: realistic values in °C (range 20-350)
- Use proper naming conventions like "P-101", "R-201", "E-301" for equipment
```

---

### Step 1.3: Set Up Django Backend Project
**Objective:** Initialize Django project with required dependencies.

**Prompt:**
```
Set up the Django backend:
1. Create virtual environment in backend folder
2. Install dependencies: Django, djangorestframework, django-cors-headers, pandas, reportlab
3. Create Django project named 'config'
4. Create Django app named 'equipment'
5. Configure settings.py with:
   - CORS headers for React frontend (localhost:3000)
   - REST Framework settings with Token Authentication
   - SQLite database configuration
   - Static and media file settings
6. Create requirements.txt with all dependencies
```

---

### Step 1.4: Create Database Models
**Objective:** Define Django models for equipment data and dataset history.

**Prompt:**
```
Create Django models in the equipment app:

1. Dataset Model:
   - id (auto primary key)
   - name (CharField - original filename)
   - uploaded_at (DateTimeField - auto now)
   - total_records (IntegerField)
   - avg_flowrate (FloatField)
   - avg_pressure (FloatField)
   - avg_temperature (FloatField)
   - type_distribution (JSONField - stores count per equipment type)

2. Equipment Model:
   - id (auto primary key)
   - dataset (ForeignKey to Dataset)
   - equipment_name (CharField)
   - equipment_type (CharField)
   - flowrate (FloatField)
   - pressure (FloatField)
   - temperature (FloatField)

3. Add model method to Dataset to enforce keeping only last 5 uploads
4. Run migrations
```

---

## Phase 2: Backend API Development

### Step 2.1: Create Serializers
**Objective:** Build DRF serializers for API responses.

**Prompt:**
```
Create serializers.py in the equipment app with:

1. EquipmentSerializer - serialize all equipment fields
2. DatasetListSerializer - for listing datasets (id, name, uploaded_at, total_records)
3. DatasetDetailSerializer - full dataset info with nested equipment list
4. DatasetSummarySerializer - summary statistics only
5. FileUploadSerializer - for validating CSV file uploads
```

---

### Step 2.2: Create API Views
**Objective:** Implement all required API endpoints.

**Prompt:**
```
Create views.py with the following API views:

1. CSVUploadView (POST /api/upload/)
   - Accept CSV file upload
   - Parse with Pandas
   - Validate columns: Equipment Name, Type, Flowrate, Pressure, Temperature
   - Calculate summary statistics
   - Save Dataset and Equipment records
   - Delete oldest dataset if more than 5 exist
   - Return dataset summary

2. DatasetListView (GET /api/datasets/)
   - Return list of all datasets (last 5)
   - Include basic info: id, name, uploaded_at, total_records

3. DatasetDetailView (GET /api/datasets/<id>/)
   - Return full dataset with all equipment records

4. DatasetSummaryView (GET /api/datasets/<id>/summary/)
   - Return summary: total_count, averages, type_distribution

5. GeneratePDFReportView (GET /api/datasets/<id>/report/pdf/)
   - Generate PDF report using ReportLab
   - Include summary stats, type distribution chart, data table
   - Return PDF file response
```

---

### Step 2.3: Configure URLs
**Objective:** Set up URL routing for the API.

**Prompt:**
```
Configure URL routing:

1. Create equipment/urls.py with all API routes:
   - POST /api/upload/
   - GET /api/datasets/
   - GET /api/datasets/<id>/
   - GET /api/datasets/<id>/summary/
   - GET /api/datasets/<id>/report/pdf/

2. Include equipment URLs in config/urls.py
3. Add authentication URLs for login/logout/register
```

---

### Step 2.4: Implement Authentication
**Objective:** Add basic token authentication.

**Prompt:**
```
Implement authentication:

1. Create User registration endpoint (POST /api/auth/register/)
   - Accept username, email, password
   - Create user and return auth token

2. Create Login endpoint (POST /api/auth/login/)
   - Accept username, password
   - Return auth token

3. Create Logout endpoint (POST /api/auth/logout/)
   - Invalidate token

4. Protect all dataset endpoints with IsAuthenticated permission
5. Keep upload endpoint accessible (or protected based on requirement)
```

---

### Step 2.5: Test Backend API
**Objective:** Verify all endpoints work correctly.

**Prompt:**
```
Test the Django backend:

1. Run Django development server
2. Use the sample_equipment_data.csv to test upload endpoint
3. Verify all CRUD operations work
4. Test authentication flow
5. Test PDF generation
6. Verify only last 5 datasets are kept
7. Check CORS is working for frontend requests
```

---

## Phase 3: React Web Frontend Development

### Step 3.1: Initialize React Project
**Objective:** Set up React application with dependencies.

**Prompt:**
```
Set up React frontend:

1. Create React app in frontend-web folder using create-react-app
2. Install dependencies:
   - axios (API calls)
   - chart.js and react-chartjs-2 (charts)
   - react-router-dom (routing)
   - bootstrap or tailwind (styling - optional)
3. Set up project structure:
   - src/components/
   - src/pages/
   - src/services/
   - src/context/
4. Configure API base URL for Django backend
```

---

### Step 3.2: Create Authentication Components
**Objective:** Build login and registration UI.

**Prompt:**
```
Create authentication components:

1. LoginPage.jsx
   - Username and password form
   - Call login API endpoint
   - Store token in localStorage
   - Redirect to dashboard on success

2. RegisterPage.jsx
   - Username, email, password form
   - Call register API endpoint
   - Auto-login after registration

3. AuthContext.jsx
   - Manage authentication state
   - Provide login, logout, isAuthenticated methods
   - Persist auth state across page refreshes

4. ProtectedRoute.jsx
   - Wrapper for routes requiring authentication
   - Redirect to login if not authenticated
```

---

### Step 3.3: Create File Upload Component
**Objective:** Build CSV upload functionality.

**Prompt:**
```
Create FileUpload component:

1. FileUpload.jsx
   - Drag and drop zone for CSV files
   - File input with accept=".csv"
   - Preview selected file name
   - Upload button that calls API
   - Loading state during upload
   - Success/error message display
   - After successful upload, redirect to dataset view
```

---

### Step 3.4: Create Data Table Component
**Objective:** Display equipment data in a table.

**Prompt:**
```
Create DataTable component:

1. DataTable.jsx
   - Receive equipment data as prop
   - Display all columns: Equipment Name, Type, Flowrate, Pressure, Temperature
   - Add sorting functionality for each column
   - Add pagination (10 rows per page)
   - Optional: Add search/filter functionality
   - Style with CSS for readability
```

---

### Step 3.5: Create Chart Components
**Objective:** Build data visualization with Chart.js.

**Prompt:**
```
Create chart components using Chart.js:

1. TypeDistributionChart.jsx
   - Pie or Doughnut chart showing equipment type distribution
   - Display count and percentage for each type
   - Use distinct colors for each type

2. ParameterBarChart.jsx
   - Bar chart comparing average Flowrate, Pressure, Temperature
   - Include labels and legend

3. ParameterComparisonChart.jsx (optional)
   - Line or bar chart showing individual equipment parameters
   - Allow filtering by equipment type

4. ChartPanel.jsx
   - Container component that renders all charts
   - Responsive layout for different screen sizes
```

---

### Step 3.6: Create Summary Card Component
**Objective:** Display dataset summary statistics.

**Prompt:**
```
Create SummaryCard component:

1. SummaryCard.jsx
   - Display total equipment count
   - Display average Flowrate, Pressure, Temperature
   - Use card-style layout with icons
   - Show upload date and dataset name

2. Style cards with distinct colors for each metric
3. Make responsive for mobile view
```

---

### Step 3.7: Create History Component
**Objective:** Show list of uploaded datasets.

**Prompt:**
```
Create dataset history component:

1. HistoryList.jsx
   - Fetch and display last 5 uploaded datasets
   - Show: dataset name, upload date, record count
   - Click on dataset to view details
   - Add delete button for each dataset (optional)

2. HistorySidebar.jsx
   - Sidebar version of history list
   - Collapsible for mobile view
```

---

### Step 3.8: Create Dashboard Page
**Objective:** Assemble main dashboard with all components.

**Prompt:**
```
Create Dashboard page:

1. Dashboard.jsx
   - Layout with header, sidebar, main content
   - Integrate: SummaryCard, ChartPanel, DataTable
   - Fetch dataset data on component mount
   - Handle loading and error states
   - Add button to download PDF report
   - Add button to upload new dataset

2. Set up React Router with routes:
   - / -> Login
   - /register -> Register
   - /dashboard -> Dashboard (protected)
   - /upload -> Upload page (protected)
   - /dataset/:id -> Dataset detail view (protected)
```

---

### Step 3.9: Test React Frontend
**Objective:** Verify all functionality works with backend.

**Prompt:**
```
Test React frontend:

1. Start Django backend server
2. Start React development server
3. Test authentication flow (register, login, logout)
4. Test CSV upload with sample file
5. Verify data table displays correctly
6. Verify all charts render with correct data
7. Test dataset history navigation
8. Test PDF download functionality
9. Test responsive design on different screen sizes
```

---

## Phase 4: PyQt5 Desktop Frontend Development

### Step 4.1: Set Up PyQt5 Project
**Objective:** Initialize desktop application structure.

**Prompt:**
```
Set up PyQt5 desktop app:

1. Create virtual environment in frontend-desktop folder
2. Install dependencies: PyQt5, matplotlib, pandas, requests
3. Create project structure:
   - main.py (entry point)
   - ui/ (UI components)
   - services/ (API calls)
   - charts/ (Matplotlib charts)
4. Create requirements.txt
```

---

### Step 4.2: Create Main Window
**Objective:** Build the main application window.

**Prompt:**
```
Create PyQt5 main window:

1. main_window.py
   - QMainWindow with menu bar
   - Tab widget with tabs: Dashboard, Upload, History
   - Status bar for messages
   - Window title and icon
   - Minimum size: 1200x800

2. Create menu items:
   - File -> Upload CSV, Download Report, Exit
   - Account -> Login, Logout
   - Help -> About
```

---

### Step 4.3: Create Login Dialog
**Objective:** Build authentication UI for desktop.

**Prompt:**
```
Create login dialog:

1. login_dialog.py
   - QDialog with username and password fields
   - Login and Register buttons
   - Call backend API for authentication
   - Store token for subsequent requests
   - Show error message on failed login

2. register_dialog.py
   - QDialog for new user registration
   - Username, email, password fields
   - Call register API endpoint
```

---

### Step 4.4: Create Upload Widget
**Objective:** Build CSV upload functionality.

**Prompt:**
```
Create upload widget:

1. upload_widget.py
   - QWidget with file selection button
   - Use QFileDialog to select CSV file
   - Display selected file path
   - Upload button to send to API
   - Progress bar during upload
   - Success/error message display
   - Option to preview CSV data before upload using QTableWidget
```

---

### Step 4.5: Create Data Table Widget
**Objective:** Display equipment data in PyQt5 table.

**Prompt:**
```
Create data table widget:

1. data_table_widget.py
   - QTableWidget to display equipment data
   - Columns: Equipment Name, Type, Flowrate, Pressure, Temperature
   - Enable sorting by column headers
   - Add search/filter input field
   - Style with alternating row colors
   - Right-click context menu for actions
```

---

### Step 4.6: Create Matplotlib Charts
**Objective:** Build chart widgets using Matplotlib.

**Prompt:**
```
Create Matplotlib chart widgets:

1. charts/base_chart.py
   - Base class with FigureCanvasQTAgg integration
   - Common styling and configuration

2. charts/pie_chart.py
   - Pie chart for equipment type distribution
   - Legend and percentage labels

3. charts/bar_chart.py
   - Bar chart for average parameters comparison
   - Flowrate, Pressure, Temperature bars

4. charts/parameter_chart.py
   - Line or scatter chart for parameter comparison
   - Filter by equipment type

5. All charts should update when data changes
```

---

### Step 4.7: Create Summary Widget
**Objective:** Display summary statistics.

**Prompt:**
```
Create summary widget:

1. summary_widget.py
   - QFrame/QGroupBox displaying:
     - Total equipment count
     - Average Flowrate
     - Average Pressure
     - Average Temperature
   - Use QLabel with styled fonts
   - Update dynamically when dataset changes
```

---

### Step 4.8: Create Dashboard Tab
**Objective:** Assemble main dashboard view.

**Prompt:**
```
Create dashboard tab:

1. dashboard_tab.py
   - QWidget with layout combining:
     - Summary widget (top)
     - Charts section (middle)
     - Data table (bottom)
   - Splitter for resizable sections
   - Dropdown to select dataset from history
   - Button to download PDF report
   - Refresh button to reload data
```

---

### Step 4.9: Create History Tab
**Objective:** Show uploaded dataset history.

**Prompt:**
```
Create history tab:

1. history_tab.py
   - QListWidget showing last 5 datasets
   - Display: name, upload date, record count
   - Double-click to load dataset in dashboard
   - Delete button for each entry (optional)
   - Refresh button to reload history
```

---

### Step 4.10: Create API Service
**Objective:** Centralize API calls.

**Prompt:**
```
Create API service module:

1. services/api_service.py
   - Class to handle all API requests
   - Methods: login, register, logout
   - Methods: upload_csv, get_datasets, get_dataset_detail, get_summary
   - Method: download_pdf_report
   - Handle authentication token in headers
   - Error handling and response parsing
   - Base URL configuration for backend
```

---

### Step 4.11: Test Desktop Application
**Objective:** Verify all functionality.

**Prompt:**
```
Test PyQt5 desktop app:

1. Start Django backend server
2. Run main.py to launch desktop app
3. Test login/register flow
4. Test CSV upload with sample file
5. Verify data table displays correctly
6. Verify all Matplotlib charts render
7. Test dataset history navigation
8. Test PDF download functionality
9. Test window resizing and layouts
```

---

## Phase 5: PDF Report Generation

### Step 5.1: Implement PDF Generation
**Objective:** Create PDF report using ReportLab.

**Prompt:**
```
Implement PDF report generation in Django backend:

1. Create reports/pdf_generator.py
   - Use ReportLab library
   - Generate PDF with:
     - Header with title and date
     - Summary statistics section
     - Equipment type distribution table
     - Data table with all equipment
     - Optional: Embed a chart image

2. Update GeneratePDFReportView to use generator
3. Set proper content-type and filename headers
4. Test PDF download from both frontends
```

---

## Phase 6: Testing & Finalization

### Step 6.1: Integration Testing
**Objective:** Test complete application flow.

**Prompt:**
```
Perform integration testing:

1. Test complete flow from both frontends:
   - Register new user
   - Login
   - Upload sample CSV
   - View dashboard with charts
   - Upload 5 more files, verify old ones are deleted
   - Download PDF report
   - Logout

2. Test error scenarios:
   - Invalid CSV format
   - Network errors
   - Invalid credentials
   - Empty file upload

3. Document any bugs found
```

---

### Step 6.2: Code Cleanup
**Objective:** Clean and optimize code.

**Prompt:**
```
Clean up the codebase:

1. Remove console.log statements and print statements
2. Add proper error handling throughout
3. Add loading states for all async operations
4. Optimize database queries
5. Add input validation
6. Format code consistently (use formatters)
7. Remove unused imports and variables
```

---

## Phase 7: Deployment & Documentation

### Step 7.1: Deploy Django Backend
**Objective:** Host backend on cloud platform.

**Prompt:**
```
Deploy Django backend:

1. Prepare for deployment:
   - Set DEBUG=False
   - Configure ALLOWED_HOSTS
   - Set up static file serving
   - Configure CORS for production frontend URL

2. Deploy to PythonAnywhere (free tier):
   - Create account
   - Upload code
   - Set up virtual environment
   - Configure WSGI
   - Run migrations
   - Test API endpoints

Alternative: Deploy to Railway or Render
```

---

### Step 7.2: Deploy React Frontend
**Objective:** Host web frontend on cloud platform.

**Prompt:**
```
Deploy React frontend:

1. Update API base URL to production backend
2. Build production bundle: npm run build
3. Deploy to Vercel:
   - Connect GitHub repository
   - Configure build settings
   - Deploy and get production URL

Alternative: Deploy to Netlify
4. Test all functionality on deployed version
```

---

### Step 7.3: Package Desktop Application
**Objective:** Create executable for desktop app.

**Prompt:**
```
Package PyQt5 desktop app:

1. Install PyInstaller: pip install pyinstaller
2. Update API base URL to production backend
3. Create executable:
   pyinstaller --onefile --windowed --name "ChemEquipVisualizer" main.py
4. Test executable on clean Windows machine
5. Create installer using NSIS (optional)
```

---

### Step 7.4: Create README Documentation
**Objective:** Write comprehensive setup instructions.

**Prompt:**
```
Create README.md with:

1. Project title and description
2. Features list
3. Tech stack table
4. Screenshots of both frontends

5. Setup Instructions:
   a. Backend setup (Python, Django, migrations)
   b. Web frontend setup (Node.js, npm install, npm start)
   c. Desktop frontend setup (Python, PyQt5, run main.py)

6. API documentation (endpoints list)
7. Sample data description
8. Deployment links (web version)
9. Demo video link
10. Author information
11. License
```

---

### Step 7.5: Record Demo Video
**Objective:** Create demonstration video.

**Prompt:**
```
Record 2-3 minute demo video showing:

1. Introduction (10 seconds)
   - Project name and purpose

2. Web Application Demo (60 seconds)
   - Login
   - Upload CSV file
   - Show data table
   - Show charts
   - Download PDF report
   - Show dataset history

3. Desktop Application Demo (60 seconds)
   - Same features as web
   - Show Matplotlib charts
   - Show PDF download

4. Conclusion (10 seconds)
   - Tech stack summary
   - GitHub link

Use OBS or screen recording software
Upload to YouTube or Google Drive
```

---

### Step 7.6: Submit Project
**Objective:** Complete final submission.

**Prompt:**
```
Final submission checklist:

1. Push all code to GitHub
2. Verify README is complete
3. Verify .gitignore excludes:
   - node_modules/
   - venv/
   - __pycache__/
   - .env files
   - db.sqlite3 (or include for demo)

4. Add demo video to README
5. Add deployment link to README
6. Fill Google Form with:
   - GitHub repository link
   - Demo video link
   - Deployed web app link
   - Your contact information
```

---

## Summary Timeline

| Phase | Description | Estimated Time |
|-------|-------------|----------------|
| Phase 1 | Project Setup & Backend Foundation | 3-4 hours |
| Phase 2 | Backend API Development | 4-5 hours |
| Phase 3 | React Web Frontend | 5-6 hours |
| Phase 4 | PyQt5 Desktop Frontend | 5-6 hours |
| Phase 5 | PDF Report Generation | 1-2 hours |
| Phase 6 | Testing & Finalization | 2-3 hours |
| Phase 7 | Deployment & Documentation | 3-4 hours |
| **Total** | | **23-30 hours** |

---

## Quick Reference: Key Files

### Backend
- `backend/config/settings.py` - Django settings
- `backend/equipment/models.py` - Database models
- `backend/equipment/views.py` - API endpoints
- `backend/equipment/serializers.py` - DRF serializers
- `backend/requirements.txt` - Python dependencies

### Web Frontend
- `frontend-web/src/App.js` - Main React component
- `frontend-web/src/services/api.js` - API service
- `frontend-web/src/pages/Dashboard.jsx` - Dashboard page
- `frontend-web/package.json` - Node dependencies

### Desktop Frontend
- `frontend-desktop/main.py` - Application entry point
- `frontend-desktop/ui/main_window.py` - Main window
- `frontend-desktop/services/api_service.py` - API calls
- `frontend-desktop/requirements.txt` - Python dependencies

---

## Notes

- Always test with the provided `sample_equipment_data.csv`
- SQLite database will be created automatically on first migration
- Keep authentication simple (Token-based) as per requirements
- Ensure both frontends have identical functionality
- CORS must be configured correctly for cross-origin requests
