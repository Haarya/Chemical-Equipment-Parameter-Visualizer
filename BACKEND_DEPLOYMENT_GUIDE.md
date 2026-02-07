# Backend Deployment Guide (Django) - Render

Beginner-friendly step-by-step guide to deploy your Django backend to Render.

---

## Overview

We will deploy the backend first, then use its URL in the frontend deployment.

Target result:
```
Backend URL example: https://chemviz-api.onrender.com
```

---

## Prerequisites

- GitHub account
- Your project pushed to GitHub
- Render account (free)

---

## Step 1: Prepare Django for Production

### 1.1 Create a production requirements file

In the backend folder, ensure requirements.txt includes:
- Django
- djangorestframework
- django-cors-headers
- pandas
- reportlab
- gunicorn
- psycopg2-binary
- whitenoise

If any are missing, add them.

### 1.2 Add a Procfile (Render uses this)

Create a file named `Procfile` in the backend folder with:
```
web: gunicorn config.wsgi:application
```

### 1.3 Update settings for production

Open `backend/config/settings.py` and ensure the following:

1. **Allowed hosts** includes Render domain:
```
ALLOWED_HOSTS = ["*"]
```

2. **CORS settings** allow your frontend:
```
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend.vercel.app"
]
```

3. **Static files**:
```
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
```

4. **Whitenoise middleware** is enabled:
Add this near the top of MIDDLEWARE:
```
"whitenoise.middleware.WhiteNoiseMiddleware",
```

---

## Step 2: Create Render Account

1. Go to https://render.com
2. Click **Sign Up**
3. Choose **GitHub** to connect your repository
4. Authorize Render access

---

## Step 3: Create New Web Service

1. On Render dashboard, click **New +**
2. Select **Web Service**
3. Choose your GitHub repo
4. Click **Connect**

---

## Step 4: Configure Render Service

Use these settings:

- **Name**: chemviz-api (any name you want)
- **Region**: Choose closest
- **Branch**: main
- **Root Directory**: backend
- **Runtime**: Python
- **Build Command**:
  ```
  pip install -r requirements.txt
  ```
- **Start Command**:
  ```
  gunicorn config.wsgi:application
  ```

---

## Step 5: Add Environment Variables

In Render, click **Environment** and add:

```
DJANGO_SECRET_KEY=your_secret_key_here
DJANGO_DEBUG=False
```

You can generate a secret key with:
```
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

## Step 6: Deploy

1. Click **Create Web Service**
2. Render will build and deploy
3. Wait until status is **Live**

---

## Step 7: Run Migrations

Once deployed, open Render shell:

```
python manage.py migrate
```

---

## Step 8: Test Backend

Open this in browser:
```
https://your-backend-name.onrender.com/api/auth/login/
```

You should see a response (usually 405 for GET, which is OK).

---

## Step 9: Save Backend URL

Copy your backend URL. Example:
```
https://chemviz-api.onrender.com
```

You will use this in the frontend deployment guide.

---

## Troubleshooting

### Issue: Build fails with "Module not found"
- Make sure requirements.txt has all dependencies

### Issue: CORS error in frontend
- Add your Vercel domain in CORS_ALLOWED_ORIGINS
- Redeploy backend

### Issue: 500 server error
- Check Render logs for error details

---

## Next Step

Once backend is live and tested, go back to **DEPLOYMENT_GUIDE.md** and follow Phase 2 to deploy the frontend on Vercel.
