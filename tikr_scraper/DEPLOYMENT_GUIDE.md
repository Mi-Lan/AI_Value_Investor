# TIKR Scraper Deployment Guide

This guide helps you deploy the TIKR Scraper in production environments where Chrome/WebDriver is not available (like Streamlit Cloud, Heroku, Railway, etc.).

## The Problem

The TIKR Scraper normally uses Chrome WebDriver to automatically log into TIKR and extract access tokens. However, in deployment environments:

1. Chrome browser is often not available
2. WebDriver setup is complex and resource-intensive  
3. GUI interactions are not possible

## The Solution

For deployment, we use a **manual token setup** approach:

1. **Generate a token locally** using Chrome (one time)
2. **Set the token as an environment variable** in deployment
3. **Use deployment-specific requirements** (no Chrome dependencies)

## Step-by-Step Deployment Process

### Step 1: Generate Access Token Locally

Run this locally (where Chrome is available) to get your token:

```python
from tikr_scraper import TIKRScraper

# This will use Chrome to login and extract token
scraper = TIKRScraper()
scraper.get_access_token()
print(f"Your access token: {scraper.access_token}")
```

The token will be saved in `outputs/token.tmp` and printed to console.

### Step 2: Set Environment Variables in Deployment

Set these environment variables in your deployment platform:

```bash
TIKR_EMAIL=your_email@example.com
TIKR_PASSWORD=your_password
TIKR_ACCESS_TOKEN=your_generated_token_here
DEPLOYMENT=true
```

**Platform-specific instructions:**

#### Streamlit Cloud
1. Go to your app settings
2. Add environment variables in the "Secrets" section
3. Use this format in your secrets.toml:
```toml
TIKR_EMAIL = "your_email@example.com"
TIKR_PASSWORD = "your_password"  
TIKR_ACCESS_TOKEN = "your_token_here"
DEPLOYMENT = "true"
```

#### Heroku
```bash
heroku config:set TIKR_EMAIL=your_email@example.com
heroku config:set TIKR_PASSWORD=your_password
heroku config:set TIKR_ACCESS_TOKEN=your_token_here
heroku config:set DEPLOYMENT=true
```

#### Railway
```bash
railway env set TIKR_EMAIL=your_email@example.com
railway env set TIKR_PASSWORD=your_password
railway env set TIKR_ACCESS_TOKEN=your_token_here
railway env set DEPLOYMENT=true
```

### Step 3: Use Deployment Requirements

Use `requirements_deployment.txt` instead of `requirements.txt`:

```bash
pip install -r requirements_deployment.txt
```

This excludes Chrome/WebDriver dependencies that cause deployment issues.

### Step 4: Updated Code Usage

The scraper will automatically detect deployment environment and use the token:

```python
from tikr_scraper import TIKRScraper

# Will automatically use TIKR_ACCESS_TOKEN env variable
scraper = TIKRScraper()

# Will work without Chrome
trading_id, company_id = scraper.find_company_info("AAPL")
if trading_id and company_id:
    scraper.get_financials(trading_id, company_id)
    scraper.export_to_excel("AAPL_analysis.xlsx")
```

## Token Management

### Token Expiration
- TIKR tokens typically expire after several hours/days
- When a token expires, you'll get 502 errors
- Generate a new token locally and update the environment variable

### Security Best Practices
1. **Never commit tokens to version control**
2. **Use environment variables only**
3. **Rotate tokens regularly**
4. **Use deployment platform's secret management**

## Troubleshooting

### Error: "Access token generation requires manual token setup"
- **Cause**: Trying to generate token in deployment environment
- **Solution**: Set `TIKR_ACCESS_TOKEN` environment variable

### Error: "502 Server Error: Bad Gateway"
- **Cause**: Token has expired or is invalid
- **Solution**: Generate new token locally and update environment variable

### Error: "Failed to fetch financial data after 2 attempts"
- **Cause**: Network issues or invalid token
- **Solution**: 
  1. Check token validity
  2. Verify internet connection
  3. Try again later (TIKR server issues)

### Error: "WebDriver error" in deployment
- **Cause**: Chrome dependencies in requirements.txt
- **Solution**: Use `requirements_deployment.txt` instead

## Example Deployment Files

### For Streamlit Cloud
```python
# app.py
import streamlit as st
from tikr_scraper import TIKRScraper

st.title("TIKR Analysis App")

ticker = st.text_input("Enter ticker symbol:", "AAPL")
if st.button("Analyze"):
    try:
        scraper = TIKRScraper()
        trading_id, company_id = scraper.find_company_info(ticker)
        
        if trading_id and company_id:
            scraper.get_financials(trading_id, company_id)
            filename = scraper.export_to_excel(f"{ticker}_analysis.xlsx")
            st.success(f"Analysis complete! Generated {filename}")
        else:
            st.error(f"Company {ticker} not found")
    except Exception as e:
        st.error(f"Error: {e}")
```

### For Flask/FastAPI
```python
# app.py
from flask import Flask, jsonify
from tikr_scraper import TIKRScraper

app = Flask(__name__)

@app.route('/analyze/<ticker>')
def analyze_company(ticker):
    try:
        scraper = TIKRScraper()
        trading_id, company_id = scraper.find_company_info(ticker)
        
        if trading_id and company_id:
            scraper.get_financials(trading_id, company_id)
            return jsonify({
                "success": True,
                "data": scraper.content,
                "message": f"Analysis complete for {ticker}"
            })
        else:
            return jsonify({
                "success": False,
                "message": f"Company {ticker} not found"
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run()
```

## Environment Detection

The scraper automatically detects deployment environments by checking:

- `DEPLOYMENT=true` environment variable
- `STREAMLIT_RUNTIME_ENV` (Streamlit Cloud)
- `HEROKU_APP_NAME` (Heroku)
- `RAILWAY_PROJECT_NAME` (Railway)

This prevents Chrome initialization in deployment environments.

## Support

If you encounter issues:

1. Check your token is valid by testing locally
2. Verify all environment variables are set correctly
3. Use `requirements_deployment.txt` for deployment
4. Check platform-specific deployment logs for details

For additional help, ensure your local setup works first, then follow the deployment steps exactly as outlined above. 