# React Frontend Setup - Chemical Equipment Parameter Visualizer

## ✅ Setup Complete!

The React frontend has been initialized with all required dependencies and project structure.

---

## 📁 Project Structure

```
frontend-web/
├── public/                 # Static files
├── src/
│   ├── components/         # Reusable UI components
│   ├── pages/             # Page components (Login, Dashboard, etc.)
│   ├── services/          # API service layer
│   │   └── api.js         # Backend API calls (configured)
│   ├── context/           # React Context for state management
│   ├── App.js             # Main app component
│   └── index.js           # Entry point
├── .env                   # Environment variables (NOT committed to Git)
├── .env.example           # Environment variables template
└── package.json           # Dependencies
```

---

## 📦 Installed Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| react | 18.x | Core React library |
| react-dom | 18.x | React DOM rendering |
| axios | Latest | HTTP client for API calls |
| chart.js | Latest | Charting library |
| react-chartjs-2 | Latest | React wrapper for Chart.js |
| react-router-dom | Latest | Client-side routing |

---

## ⚙️ Configuration

### API Service (`src/services/api.js`)

✅ **Configured and ready to use!**

Features:
- Base URL: `http://127.0.0.1:8000` (from `.env`)
- Automatic token authentication (interceptor)
- Auto-redirect to login on 401 Unauthorized
- All API methods ready:
  - `registerUser(userData)`
  - `loginUser(credentials)`
  - `logoutUser()`
  - `getUserInfo()`
  - `uploadCSV(file)`
  - `getDatasets()`
  - `getDatasetDetail(datasetId)`
  - `getDatasetSummary(datasetId)`
  - `downloadPDFReport(datasetId)`

### Environment Variables (`.env`)

```env
REACT_APP_API_URL=http://127.0.0.1:8000
REACT_APP_NAME=Chemical Equipment Parameter Visualizer
REACT_APP_VERSION=1.0.0
```

**Note:** `.env` file is in `.gitignore` - secrets are safe!

---

## 🚀 Running the Development Server

### Start React App:

```bash
cd frontend-web
npm start
```

The app will open at **http://localhost:3000**

### Start Django Backend (in another terminal):

```bash
cd backend
.\venv\Scripts\python.exe manage.py runserver
```

Backend runs at **http://127.0.0.1:8000**

---

## 📝 Next Steps (Phase 3 - Remaining Steps)

Now you'll build the actual UI components:

### Step 3.2: Authentication Components ✨ NEXT
- LoginPage.jsx
- RegisterPage.jsx  
- AuthContext.jsx
- ProtectedRoute.jsx

### Step 3.3: File Upload Component
- FileUpload.jsx (drag & drop CSV)

### Step 3.4: Data Table Component
- DataTable.jsx (display equipment data)

### Step 3.5: Chart Components
- TypeDistributionChart.jsx (Pie chart)
- ParameterBarChart.jsx (Bar chart)
- ChartPanel.jsx (container)

### Step 3.6: Summary Card Component
- SummaryCard.jsx (statistics cards)

### Step 3.7: History Component
- HistoryList.jsx (dataset history)

### Step 3.8: Dashboard Page
- Dashboard.jsx (main page with all components)
- Set up React Router

### Step 3.9: Testing
- Test all functionality end-to-end

---

## 🔧 Available Scripts

### `npm start`
Runs the app in development mode at http://localhost:3000

### `npm test`
Launches the test runner

### `npm run build`
Builds the app for production to the `build` folder

---

## 🎨 Styling Options

The setup doesn't include a UI framework yet. You can add one:

### Option 1: Bootstrap (Recommended for quick setup)
```bash
npm install bootstrap react-bootstrap
```

Then add to `src/index.js`:
```javascript
import 'bootstrap/dist/css/bootstrap.min.css';
```

### Option 2: Tailwind CSS (Modern utility-first CSS)
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init
```

### Option 3: Material-UI (Google Material Design)
```bash
npm install @mui/material @emotion/react @emotion/styled
```

### Option 4: Custom CSS
Just create CSS files and import them in components!

---

## 🔐 Using the API Service

### Example: Login

```javascript
import { loginUser, saveAuthToken, saveUserInfo } from './services/api';

const handleLogin = async (username, password) => {
  try {
    const response = await loginUser({ username, password });
    
    // Save token and user info
    saveAuthToken(response.token);
    saveUserInfo(response.user);
    
    // Redirect to dashboard
    navigate('/dashboard');
  } catch (error) {
    console.error('Login failed:', error);
  }
};
```

### Example: Upload CSV

```javascript
import { uploadCSV } from './services/api';

const handleFileUpload = async (file) => {
  try {
    const response = await uploadCSV(file);
    console.log('Upload successful:', response);
  } catch (error) {
    console.error('Upload failed:', error);
  }
};
```

---

## 🐛 Troubleshooting

### CORS Errors
Make sure Django backend has CORS configured for `http://localhost:3000`:
```python
# backend/config/settings.py
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
```

### API Connection Failed
- Verify Django server is running at http://127.0.0.1:8000
- Check `.env` file has correct `REACT_APP_API_URL`
- Restart React dev server after changing `.env`

### Token Not Working
- Check Authorization header format: `Token <token_value>`
- Verify token is saved in localStorage
- Check browser console for errors

---

## 📚 Resources

- [React Documentation](https://react.dev/)
- [Axios Documentation](https://axios-http.com/)
- [Chart.js Documentation](https://www.chartjs.org/)
- [React Router Documentation](https://reactrouter.com/)

---

Ready to build the UI! 🎨 Start with authentication components in the next step.
