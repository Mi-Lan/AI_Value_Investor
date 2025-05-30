#!/usr/bin/env python3
"""
Test script to verify TIKR scraper is working before using web app.
"""

import sys
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

try:
    from tikr_scraper.tikr_scraper import TIKRScraper
    print("✅ Successfully imported TIKRScraper")
except ImportError as e:
    print(f"❌ Failed to import TIKRScraper: {e}")
    sys.exit(1)

def test_scraper():
    """Test basic scraper functionality."""
    print("🧪 Testing TIKR Scraper...")
    
    try:
        # Initialize scraper
        scraper = TIKRScraper(output_dir="outputs")
        print("✅ Scraper initialized")
        
        # Test company search
        print("🔍 Testing company search...")
        trading_id, company_id = scraper.find_company_info("AAPL")
        
        if trading_id:
            print(f"✅ Found AAPL: trading_id={trading_id}, company_id={company_id}")
        else:
            print("❌ Could not find AAPL")
            return False
        
        # Check if token exists
        if scraper.access_token:
            print("✅ Found existing access token")
            return True
        else:
            print("⚠️  No access token found - web app will need to generate one")
            print("💡 This is normal for first run")
            return True
            
    except Exception as e:
        print(f"❌ Error testing scraper: {e}")
        return False

if __name__ == "__main__":
    success = test_scraper()
    if success:
        print("\n🎉 Basic tests passed! The web app should work.")
        print("📱 You can now run: python run_web_app.py")
    else:
        print("\n💥 Tests failed. Please check your setup.")
        sys.exit(1) 