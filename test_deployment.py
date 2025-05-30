#!/usr/bin/env python3
"""
Deployment Test Script - Verify all dependencies work
Run this before deploying to catch any import issues
"""

import sys
from pathlib import Path

def test_imports():
    """Test all critical imports for TIKR scraper"""
    print("🧪 Testing Critical Dependencies")
    print("=" * 50)
    
    failed_imports = []
    
    # Core dependencies
    critical_imports = [
        ('pandas', 'pandas'),
        ('requests', 'requests'),
        ('openpyxl', 'openpyxl'),
        ('xlsxwriter', 'xlsxwriter'),
        ('dotenv', 'python-dotenv'),
        ('selenium', 'selenium'),
        ('seleniumwire', 'selenium-wire'),
        ('webdriver_manager', 'webdriver-manager'),
        ('yfinance', 'yfinance'),
        ('streamlit', 'streamlit'),
        ('plotly', 'plotly'),
    ]
    
    for module_name, package_name in critical_imports:
        try:
            __import__(module_name)
            print(f"✅ {module_name:15} - OK")
        except ImportError as e:
            print(f"❌ {module_name:15} - MISSING: {e}")
            failed_imports.append(package_name)
    
    print("\n" + "=" * 50)
    
    if failed_imports:
        print("❌ FAILED IMPORTS:")
        for package in failed_imports:
            print(f"   pip install {package}")
        print("\n💡 Run these commands to fix:")
        print(f"   pip install {' '.join(failed_imports)}")
        return False
    else:
        print("✅ All critical dependencies are installed!")
        return True

def test_tikr_scraper_import():
    """Test if TIKRScraper can be imported"""
    print("\n🔍 Testing TIKRScraper Import")
    print("=" * 50)
    
    try:
        # Add current directory to path
        sys.path.insert(0, str(Path(__file__).parent))
        
        from tikr_scraper.tikr_scraper import TIKRScraper
        print("✅ TIKRScraper imported successfully!")
        return True
        
    except Exception as e:
        print(f"❌ TIKRScraper import failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you're in the tikr_standalone_app directory")
        print("2. Check that tikr_scraper/tikr_scraper.py exists")
        print("3. Verify all dependencies are installed")
        return False

def test_streamlit_app():
    """Test if Streamlit app can be imported"""
    print("\n🌐 Testing Streamlit App Import")
    print("=" * 50)
    
    try:
        # Add web_app to path
        sys.path.insert(0, str(Path(__file__).parent / 'web_app'))
        
        # Try importing the app module
        import app
        print("✅ Streamlit app imported successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Streamlit app import failed: {e}")
        print("\n🔧 Check:")
        print("1. web_app/app.py exists")
        print("2. All dependencies are installed")
        print("3. No syntax errors in app.py")
        return False

def main():
    print("🚀 TIKR Deployment Test Suite")
    print("=" * 60)
    print("Testing all components before deployment...")
    print()
    
    # Run all tests
    test1 = test_imports()
    test2 = test_tikr_scraper_import()
    test3 = test_streamlit_app()
    
    print("\n📊 FINAL RESULTS")
    print("=" * 60)
    print(f"Dependencies: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"TIKRScraper:  {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"Streamlit App: {'✅ PASS' if test3 else '❌ FAIL'}")
    
    if all([test1, test2, test3]):
        print("\n🎉 ALL TESTS PASSED!")
        print("🚀 Your app is ready for deployment!")
        print("\n📋 Next steps:")
        print("1. Push to GitHub")
        print("2. Deploy on Streamlit Cloud")
        print("3. Share the URL with friends!")
    else:
        print("\n⚠️  DEPLOYMENT NOT READY")
        print("🔧 Fix the failed tests above before deploying")
        print("\n💡 Common fixes:")
        print("- Run: pip install -r requirements.txt")
        print("- Check file structure")
        print("- Verify all imports work locally first")

if __name__ == "__main__":
    main() 