"""
TIKR Financial Scraper - Configuration File

Store your TIKR account credentials here for easy access.
This file is more convenient than using environment variables.

IMPORTANT: Keep this file secure and never commit it to version control!
"""

# TIKR Account Credentials
# Replace these with your actual TIKR account details
# Sign up at: https://app.tikr.com/

TIKR_EMAIL = "milanrasovic.f@gmail.com"
TIKR_PASSWORD = "GsHr5-TiP$7uXLn"

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