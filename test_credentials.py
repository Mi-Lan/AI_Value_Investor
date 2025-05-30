#!/usr/bin/env python3
"""
Test script to verify TIKR credentials are loaded correctly from .env file
"""

import os
import sys
from pathlib import Path

# Add the tikr_scraper to path
sys.path.insert(0, str(Path(__file__).parent))

def test_env_loading():
    """Test .env file loading"""
    print("🔍 Testing .env file loading...")
    
    # Check if .env file exists
    env_paths = [
        Path.cwd() / '.env',
        Path(__file__).parent / '.env',
    ]
    
    env_found = False
    for env_path in env_paths:
        if env_path.exists():
            print(f"✅ Found .env file at: {env_path}")
            env_found = True
            
            # Read and display (censored) contents
            with open(env_path, 'r') as f:
                content = f.read()
                lines = content.strip().split('\n')
                print("\n📄 .env file contents:")
                for line in lines:
                    if line.strip() and not line.strip().startswith('#'):
                        if 'TIKR_EMAIL' in line:
                            parts = line.split('=', 1)
                            if len(parts) == 2:
                                print(f"   {parts[0]}={parts[1]}")
                        elif 'TIKR_PASSWORD' in line:
                            parts = line.split('=', 1)
                            if len(parts) == 2:
                                censored = '*' * (len(parts[1]) - 2) + parts[1][-2:] if len(parts[1]) > 2 else '***'
                                print(f"   {parts[0]}={censored}")
                        else:
                            print(f"   {line}")
            break
    
    if not env_found:
        print("❌ No .env file found!")
        print("💡 Create one using: cp env_example.txt .env")
        return False
    
    return True

def test_credential_loading():
    """Test credential loading through the scraper"""
    print("\n🔍 Testing credential loading through TIKRScraper...")
    
    try:
        from tikr_scraper.tikr_scraper import TIKRScraper
        
        # Create scraper instance (this will test credential loading)
        scraper = TIKRScraper()
        
        print(f"✅ Email loaded: {scraper.username}")
        if scraper.password:
            censored_password = '*' * (len(scraper.password) - 2) + scraper.password[-2:] if len(scraper.password) > 2 else '***'
            print(f"✅ Password loaded: {censored_password}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading credentials: {e}")
        return False

def test_environment_variables():
    """Test environment variable loading"""
    print("\n🔍 Testing environment variables...")
    
    # Load dotenv
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        email = os.getenv('TIKR_EMAIL')
        password = os.getenv('TIKR_PASSWORD')
        
        if email:
            print(f"✅ TIKR_EMAIL found: {email}")
        else:
            print("❌ TIKR_EMAIL not found in environment")
            
        if password:
            censored = '*' * (len(password) - 2) + password[-2:] if len(password) > 2 else '***'
            print(f"✅ TIKR_PASSWORD found: {censored}")
        else:
            print("❌ TIKR_PASSWORD not found in environment")
            
        return bool(email and password)
        
    except Exception as e:
        print(f"❌ Error loading environment variables: {e}")
        return False

def main():
    print("🧪 TIKR Credentials Test")
    print("=" * 50)
    
    # Test 1: .env file exists and readable
    env_test = test_env_loading()
    
    # Test 2: Environment variables load correctly
    env_var_test = test_environment_variables()
    
    # Test 3: Scraper loads credentials correctly
    scraper_test = test_credential_loading()
    
    print("\n📊 Test Results:")
    print("=" * 50)
    print(f"📁 .env file found: {'✅' if env_test else '❌'}")
    print(f"🌍 Environment variables: {'✅' if env_var_test else '❌'}")
    print(f"🤖 Scraper credential loading: {'✅' if scraper_test else '❌'}")
    
    if all([env_test, env_var_test, scraper_test]):
        print("\n🎉 All tests passed! Your credentials are loaded correctly from .env file.")
        print("🚀 Your app is ready to deploy securely!")
    else:
        print("\n⚠️  Some tests failed. Please check your .env file setup.")
        print("\n💡 Quick fix:")
        print("1. Copy env_example.txt to .env")
        print("2. Edit .env with your real TIKR credentials")
        print("3. Run this test again")

if __name__ == "__main__":
    main() 