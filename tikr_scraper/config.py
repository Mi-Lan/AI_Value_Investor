"""
TIKR Financial Scraper - Configuration File

Store your TIKR account credentials here for easy access.
This file is more convenient than using environment variables.

IMPORTANT: DO NOT PUT REAL CREDENTIALS IN THIS FILE!
This file may be shared publicly or committed to version control.

Instead, use one of these secure methods:
1. Environment variables (.env file)
2. Streamlit secrets (for cloud deployment)
3. User input in the web interface
"""

# Demo/placeholder credentials (DO NOT USE REAL ONES!)
TIKR_EMAIL = "your_email@example.com"
TIKR_PASSWORD = "your_password"

# Optional: Output directory for Excel files
DEFAULT_OUTPUT_DIR = "outputs"

# Optional: Debug settings
DEBUG_MODE = False
SHOW_BROWSER = False  # Set to True to see browser during scraping

# Notes:
# - Free TIKR accounts have limitations on historical data
# - Paid accounts provide full access to all financial statements  
# - 2FA is not supported - ensure it's disabled on your account
# - This file takes precedence over .env file if both are present 