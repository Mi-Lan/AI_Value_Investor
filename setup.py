#!/usr/bin/env python3
"""
TIKR Financial Scraper - Setup Script

This script helps users set up the TIKR scraper by:
1. Installing required dependencies
2. Testing the installation
3. Providing next steps for credential configuration
"""

import subprocess
import sys
import os
from pathlib import Path

def print_banner():
    """Print a welcome banner."""
    print("=" * 60)
    print("🍎 TIKR Financial Scraper - Automated Setup")
    print("=" * 60)
    print("This setup script will install dependencies and test the installation.")
    print("No prompts required - fully automated!\n")

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    else:
        print(f"✅ Python version OK: {version.major}.{version.minor}.{version.micro}")
        return True

def install_dependencies():
    """Install required Python packages."""
    print("\n🔧 Installing dependencies...")
    
    try:
        # Install scraper dependencies
        print("   Installing scraper dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "tikr_scraper/requirements.txt"])
        
        # Install web app dependencies
        print("   Installing web app dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "web_app/requirements.txt"])
        
        print("✅ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("   Try manually running:")
        print("     pip install -r tikr_scraper/requirements.txt")
        print("     pip install -r web_app/requirements.txt")
        return False

def test_installation():
    """Test if the installation works."""
    print("\n🧪 Testing installation...")
    
    try:
        # Test imports
        import pandas
        import requests
        import selenium
        import streamlit
        from dotenv import load_dotenv
        print("✅ All required packages imported successfully")
        
        # Test scraper import
        from tikr_scraper import TIKRScraper
        print("✅ TIKRScraper imported successfully")
        
        # Test basic initialization (without actually scraping)
        scraper = TIKRScraper(output_dir="test_outputs")
        print("✅ TIKRScraper initialized successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return False

def check_credentials():
    """Check if credentials are configured."""
    print("\n🔐 Checking credential configuration...")
    
    # Check tikr_scraper/config.py
    try:
        from tikr_scraper import config
        if hasattr(config, 'TIKR_EMAIL') and hasattr(config, 'TIKR_PASSWORD'):
            email = config.TIKR_EMAIL
            if email and email != "your_email@example.com":
                print(f"✅ Credentials found in tikr_scraper/config.py: {email}")
                return True
    except ImportError:
        pass
    
    # Check .env file
    if Path(".env").exists():
        print("✅ .env file exists (checking for credentials...)")
        from dotenv import load_dotenv
        load_dotenv()
        if os.getenv('TIKR_EMAIL') and os.getenv('TIKR_PASSWORD'):
            print("✅ Credentials found in .env file")
            return True
    
    print("⚠️  No credentials configured yet")
    return False

def show_next_steps(credentials_configured):
    """Show the user what to do next."""
    print("\n🎉 Setup completed successfully!")
    print("=" * 60)
    
    if not credentials_configured:
        print("🔐 CREDENTIAL SETUP REQUIRED:")
        print("\nOption 1 (Recommended):")
        print("   python tikr_scraper/configure_credentials.py")
        
        print("\nOption 2 (Manual):")
        print("   Edit tikr_scraper/config.py file with your TIKR credentials")
        
        print("\nOption 3 (Environment):")
        print("   Create .env file with TIKR_EMAIL and TIKR_PASSWORD")
        print("\n" + "-" * 60)
    
    print("\n🚀 READY TO USE:")
    print("\n1. 🌐 Web Interface:")
    print("   python run_web_app.py")
    print("   streamlit run web_app/app.py")
    
    print("\n2. 💻 Command Line:")
    print("   python run_scraper.py AAPL")
    print("   python run_quick_start.py TSLA MSFT")
    
    print("\n3. 🎮 Demo:")
    print("   python run_demo.py")
    
    print("\n📁 Output files will be saved to the 'outputs' directory")
    print("🔧 Need help? Check README.md for troubleshooting")

def main():
    """Main setup function."""
    print_banner()
    
    # Step 1: Check Python version
    if not check_python_version():
        print("\n❌ Setup failed: Python version incompatible")
        sys.exit(1)
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed at dependency installation")
        print("   Try running manually: pip install -r requirements.txt")
        sys.exit(1)
    
    # Step 3: Test installation
    if not test_installation():
        print("\n⚠️  Installation test failed")
        print("   The scraper might still work, but there may be issues")
    
    # Step 4: Check credentials
    credentials_configured = check_credentials()
    
    # Step 5: Show next steps
    show_next_steps(credentials_configured)

if __name__ == "__main__":
    main() 