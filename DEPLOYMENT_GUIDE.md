# Complete Deployment Guide - ChemViz Pro

**Beginner-friendly guide to deploy your full-stack application**

---

## 🎯 Deployment Strategy

We'll deploy in this order for best results:

```
Step 1: Deploy Backend (Django) → Get API URL ✅
Step 2: Deploy Frontend (React) → Connect to backend ✅
```

**Why this order?**
- Frontend needs the backend URL to make API calls
- Easier to test and debug
- No need to redeploy frontend later

---

## 📋 Prerequisites Checklist

Before starting, make sure you have:
- ✅ GitHub account (sign up at https://github.com if you don't have one)
- ✅ Your project code pushed to GitHub
- ✅ Google Chrome or Firefox browser
- ✅ Email address for account verification

---

## 🚀 Phase 1: Deploy Backend First

**⚠️ IMPORTANT: Deploy the backend before the frontend!**

See the separate **BACKEND_DEPLOYMENT_GUIDE.md** for complete instructions on deploying your Django API to Render.

Once your backend is deployed, you'll get a URL like:
```
https://your-backend-name.onrender.com
```

**Write this URL down! You'll need it in Phase 2.**

---

## 🌐 Phase 2: Deploy Frontend to Vercel

### Prerequisites for This Phase:
- ✅ Backend already deployed and URL obtained
- ✅ Backend API tested and working

---

## Step 1: Prepare Your React App for Deployment

### 1.1: Update Environment Configuration with Backend URL

1. **Open your project folder** in VS Code:
   ```
   C:\Users\AARYA\Desktop\FOSSEE\frontend-web
   ```

2. **Open the `.env.production` file** (already created in `frontend-web` folder)

3. **Update with YOUR backend URL** from Phase 1:
   ```
   REACT_APP_API_URL=https://your-backend-name.onrender.com
   ```
   
   > **⚠️ CRITICAL**: Replace `your-backend-name.onrender.com` with your actual backend URL!
   
   Example:
   ```
   REACT_APP_API_URL=https://chemviz-api.onrender.com
   `1.2: Test Production Build Locally

Open terminal in VS Code and run:

```bash
cd C:\Users\AARYA\Desktop\FOSSEE\frontend-web
npm run build
```

This creates an optimized production build. If there are errors, fix them before deploying.

### 1.3: Push Code to GitHub

```bash
cd C:\Users\AARYA\Desktop\FOSSEE
git add .
git commit -m "Update backend URL for production"
git push origin main
```

---

## Step 2: Deploy to Vercel

### Method A: Deploy via Vercel Website (Recommended)

####d A: Deploy via Vercel Website (Easiest for Beginners)

#### Step 2.1: Create Vercel Account

1. **Go to Vercel**: https://vercel.com
2. **Click "Sign Up"** (top right corner)
3. **Select "Continue with GitHub"**
4. **Authorize Vercel** to access your GitHub account
5. Complete the sign-up process

#### Step 2.2: Import Your Project

1. **Click "Add New..."** button (top right)
2. **Select "Project"**
3. **Import Git Repository**:
   - You'll see your GitHub repositories
   - Find your `FOSSEE` repository
   - Click **"Import"**

#### Step 2.3: Configure Project Settings

On the configuration page:

1. **Project Name**: Leave as default or change (e.g., `chemviz-pro`)

2. **Framework Preset**: 
   - Should auto-detect "Create React App"
   - If not, select it manually

3. **Root Directory**: 
   - Click **"Edit"**
   - Type: `frontend-web`
   - This tells Vercel where your React app is located

4. **Build and Output Settings**:
   - Build Command: `npm run build` (already set)
   - Output Directory: `build` (already set)
   - Install Command: `npm install` (already set)

5. **Environment Variables** (IMPORTANT):
   - Click **"Add"** under Environment Variables
   - Key: `REACT_APP_API_URL`
   - Value: **YOUR BACKEND URL** (e.g., `https://chemviz-api.onrender.com`)
   - ⚠️ Make sure to use HTTPS, not HTTP!
   - Click **"Add"**

6. **Click "Deploy"** button

#### 2.4: Wait for Deployment

- Vercel will now:
  1. Install dependencies
  2. Build your React app
  3. Deploy to their CDN
  
- This takes 2-5 minutes
- You'll see a progress screen with logs

#### Step 2.5: Access Your Deployed Site

Once deployment completes:

1. You'll see a **success screen** with confetti 🎉
2. Your site URL will be shown (e.g., `https://chemviz-pro.vercel.app`)
3. Click the URL to open your deployed website

---

### Method B: Deploy via Vercel CLI (Alternative)

If you prefer using the terminal:

#### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

#### Step 2: Login to Vercel

```bash
vercel login
```

Follow the prompts to authenticate.

#### Step 3: Deploy

```bash
cd C:\Users\AARYA\Desktop\FOSSEE\frontend-web
vercel
```

Follow the interactive prompts:
- **Set up and deploy**: Yes
- **Which scope**: Select your account
- **Link to existing project**: No
- **Project name**: (press Enter for default)
- **Directory**: `./` (it's already in frontend-web)
- **Override settings**: No

#### Step 4: Deploy to Production

```bash
vercel --prod
```

---
Step 3: Test Your Full Application

### 3.1: Open Your Deployed Site

Visit your Vercel URL: `https://your-project-name.vercel.app`

### 3.2: Test Complete Workflow

1. ✅ **Register a new account**
   - Should create account successfully
   - Should automatically log in

2. ✅ **Log out and log back in**
   - Test with the account you just created

3. ✅ **Upload a CSV file**
   - Use your sample data
   - Should process and show results

4. ✅ **View charts and data**
   - All visualizations should load

5. ✅ **Download PDF report**
   - Should generate and download

### 3.3: Check Browser Console

Press **F12** → Console tab
- Should see no errors
- All API calls should return 200/201 status codes

---

## Step 4: Update Backend CORS Settings

If you get CORS errors, update your Django backend:

1. **Add your Vercel URL to allowed origins**
2. **See BACKEND_DEPLOYMENT_GUIDE.md** for CORS configuration

---

##
## Part 4: Troubleshooting Common Issues

### Issue 1: Build Fails with "Module not found"

**Solution**: Install missing dependencies
```bash
cd C:\Users\AARYA\Desktop\FOSSEE\frontend-web
npm install
git add .
git commit -m "Update dependencies"
git push
```

Vercel will auto-redeploy when you push to GitHub.

### Issue 2: Blank Page After Deployment
 (Most Common)

**Symptoms**: Login/Register doesn't work, "Network Error" messages

**Solutions**:
1. **Verify backend URL is correct**:
   - Should be `https://` not `http://`
   - Should not end with `/`
   - Example: `https://chemviz-api.onrender.com`

2. **Check if backend is running**:
   - Visit your backend URL in browser
   - Should show API root or Django admin

3. **Verify CORS settings**:
   - Backend must allow your Vercel domain
   - See BACKEND_DEPLOYMENT_GUIDE.md

4. **Check environment variable in Vercel**:
   - Settings → Environment Variables
   - Verify `REACT_APP_API_URL` is set correctly
   - Redeploy after changing
### Issue 3: API Calls Fail

**Solution**:
1. Check if backend is running
2. Verify `REACT_APP_API_URL` is correct
3. Check CORS settings in Django backend

### Issue 4: 404 on Page Refresh

**Solution**: Vercel needs rewrite rules for React Router

Create `vercel.json` in `frontend-web` folder:

```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

Then push to GitHub:
```bash
git add .
git commit -m "Add Vercel rewrites for React Router"
git push
```

---

## Part 5: Automatic Deployments

**Good news!** Vercel automatically redeploys when you push to GitHub.

Workflow:
1. Make changes to your code
2. Test locally
3. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your change description"
   git push
   ```
4. Vercel automatically builds and deploys
5. Check deployment status on Vercel dashboard

---

## Part 6: Custom Domain (Optional)

Want your own domain like `chemviz.com`?

### Step 1: Buy a Domain
- Recommended: Namecheap, Google Domains, GoDaddy

### Step 2: Add to Vercel
1. Go to **Project Settings** → **Domains**
2. Click **"Add"**
3. Enter your domain
4. Follow DNS configuration instructions
5. Wait for DNS propagation (24-48 hours)

---

## Quick Reference: Vercel Dashboard URLs

- **Dashboard**: https://vercel.com/dashboard
- **Deployments**: https://vercel.com/[your-username]/[project-name]/deployments
- **Settings**: https://vercel.com/[your-username]/[project-name]/settings

---

## Final Checklist

- [ ] Backend deployed and URL obtained
- [ ] `.env.production` updated with backend URL
- [ ] Code committed to GitHub
- [ ] `npm run build` runs without errors
- [ ] Vercel account created
- [ ] Project imported to Vercel
- [ ] Root directory set to `frontend-web`
- [ ] Environment variable `REACT_APP_API_URL` configured correctly
- [ ] Deployment successful
- [ ] Registration tested
- [ ] Login tested
- [ ] File upload tested
- [ ] Charts displayed correctly
- [ ] PDF download works
- [ ] CORS configured in backend (if needed)
## What's Next?

### For Complete Production Deployment:

1. **Deploy Backend**:
   - Use Render (easiest for Django): https://render.com
   - Or Railway: https://railway.app
   - Or PythonAnywhere: https://www.pythonanywhere.com

2. **Update Frontend Environment**:
   - Change `REACT_APP_API_URL` to backend URL
   - Redeploy on Vercel

3. **Configure CORS in Backend**:
   - Add Vercel URL to `ALLOWED_HOSTS` in Django
   - Update CORS settings to allow your Vercel domain

---

## Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Vercel Support**: https://vercel.com/support
- **Vercel Discord**: https://vercel.com/discord

---
**Congratulations!** 🎉 

Your full-stack application is now live on the internet!

- **Frontend**: `https://[your-project-name].vercel.app`
- **Backend**: `https://[your-backend-name].onrender.com`

Share your frontend
Share this URL with anyone to show your project!
