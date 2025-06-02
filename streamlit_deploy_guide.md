# 🚀 Deploy Your TIKR App to Streamlit Cloud

## Option 1: Streamlit Cloud (Recommended - FREE!)

### Prerequisites:
1. GitHub account
2. Your app pushed to a GitHub repository

### Steps:
1. **Push to GitHub:**
   ```bash
   cd tikr_standalone_app
   git init
   git add .
   git commit -m "Initial commit - TIKR Financial Scraper"
   git branch -M main
   git remote add origin https://github.com/yourusername/tikr-app.git
   git push -u origin main
   ```

2. **Visit:** https://share.streamlit.io/

3. **Connect GitHub & Deploy:**
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `web_app/app.py`
   - Click "Deploy!"

4. **Share the URL:** Your friends get a public URL like `https://yourapp.streamlit.app`

### ✅ Pros:
- Completely FREE
- Auto-deploys on code changes
- No setup hassle
- Professional URL
- Handles all infrastructure

### ⚠️ Limitations:
- Resources are limited (but fine for demos)
- Apps sleep after inactivity (wake up on first visit)

---

## Option 2: Railway (Super Easy + More Power)

### Steps:
1. **Visit:** https://railway.app/
2. **Connect GitHub** repository
3. **Add environment variables** (TIKR_EMAIL, TIKR_PASSWORD)
4. **Set start command:** `streamlit run web_app/app.py --server.port $PORT`
5. **Deploy!**

### ✅ Pros:
- $5/month for hobby plan
- Always-on (no sleeping)
- Custom domains
- More resources

---

## Option 3: Docker + Any Cloud Provider

### Create Dockerfile:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "web_app/app.py", "--server.address=0.0.0.0"]
```

Deploy to:
- **Render** (free tier available)
- **Fly.io** (generous free tier)
- **Google Cloud Run** (pay per use)
- **Heroku** (paid plans only now)

---

## Quick Setup for Streamlit Cloud:

1. **Create `.streamlit/config.toml`:**
```toml
[server]
headless = true
port = 8501

[browser]
gatherUsageStats = false
```

2. **Create `app_main.py` (entry point for Streamlit Cloud):**
```python
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web_app.app import *
```

3. **Push to GitHub and deploy on Streamlit Cloud!** 

## The Problem
When deploying the TIKR Scraper to Streamlit Cloud, the app cannot generate access tokens automatically because:

1. Chrome browser is not available in the Streamlit Cloud environment
2. Selenium WebDriver cannot run properly in the cloud environment
3. Headless browser automation is blocked or unreliable

## The Solution: Using Streamlit Secrets

This app has been updated to automatically detect when it's running in a deployment environment and use a pre-generated token instead of trying to use Chrome.

## Step-by-Step Deployment Guide

### Step 1: Generate a Token Locally

First, run the app locally to generate a token. You'll need:
- Chrome installed
- Valid TIKR credentials

Run the app locally and let it generate a token. The token will be stored in the `outputs/token.tmp` file.

```bash
# Open the token file and copy its contents
cat outputs/token.tmp
```

### Step 2: Configure Streamlit Secrets

1. In your Streamlit Cloud dashboard, go to your app settings
2. Open the "Secrets" section 
3. Add the following to your secrets (replacing with your values):

```toml
# TIKR Scraper Secrets Configuration
# For Streamlit Community Cloud deployment

# Credentials - Replace with your actual TIKR account credentials
# These will be used automatically without prompting in the UI
TIKR_EMAIL = "your_email@example.com"
TIKR_PASSWORD = "your_password"

# Deployment flag - MUST be set to "true"
IS_DEPLOYMENT = "true"

# Pre-generated access token (required for deployment)
# Paste your locally generated token here
TOKEN = "your_locally_generated_token"
```

With this configuration:
- The app will run in deployment mode
- It will use your provided credentials automatically (no UI prompt)
- It will use the pre-generated token instead of trying to use Chrome

### Step 3: Deploy Your App

Deploy your app as normal to Streamlit Cloud. The app will automatically:
1. Detect it's running in deployment mode
2. Use the pre-generated token from secrets
3. Skip Chrome/WebDriver initialization

### Step 4: Token Renewal

TIKR tokens typically expire after a certain period. When this happens:

1. Run the app locally to generate a new token
2. Copy the new token from `outputs/token.tmp`
3. Update the `TOKEN` value in your Streamlit Cloud secrets

## Troubleshooting

### Error: "Running in deployment mode but no TOKEN provided"
- **Cause**: Missing TOKEN in Streamlit secrets
- **Solution**: Add the TOKEN to your secrets as shown above

### Error: "502 Server Error: Bad Gateway"
- **Cause**: Token has expired
- **Solution**: Generate a new token locally and update your secrets

### Error: "Failed to fetch financial data after token regeneration"
- **Cause**: Invalid token or network issues
- **Solution**: Generate a new token locally and update your secrets

## Advanced: Managing Tokens

For production deployments, consider:
1. Setting up a scheduled job to generate tokens
2. Implementing a token rotation system
3. Using a secure method to transfer tokens to your deployment 