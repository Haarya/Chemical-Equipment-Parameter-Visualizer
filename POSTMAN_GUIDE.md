# 📮 Postman Testing Guide for Beginners

## 🎯 What is Postman?
Postman is a tool for testing APIs. Think of it like a browser, but for APIs instead of websites.

---

## 📥 Step 1: Install Postman

1. Download from: https://www.postman.com/downloads/
2. Install and create a free account (optional but recommended)
3. Open Postman

---

## 🚀 Step 2: Test the API Root

### Create Your First Request:

1. **Click** the `+` button (New Tab) or "New" → "HTTP Request"
2. **Enter URL:** `http://127.0.0.1:8000/`
3. **Method:** Should be `GET` (default)
4. **Click:** Blue "Send" button

**✅ Expected Result:**
```json
{
  "message": "Welcome to Chemical Equipment Parameter Visualizer API",
  "version": "1.0.0",
  "endpoints": {
    ...list of all endpoints...
  }
}
```

---

## 🔐 Step 3: Test Authentication

### A. Register a New User

1. **New Request** (click + button)
2. **Method:** Change dropdown from `GET` to `POST`
3. **URL:** `http://127.0.0.1:8000/api/auth/register/`
4. **Go to "Body" tab** (below the URL bar)
5. **Select:** `raw` (radio button)
6. **Select:** `JSON` from the dropdown (instead of "Text")
7. **Enter this JSON:**
   ```json
   {
     "username": "testuser",
     "email": "test@example.com",
     "password": "test123456"
   }
   ```
8. **Click:** "Send"

**✅ Expected Result (Status: 201 Created):**
```json
{
  "message": "User registered successfully",
  "token": "a1b2c3d4e5f6...long_token_string...",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

**🔑 IMPORTANT:** Copy the token! You'll need it for protected endpoints.

---

### B. Login (Test Existing User)

1. **New Request**
2. **Method:** `POST`
3. **URL:** `http://127.0.0.1:8000/api/auth/login/`
4. **Body tab** → `raw` → `JSON`
5. **Enter:**
   ```json
   {
     "username": "testuser",
     "password": "test123456"
   }
   ```
6. **Send**

**✅ Expected Result:** Same as registration (returns token)

---

### C. Get User Info (Protected Endpoint)

This requires authentication!

1. **New Request**
2. **Method:** `GET`
3. **URL:** `http://127.0.0.1:8000/api/auth/user/`
4. **Go to "Headers" tab**
5. **Add a header:**
   - Key: `Authorization`
   - Value: `Token a1b2c3d4e5f6...` (paste your token from registration/login)
6. **Send**

**✅ Expected Result:**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com"
}
```

**❌ Without Token:** You'll get `401 Unauthorized`

---

## 📤 Step 4: Upload CSV File

1. **New Request**
2. **Method:** `POST`
3. **URL:** `http://127.0.0.1:8000/api/upload/`
4. **Go to "Body" tab**
5. **Select:** `form-data` (radio button)
6. **Add a field:**
   - Key: `file` (type must be "File" - hover over key field, select "File" from dropdown)
   - Value: Click "Select Files" button → Choose `C:\Users\AARYA\Desktop\FOSSEE\sample_data\sample_equipment_data.csv`
7. **Send**

**✅ Expected Result (Status: 201 Created):**
```json
{
  "message": "CSV file uploaded successfully",
  "dataset": {
    "id": 1,
    "name": "sample_equipment_data.csv",
    "total_records": 17,
    "avg_flowrate": 125.5,
    "avg_pressure": 15.2,
    "avg_temperature": 85.3,
    ...
  }
}
```

**💡 Note:** The dataset ID (here: `1`) - you'll use this in next requests!

---

## 📊 Step 5: Get Dataset List

1. **New Request**
2. **Method:** `GET`
3. **URL:** `http://127.0.0.1:8000/api/datasets/`
4. **Headers tab:** Add `Authorization: Token YOUR_TOKEN`
5. **Send**

**✅ Expected Result:**
```json
[
  {
    "id": 1,
    "name": "sample_equipment_data.csv",
    "uploaded_at": "2026-02-04T13:15:00Z",
    "total_records": 17
  }
]
```

---

## 🔍 Step 6: Get Dataset Details

1. **New Request**
2. **Method:** `GET`
3. **URL:** `http://127.0.0.1:8000/api/datasets/1/` (use your dataset ID)
4. **Headers:** `Authorization: Token YOUR_TOKEN`
5. **Send**

