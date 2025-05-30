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