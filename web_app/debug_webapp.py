#!/usr/bin/env python3
"""
Comprehensive debug script for TIKR Web App
Tests all components to ensure everything works before running Streamlit
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test all required imports."""
    print("🧪 Testing imports...")
    
    # Test basic imports
    try:
        import streamlit as st
        print("✅ Streamlit imported")
    except ImportError:
        print("❌ Streamlit not found - run: pip install streamlit")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas imported")
    except ImportError:
        print("❌ Pandas not found")
        return False
    
    # Test TIKRScraper import
    current_dir = Path(__file__).parent.absolute()
    parent_dir = current_dir.parent.absolute()
    tikr_scraper_dir = parent_dir / "tikr_scraper"
    
    print(f"📁 Current dir: {current_dir}")
    print(f"📁 Parent dir: {parent_dir}")
    print(f"📁 TIKRScraper dir: {tikr_scraper_dir}")
    print(f"📁 TIKRScraper exists: {tikr_scraper_dir.exists()}")
    
    if not tikr_scraper_dir.exists():
        print("❌ TIKRScraper directory not found")
        return False
    
    # Add to Python path
    sys.path.insert(0, str(parent_dir))
    sys.path.insert(0, str(tikr_scraper_dir))
    
    try:
        from tikr_scraper.tikr_scraper import TIKRScraper
        print("✅ TIKRScraper imported successfully")
    except ImportError as e:
        print(f"⚠️  Primary import failed: {e}")
        try:
            from tikr_scraper import TIKRScraper
            print("✅ TIKRScraper imported successfully (alternative method)")
        except ImportError as e2:
            print(f"❌ Alternative import failed: {e2}")
            return False
    
    return True

def test_scraper_basic():
    """Test basic scraper functionality."""
    print("\n🧪 Testing scraper functionality...")
    
    try:
        # Import TIKRScraper (should work after test_imports)
        try:
            from tikr_scraper.tikr_scraper import TIKRScraper
        except ImportError:
            from tikr_scraper import TIKRScraper
        
        # Initialize scraper
        scraper = TIKRScraper(output_dir="outputs")
        print("✅ Scraper initialized")
        
        # Test company search
        trading_id, company_id = scraper.find_company_info("AAPL")
        if trading_id:
            print(f"✅ Company search works: AAPL found (ID: {trading_id})")
        else:
            print("❌ Company search failed")
            return False
        
        # Check token
        if scraper.access_token:
            print("✅ Access token found")
        else:
            print("⚠️  No access token (normal for first run)")
        
        return True
        
    except Exception as e:
        print(f"❌ Scraper test failed: {e}")
        return False

def test_credentials():
    """Test credential configuration."""
    print("\n🧪 Testing credentials...")
    
    current_dir = Path(__file__).parent.absolute()
    parent_dir = current_dir.parent.absolute()
    config_file = parent_dir / "tikr_scraper" / "config.py"
    
    if config_file.exists():
        print("✅ Config file found")
        try:
            sys.path.insert(0, str(parent_dir / "tikr_scraper"))
            import config
            if hasattr(config, 'TIKR_EMAIL') and config.TIKR_EMAIL:
                print(f"✅ Email configured: {config.TIKR_EMAIL}")
            if hasattr(config, 'TIKR_PASSWORD') and config.TIKR_PASSWORD:
                print("✅ Password configured")
            return True
        except Exception as e:
            print(f"⚠️  Config file error: {e}")
    else:
        print("⚠️  No config file found")
    
    # Check environment variables
    if os.getenv('TIKR_EMAIL'):
        print("✅ Email in environment")
    if os.getenv('TIKR_PASSWORD'):
        print("✅ Password in environment")
    
    return True

def main():
    """Run all tests."""
    print("🍎 TIKR Web App Debug Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test 1: Imports
    if not test_imports():
        all_tests_passed = False
    
    # Test 2: Basic scraper
    if not test_scraper_basic():
        all_tests_passed = False
    
    # Test 3: Credentials
    test_credentials()
    
    print("\n" + "=" * 50)
    
    if all_tests_passed:
        print("🎉 All tests passed! The web app should work.")
        print("\n🚀 To start the web app:")
        print("   streamlit run app.py")
        print("\n💡 Tips:")
        print("   - Enter TIKR credentials in the sidebar")
        print("   - Enable 'Show Debug Logs' for troubleshooting")
        print("   - First-time token generation takes 1-2 minutes")
    else:
        print("💥 Some tests failed. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 