**✅ Expected Result:**
```json
{
  "id": 1,
  "name": "sample_equipment_data.csv",
  "uploaded_at": "2026-02-04T13:15:00Z",
  "total_records": 17,
  "equipment_records": [
    {
      "id": 1,
      "equipment_name": "P-101",
      "equipment_type": "Pump",
      "flowrate": 120.5,
      "pressure": 15.2,
      "temperature": 65.0
    },
    ...
  ]
}
```

---

## 📈 Step 7: Get Dataset Summary

1. **Method:** `GET`
2. **URL:** `http://127.0.0.1:8000/api/datasets/1/summary/`
3. **Headers:** `Authorization: Token YOUR_TOKEN`
4. **Send**

---

## 📄 Step 8: Download PDF Report

1. **Method:** `GET`
2. **URL:** `http://127.0.0.1:8000/api/datasets/1/report/pdf/`
3. **Headers:** `Authorization: Token YOUR_TOKEN`
4. **Send**
5. **Click "Save Response" → "Save to a file"** (above the response area)
6. Save as `report.pdf`

**✅ Expected Result:** PDF file downloaded

---

## 🚪 Step 9: Logout

1. **Method:** `POST`
2. **URL:** `http://127.0.0.1:8000/api/auth/logout/`
3. **Headers:** `Authorization: Token YOUR_TOKEN`
4. **Send**

**✅ Expected Result:**
```json
{
  "message": "Logged out successfully"
}
```

**After logout:** Your token is invalidated. Try accessing `/api/auth/user/` again - you'll get 401.

---

## 💾 Bonus: Save Your Requests as a Collection

1. **Click "Collections"** (left sidebar)
2. **Click "+"** → "Create Collection"
3. **Name it:** "Chemical Equipment API"
4. **For each request tab:**
   - Click the dropdown arrow next to "Send"
   - Select "Save As"
   - Choose the collection
   - Give it a name (e.g., "Register User")

Now you can reuse these requests anytime!

---

## 🎓 Common Issues & Solutions

### ❌ "Could not get any response"
- **Solution:** Make sure Django server is running (`python manage.py runserver`)

### ❌ "401 Unauthorized"
- **Solution:** You forgot the Authorization header or token is invalid/expired
- **Check:** Headers tab has `Authorization: Token YOUR_ACTUAL_TOKEN`

### ❌ "404 Not Found"
- **Solution:** Check your URL spelling
- **Tip:** URLs are case-sensitive!

### ❌ "400 Bad Request"
- **Solution:** Check your JSON syntax (missing quotes, commas, brackets)
- **Tip:** Postman shows JSON errors in red

### ❌ CSV upload fails
- **Solution:** Make sure you selected "File" type for the `file` key (hover over key field)

---

## 📱 Quick Reference Card

| Endpoint | Method | Auth Required | Body Type |
|----------|--------|--------------|-----------|
| `/` | GET | No | - |
| `/api/auth/register/` | POST | No | JSON |
| `/api/auth/login/` | POST | No | JSON |
| `/api/auth/logout/` | POST | Yes | - |
| `/api/auth/user/` | GET | Yes | - |
| `/api/upload/` | POST | No | form-data (file) |
| `/api/datasets/` | GET | Yes | - |
| `/api/datasets/<id>/` | GET | Yes | - |
| `/api/datasets/<id>/summary/` | GET | Yes | - |
| `/api/datasets/<id>/report/pdf/` | GET | Yes | - |

**Auth Format:** `Authorization: Token YOUR_TOKEN_HERE`

---

## 🎯 Testing Checklist

- [ ] Register new user
- [ ] Login with credentials
- [ ] Get user info (with token)
- [ ] Try accessing protected endpoint without token (should fail)
- [ ] Upload CSV file
- [ ] List all datasets
- [ ] Get dataset details
- [ ] Get dataset summary
- [ ] Download PDF report
- [ ] Logout
- [ ] Verify token is invalidated (try accessing protected endpoint)

---

## 📚 Next Steps

After testing with Postman:
1. Try uploading 6 CSV files → Verify only last 5 are kept
2. Test invalid CSV formats → Should return proper errors
3. Test with very large CSV → Should reject if over 10MB
4. Ready to build the React frontend! 🚀

---

**Need Help?** 
- Postman Learning Center: https://learning.postman.com/
- Our API Root: http://127.0.0.1:8000/ (shows all endpoints)
