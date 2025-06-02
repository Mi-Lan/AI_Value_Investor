#!/usr/bin/env python3
"""
TIKR Token Generator for Deployment

This script helps you generate an access token locally for use in deployment environments
where Chrome browser is not available.

Usage:
    python generate_token.py

The generated token can then be set as TIKR_ACCESS_TOKEN environment variable
in your deployment environment (Streamlit Cloud, Heroku, Railway, etc.).
"""

import sys
import os
from pathlib import Path

# Add the tikr_scraper module to path
sys.path.insert(0, str(Path(__file__).parent / 'tikr_scraper'))

def main():
    print("🚀 TIKR Token Generator for Deployment")
    print("=" * 50)
    print()
    
    try:
        from tikr_scraper import TIKRScraper
        
        print("🔧 Initializing TIKR scraper...")
        scraper = TIKRScraper()
        
        print("🔐 Generating access token using Chrome...")
        print("   (This may take 1-2 minutes)")
        print("   Chrome browser will open automatically...")
        print()
        
        # Force local mode to ensure Chrome is used
        os.environ.pop('DEPLOYMENT', None)
        os.environ.pop('STREAMLIT_RUNTIME_ENV', None)
        
        scraper.get_access_token()
        
        if scraper.access_token:
            print("✅ SUCCESS! Access token generated:")
            print()
            print("🔑 TOKEN:")
            print("-" * 80)
            print(scraper.access_token)
            print("-" * 80)
            print()
            
            print("📋 DEPLOYMENT INSTRUCTIONS:")
            print()
            print("1. Copy the token above")
            print("2. Set it as TIKR_ACCESS_TOKEN environment variable in your deployment:")
            print()
            print("   For Streamlit Cloud (secrets.toml):")
            print(f'   TIKR_ACCESS_TOKEN = "{scraper.access_token}"')
            print()
            print("   For Heroku:")
            print(f"   heroku config:set TIKR_ACCESS_TOKEN={scraper.access_token}")
            print()
            print("   For Railway:")
            print(f"   railway env set TIKR_ACCESS_TOKEN={scraper.access_token}")
            print()
            print("3. Also set DEPLOYMENT=true in your deployment environment")
            print("4. Use requirements_deployment.txt instead of requirements.txt")
            print()
            print("⚠️  SECURITY NOTE: Keep this token secure and don't commit it to version control!")
            print()
            print("🎉 Your app is now ready for deployment!")
            
        else:
            print("❌ Failed to generate token")
            print("Please check your TIKR credentials and try again")
            return 1
            
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print()
        print("🔧 Please ensure you have all dependencies installed:")
        print("   pip install -r tikr_scraper/requirements.txt")
        print()
        print("   Required for token generation:")
        print("   - selenium")
        print("   - selenium-wire") 
        print("   - webdriver-manager")
        print("   - Chrome browser")
        return 1
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("🔧 Common solutions:")
        print("1. Check your TIKR credentials in config.py or .env file")
        print("2. Ensure Chrome browser is installed")
        print("3. Check internet connection")
        print("4. Try running with SHOW_BROWSER=True in config.py for debugging")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 