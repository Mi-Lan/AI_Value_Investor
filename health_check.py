#!/usr/bin/env python3
"""Health check script for TIKR scraper deployment."""

import subprocess
import sys
import os

def test_dependencies():
    """Test that all required dependencies are installed."""
    try:
        import pandas
        import requests
        import selenium
        import yfinance
        import openpyxl
        print("✅ All dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def test_chrome():
    """Test Chrome/ChromeDriver availability."""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.quit()
        print("✅ Chrome/ChromeDriver working")
        return True
    except Exception as e:
        print(f"❌ Chrome/ChromeDriver issue: {e}")
        return False

def test_credentials():
    """Test TIKR credentials availability."""
    email = os.getenv('TIKR_EMAIL')
    password = os.getenv('TIKR_PASSWORD')
    
    if not email or not password:
        print("❌ Missing TIKR credentials in environment")
        return False
    
    if email == "your_email@example.com":
        print("❌ Default credentials detected - update with real credentials")
        return False
        
    print("✅ TIKR credentials configured")
    return True

def test_static_files():
    """Test that required static files exist."""
    static_files = [
        'tikr_scraper/static/Valuation Base.xlsx',
        'tikr_scraper/keys.py',
        'tikr_scraper/tikr_scraper.py'
    ]
    
    missing_files = []
    for file_path in static_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing static files: {missing_files}")
        return False
    
    print("✅ All static files present")
    return True

def test_output_directory():
    """Test output directory is writable."""
    output_dir = "tikr_scraper/outputs"
    try:
        os.makedirs(output_dir, exist_ok=True)
        test_file = os.path.join(output_dir, "test_write.tmp")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print("✅ Output directory writable")
        return True
    except Exception as e:
        print(f"❌ Output directory issue: {e}")
        return False

def main():
    """Run all health checks."""
    print("🔍 Running deployment health checks...")
    print("=" * 50)
    
    checks = [
        test_dependencies(),
        test_chrome(),
        test_credentials(),
        test_static_files(),
        test_output_directory()
    ]
    
    print("=" * 50)
    
    if all(checks):
        print("🎉 All health checks passed - ready for deployment!")
        sys.exit(0)
    else:
        print("❌ Some health checks failed - fix issues before deployment")
        sys.exit(1)

if __name__ == "__main__":
    main() 