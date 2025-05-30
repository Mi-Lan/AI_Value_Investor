#!/usr/bin/env python3
"""
TIKR Financial Scraper - Credential Configuration Script

This script helps you easily configure your TIKR account credentials
by updating the config.py file with your login details.
"""

import os
import sys
from pathlib import Path

def print_banner():
    """Print a welcome banner."""
    print("=" * 60)
    print("🔐 TIKR Credential Configuration")
    print("=" * 60)
    print("This script will help you configure your TIKR account credentials.")
    print("Your credentials will be stored in config.py for easy access.\n")

def check_existing_config():
    """Check if config.py exists and has credentials."""
    config_file = Path("config.py")
    
    if not config_file.exists():
        print("❌ config.py file not found!")
        print("Please make sure you're in the correct directory.")
        return False
    
    try:
        with open(config_file, 'r') as f:
            content = f.read()
            
        if 'your_email@example.com' in content:
            print("📝 Found config.py with default template values")
            return True
        else:
            print("✅ config.py exists and appears to have been configured")
            choice = input("Do you want to update your credentials? (y/n): ").lower()
            return choice == 'y'
            
    except Exception as e:
        print(f"❌ Error reading config.py: {e}")
        return False

def get_credentials():
    """Get TIKR credentials from user input."""
    print("\nPlease enter your TIKR account credentials:")
    print("(Sign up at https://app.tikr.com/ if you don't have an account)\n")
    
    while True:
        email = input("TIKR Email: ").strip()
        if email and "@" in email:
            break
        print("❌ Please enter a valid email address")
    
    while True:
        password = input("TIKR Password: ").strip()
        if password:
            break
        print("❌ Password cannot be empty")
    
    return email, password

def update_config_file(email, password):
    """Update the config.py file with new credentials."""
    config_file = Path("config.py")
    
    try:
        # Read current config
        with open(config_file, 'r') as f:
            content = f.read()
        
        # Replace credentials
        content = content.replace('TIKR_EMAIL = "your_email@example.com"', f'TIKR_EMAIL = "{email}"')
        content = content.replace('TIKR_PASSWORD = "your_password"', f'TIKR_PASSWORD = "{password}"')
        
        # Write updated config
        with open(config_file, 'w') as f:
            f.write(content)
        
        print("✅ config.py updated successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error updating config.py: {e}")
        return False

def test_credentials():
    """Test if the credentials can be loaded."""
    try:
        # Try to import the updated config
        import importlib
        import sys
        
        # Clear any cached import
        if 'config' in sys.modules:
            importlib.reload(sys.modules['config'])
        
        from . import config
        
        if hasattr(config, 'TIKR_EMAIL') and hasattr(config, 'TIKR_PASSWORD'):
            email = config.TIKR_EMAIL
            if email != "your_email@example.com" and email:
                print(f"✅ Credentials test passed!")
                print(f"   Email: {email}")
                print(f"   Password: {'*' * len(config.TIKR_PASSWORD)}")
                return True
        
        print("❌ Credentials test failed - config not properly updated")
        return False
        
    except Exception as e:
        print(f"❌ Error testing credentials: {e}")
        return False

def show_next_steps():
    """Show what to do next."""
    print("\n🎉 Credential configuration completed!")
    print("=" * 60)
    print("Your TIKR credentials are now stored in config.py")
    print("\nNext steps:")
    print("\n1. 🌐 Launch Web Interface:")
    print("   streamlit run app.py")
    print("   OR")
    print("   python run_web_app.py")
    
    print("\n2. 💻 Use Command Line:")
    print("   python tikr_scraper.py AAPL")
    print("   python tikr_scraper.py TSLA")
    
    print("\n3. 🎮 Try Demo:")
    print("   python demo.py")
    
    print("\n🔒 Security Notes:")
    print("   • Keep config.py secure and never share it")
    print("   • Don't commit config.py to version control")
    print("   • You can change credentials anytime by running this script again")

def main():
    """Main configuration function."""
    print_banner()
    
    # Check if we're in the right directory
    if not Path("tikr_scraper.py").exists():
        print("❌ tikr_scraper.py not found!")
        print("Please run this script from the tikr_scraper directory.")
        sys.exit(1)
    
    # Check existing config
    if not check_existing_config():
        sys.exit(1)
    
    # Get credentials from user
    try:
        email, password = get_credentials()
    except KeyboardInterrupt:
        print("\n\n❌ Configuration cancelled by user")
        sys.exit(1)
    
    # Confirm before updating
    print(f"\n📋 Configuration Summary:")
    print(f"   Email: {email}")
    print(f"   Password: {'*' * len(password)}")
    
    confirm = input("\nSave these credentials to config.py? (y/n): ").lower()
    if confirm != 'y':
        print("❌ Configuration cancelled")
        sys.exit(1)
    
    # Update config file
    if not update_config_file(email, password):
        sys.exit(1)
    
    # Test the configuration
    if not test_credentials():
        print("⚠️  Configuration saved but test failed")
        print("You may need to restart Python for changes to take effect")
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main() 