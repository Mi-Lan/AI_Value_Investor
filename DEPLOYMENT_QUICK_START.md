# 🚀 TIKR App Deployment Quick Start

This guide helps you deploy the TIKR app when you encounter Chrome browser errors in production environments.

## 🚨 The Problem

When deploying to cloud platforms (Streamlit Cloud, Heroku, Railway, etc.), you might see errors like:

```
selenium.common.exceptions.WebDriverException: Message: Service /path/to/chromedriver unexpectedly exited. Status code was: 127
Failed to initialize browser. Make sure Chrome is installed.
```

This happens because deployment environments don't have Chrome browser installed.

## ✅ The Solution

### Option 1: Pre-Generated Token (Recommended)

1. **Generate token locally** (where Chrome is available):
   ```bash
   python generate_token.py
   ```

2. **Set environment variables** in your deployment:
   ```bash
   TIKR_EMAIL=your_email@example.com
   TIKR_PASSWORD=your_password
   TIKR_ACCESS_TOKEN=your_generated_token_here
   DEPLOYMENT=true
   ```

3. **Use deployment requirements**:
   ```bash
   pip install -r requirements_deployment.txt
   ```

### Option 2: Environment Variable Only

If you have a valid token from another source:

```bash
# Set these in your deployment environment
TIKR_ACCESS_TOKEN=your_valid_token_here
DEPLOYMENT=true
```

## 🔧 Platform-Specific Setup

### Streamlit Cloud

1. Go to your app settings → Secrets
2. Add to `secrets.toml`:
   ```toml
   TIKR_EMAIL = "your_email@example.com"
   TIKR_PASSWORD = "your_password"
   TIKR_ACCESS_TOKEN = "your_generated_token_here"
   DEPLOYMENT = "true"
   ```

3. Update your requirements file reference to `requirements_deployment.txt`

### Heroku

```bash
heroku config:set TIKR_EMAIL=your_email@example.com
heroku config:set TIKR_PASSWORD=your_password
heroku config:set TIKR_ACCESS_TOKEN=your_generated_token_here
heroku config:set DEPLOYMENT=true
```

### Railway

```bash
railway env set TIKR_EMAIL=your_email@example.com
railway env set TIKR_PASSWORD=your_password
railway env set TIKR_ACCESS_TOKEN=your_generated_token_here
railway env set DEPLOYMENT=true
```

## 🔄 Token Management

### When to Regenerate

Regenerate your token when you see errors like:
- `502 Server Error: Bad Gateway`
- `Failed to fetch financial data after token regeneration`
- Authentication errors

### How to Regenerate

1. Run locally: `python generate_token.py`
2. Update the `TIKR_ACCESS_TOKEN` environment variable
3. Restart your deployment

## 📁 File Structure for Deployment

```
your-app/
├── app.py                          # Your main Streamlit app
├── requirements_deployment.txt     # Deployment dependencies (no Chrome)
├── requirements.txt               # Local dependencies (with Chrome)
├── generate_token.py              # Token generation script
├── tikr_scraper/                  # TIKR scraper module
└── .env                          # Local environment (not deployed)
```

## 🚨 Security Best Practices

1. **Never commit tokens** to version control
2. **Use environment variables** only for sensitive data
3. **Rotate tokens regularly** (every few weeks)
4. **Use platform secrets management** when available

## 🛠️ Troubleshooting

### Error: "DEPLOYMENT MODE: Chrome browser not available"
✅ **Solution**: Set `TIKR_ACCESS_TOKEN` environment variable

### Error: "502 Server Error: Bad Gateway"
✅ **Solution**: Token expired - regenerate and update

### Error: "WebDriver error" during deployment
✅ **Solution**: Use `requirements_deployment.txt` instead of `requirements.txt`

### Local development still uses Chrome
✅ **Expected**: Local environment will continue using Chrome normally

## 🎯 Quick Checklist

- [ ] Generated token using `python generate_token.py`
- [ ] Set `TIKR_ACCESS_TOKEN` environment variable
- [ ] Set `DEPLOYMENT=true` environment variable  
- [ ] Using `requirements_deployment.txt` for deployment
- [ ] Local development still works with Chrome

## 📞 Need Help?

1. Check your token is valid by testing locally first
2. Verify all environment variables are set correctly
3. Ensure you're using the deployment requirements file
4. Check platform-specific deployment logs for details

Your local setup should continue working normally with Chrome, while your deployment will use the pre-generated token! 