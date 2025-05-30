#!/usr/bin/env python3
"""
Deployment Test Script for TIKR Scraper

This script runs comprehensive tests to ensure the scraper works in deployment conditions.
"""

import os
import sys
import time
import subprocess
from pathlib import Path

def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")

def print_step(step, description):
    """Print a formatted step."""
    print(f"\n{step}. {description}")
    print("-" * 40)

def run_command(command, description, timeout=300):
    """Run a command and return success status."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            if result.stdout:
                print(f"Output: {result.stdout[:200]}..." if len(result.stdout) > 200 else f"Output: {result.stdout}")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - TIMEOUT (>{timeout}s)")
        return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def test_virtual_environment():
    """Test in a clean virtual environment."""
    print_header("VIRTUAL ENVIRONMENT TEST")
    
    # Clean up any existing test environment
    if os.path.exists("test_env"):
        run_command("rm -rf test_env", "Cleaning old test environment")
    
    steps = [
        ("python -m venv test_env", "Creating virtual environment"),
        ("source test_env/bin/activate && pip install --upgrade pip", "Upgrading pip"),
        ("source test_env/bin/activate && pip install -r tikr_scraper/requirements.txt", "Installing dependencies"),
        ("source test_env/bin/activate && cd tikr_scraper && python tikr_scraper.py AAPL", "Running scraper test")
    ]
    
    results = []
    for i, (command, description) in enumerate(steps, 1):
        print_step(i, description)
        success = run_command(command, description)
        results.append(success)
        
        if not success and i < 3:  # Stop if setup fails
            print(f"⚠️  Stopping virtual environment test due to setup failure")
            break
    
    # Cleanup
    run_command("rm -rf test_env", "Cleaning up test environment")
    
    return all(results)

def test_headless_mode():
    """Test headless browser mode."""
    print_header("HEADLESS MODE TEST")
    
    print_step(1, "Testing with forced headless mode")
    
    # Set headless environment variable and test
    env_command = "cd tikr_scraper && TIKR_HEADLESS=true python tikr_scraper.py AAPL"
    success = run_command(env_command, "Headless mode test")
    
    return success

def test_output_files():
    """Test that output files are generated correctly."""
    print_header("OUTPUT FILES TEST")
    
    print_step(1, "Checking for recent output files")
    
    outputs_dir = Path("tikr_scraper/outputs")
    if not outputs_dir.exists():
        print(f"❌ Outputs directory not found: {outputs_dir}")
        return False
    
    # Find recent AAPL files
    aapl_files = list(outputs_dir.glob("AAPL_*.xlsx"))
    if not aapl_files:
        print(f"❌ No AAPL output files found in {outputs_dir}")
        return False
    
    latest_file = max(aapl_files, key=os.path.getctime)
    file_age = time.time() - os.path.getctime(latest_file)
    
    if file_age > 3600:  # More than 1 hour old
        print(f"⚠️  Latest file is {file_age/60:.1f} minutes old: {latest_file}")
    else:
        print(f"✅ Recent output file found: {latest_file} ({file_age/60:.1f} minutes old)")
    
    # Check file size
    file_size = latest_file.stat().st_size
    if file_size < 10000:  # Less than 10KB seems too small
        print(f"⚠️  Output file seems small: {file_size} bytes")
        return False
    else:
        print(f"✅ Output file size looks good: {file_size:,} bytes")
    
    return True

def test_dependencies():
    """Test critical dependencies."""
    print_header("DEPENDENCIES TEST")
    
    dependencies = [
        ("python -c 'import pandas; print(f\"pandas {pandas.__version__}\")'", "pandas"),
        ("python -c 'import selenium; print(f\"selenium {selenium.__version__}\")'", "selenium"),
        ("python -c 'import yfinance; print(f\"yfinance {yfinance.__version__}\")'", "yfinance"),
        ("python -c 'import openpyxl; print(f\"openpyxl {openpyxl.__version__}\")'", "openpyxl"),
        ("python -c 'from selenium import webdriver; print(\"WebDriver import OK\")'", "webdriver"),
    ]
    
    results = []
    for i, (command, dep_name) in enumerate(dependencies, 1):
        print_step(i, f"Testing {dep_name}")
        success = run_command(command, f"{dep_name} check")
        results.append(success)
    
    return all(results)

def test_chrome_availability():
    """Test Chrome/ChromeDriver availability."""
    print_header("CHROME/CHROMEDRIVER TEST")
    
    print_step(1, "Testing Chrome installation")
    chrome_success = run_command("google-chrome --version || chrome --version || chromium --version", "Chrome version check")
    
    print_step(2, "Testing ChromeDriver download")
    chromedriver_test = """
python -c "
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
browser_version = driver.capabilities.get('browserVersion', 'Unknown')
print(f'ChromeDriver working, version: {browser_version}')
driver.quit()
"
"""
    chromedriver_success = run_command(chromedriver_test, "ChromeDriver test")
    
    return chrome_success and chromedriver_success

def main():
    """Run all deployment tests."""
    print_header("TIKR SCRAPER DEPLOYMENT TESTING")
    print("This script tests the scraper in deployment-like conditions")
    
    # Change to the script's directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Run all tests
    tests = [
        ("Dependencies Test", test_dependencies),
        ("Chrome/ChromeDriver Test", test_chrome_availability),
        ("Output Files Test", test_output_files),
        ("Headless Mode Test", test_headless_mode),
        ("Virtual Environment Test", test_virtual_environment),
    ]
    
    results = {}
    start_time = time.time()
    
    for test_name, test_func in tests:
        print(f"\n🚀 Starting {test_name}...")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Print summary
    end_time = time.time()
    duration = end_time - start_time
    
    print_header("TEST SUMMARY")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:<30} {status}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    print(f"⏱️  Duration: {duration:.1f} seconds")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED - Ready for deployment!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} tests failed - Fix issues before deployment")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 