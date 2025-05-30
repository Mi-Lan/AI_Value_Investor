#!/usr/bin/env python3
"""
🚀 TIKR Financial Scraper - Deployment Assistant
Interactive script to help deploy your app to various platforms
"""

import os
import subprocess
import sys
from pathlib import Path

def print_banner():
    print("""
🚀 TIKR Financial Scraper - Deployment Assistant
================================================
This script will help you deploy your app so friends can access it online!
""")

def check_git_setup():
    """Check if Git is initialized and suggest setup"""
    if not Path('.git').exists():
        print("📦 Setting up Git repository...")
        return False
    return True

def streamlit_cloud_setup():
    """Guide user through Streamlit Cloud deployment"""
    print("""
🌟 STREAMLIT CLOUD DEPLOYMENT (Recommended - FREE!)
===================================================

✅ Benefits:
- Completely FREE forever
- No technical setup required  
- Professional URLs like https://yourapp.streamlit.app
- Auto-deploys when you update code
- Perfect for showing friends!

📋 Steps:
1. Push your code to GitHub (we'll help with this)
2. Go to https://share.streamlit.io/
3. Connect your GitHub account
4. Select your repository 
5. Set main file: web_app/app.py
6. Deploy!

🎯 Your friends will get a public URL they can visit anytime!
""")
    
    proceed = input("🤔 Want to proceed with Streamlit Cloud? (y/n): ").lower().strip()
    if proceed != 'y':
        return
        
    # Check if GitHub repo is set up
    try:
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ GitHub repository already configured: {result.stdout.strip()}")
        else:
            print("📦 Let's set up GitHub repository...")
            github_setup()
    except:
        print("📦 Git not found. Let's set up GitHub repository...")
        github_setup()
    
    print("""
🎉 NEXT STEPS:
1. Go to: https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Choose your repository
5. Set main file path: web_app/app.py
6. Click "Deploy!"

🔗 You'll get a URL like: https://yourapp.streamlit.app
Share this URL with your friends! 🎊
""")

def github_setup():
    """Help user set up GitHub repository"""
    print("""
📦 GITHUB SETUP
===============
We need to put your code on GitHub so Streamlit Cloud can access it.
""")
    
    if not check_git_setup():
        subprocess.run(['git', 'init'])
        print("✅ Git repository initialized")
    
    # Check if there are uncommitted changes
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if result.stdout.strip():
        print("📝 Adding and committing your code...")
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', 'Initial commit - TIKR Financial Scraper'])
        print("✅ Code committed")
    
    # Check if remote is set
    result = subprocess.run(['git', 'remote'], capture_output=True, text=True)
    if 'origin' not in result.stdout:
        print("""
🌐 CREATE GITHUB REPOSITORY:
1. Go to: https://github.com/new
2. Name: tikr-financial-scraper (or whatever you like)  
3. Keep it PUBLIC (required for free Streamlit Cloud)
4. DON'T initialize with README (we have code already)
5. Click "Create repository"
""")
        
        repo_url = input("📝 Enter your GitHub repository URL (https://github.com/username/repo-name.git): ").strip()
        if repo_url:
            subprocess.run(['git', 'remote', 'add', 'origin', repo_url])
            subprocess.run(['git', 'branch', '-M', 'main'])
            subprocess.run(['git', 'push', '-u', 'origin', 'main'])
            print("✅ Code pushed to GitHub!")

def railway_setup():
    """Guide user through Railway deployment"""
    print("""
🚂 RAILWAY DEPLOYMENT (Easy + Always On)
========================================

✅ Benefits:
- $5/month hobby plan (first project often free)
- Always-on (no sleeping like free tiers)
- More powerful than free options
- Custom domains available
- Great performance

📋 Steps:
1. Go to: https://railway.app/
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables:
   - TIKR_EMAIL: your_email@example.com
   - TIKR_PASSWORD: your_password
6. Set start command: streamlit run web_app/app.py --server.port $PORT
7. Deploy!

💰 Cost: ~$5/month for always-on hosting
🔗 You get: https://yourapp.up.railway.app/
""")

def docker_setup():
    """Guide user through Docker deployment"""
    print("""
🐳 DOCKER DEPLOYMENT (Advanced)
===============================

✅ Benefits:
- Deploy anywhere (Google Cloud, AWS, Digital Ocean, etc.)
- Consistent environment
- Scalable
- Professional setup

📋 Quick Test Locally:
""")
    
    proceed = input("🤔 Want to build and test Docker locally first? (y/n): ").lower().strip()
    if proceed == 'y':
        print("🔨 Building Docker image...")
        result = subprocess.run(['docker', 'build', '-t', 'tikr-app', '.'])
        if result.returncode == 0:
            print("✅ Docker image built successfully!")
            print("🚀 Starting container...")
            print("📡 Your app will be available at: http://localhost:8501")
            subprocess.run(['docker', 'run', '-p', '8501:8501', 'tikr-app'])
        else:
            print("❌ Docker build failed. Make sure Docker is installed.")

def heroku_setup():
    """Guide user through Heroku deployment"""
    print("""
🟣 HEROKU DEPLOYMENT
===================

⚠️  Note: Heroku removed their free tier in 2022
💰 Cost: $7+/month for basic dyno

📋 Steps if you want to proceed:
1. Install Heroku CLI
2. heroku create your-app-name
3. git push heroku main
4. heroku ps:scale web=1

🤔 Consider Railway or Streamlit Cloud instead for better value!
""")

def main():
    print_banner()
    
    print("""
🎯 CHOOSE YOUR DEPLOYMENT OPTION:

1. 🌟 Streamlit Cloud (FREE & Easiest!) 
   Perfect for demos and showing friends

2. 🚂 Railway ($5/month)
   Always-on, more powerful, custom domains

3. 🐳 Docker + Cloud Provider
   Most flexible, for advanced users

4. 🟣 Heroku (Not recommended - expensive)

5. ❌ Cancel
""")
    
    choice = input("👆 Enter your choice (1-5): ").strip()
    
    if choice == '1':
        streamlit_cloud_setup()
    elif choice == '2':
        railway_setup()
    elif choice == '3':
        docker_setup()
    elif choice == '4':
        heroku_setup()
    elif choice == '5':
        print("👋 No worries! Run this script anytime when you're ready to deploy.")
        return
    else:
        print("❌ Invalid choice. Please run the script again.")
        return
    
    print("""
🎉 DEPLOYMENT COMPLETE!
======================
Your TIKR Financial Scraper is now ready to share with friends!

💡 Tips for sharing:
- Share the public URL with friends
- They can scrape any stock ticker (AAPL, TSLA, etc.)
- No installation required on their end
- Data exports as Excel files

🛠️  Need help? Check the deployment guide:
   📄 streamlit_deploy_guide.md

Happy scraping! 🚀📊
""")

if __name__ == "__main__":
    main() 