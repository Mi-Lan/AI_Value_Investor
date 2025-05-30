#!/usr/bin/env python3
"""
TIKR Web App Startup Script

This script tests the setup and launches the web app with clear status information.
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def check_setup():
    """Check if everything is set up correctly."""
    print("🧪 Checking setup...")
    
    # Run the debug script first
    try:
        result = subprocess.run([sys.executable, "debug_webapp.py"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Setup check passed!")
            return True
        else:
            print("❌ Setup check failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("⚠️  Setup check timed out")
        return False
    except Exception as e:
        print(f"❌ Setup check error: {e}")
        return False

def launch_webapp():
    """Launch the Streamlit web app."""
    print("\n🚀 Launching TIKR Web App...")
    print("=" * 50)
    
    try:
        # Start Streamlit
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8506",
            "--server.headless", "false",
            "--browser.gatherUsageStats", "false"
        ])
        
        # Wait a moment for server to start
        print("📡 Starting Streamlit server...")
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Streamlit server started successfully!")
            
            url = "http://localhost:8506"
            print(f"🌐 Web app URL: {url}")
            print("\n💡 Usage Instructions:")
            print("   1. The web app should open automatically in your browser")
            print("   2. If there are import errors, they'll be shown prominently")
            print("   3. Enable 'Show Debug Logs' in the sidebar for detailed info")
            print("   4. Enter a ticker symbol and click 'Scrape Financial Data'")
            print("\n⚠️  Press Ctrl+C to stop the server when done")
            print("=" * 50)
            
            # Try to open browser
            try:
                webbrowser.open(url)
            except:
                print("⚠️  Could not open browser automatically")
                print(f"   Please open {url} manually")
            
            # Wait for user to stop
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Stopping web app...")
                process.terminate()
                process.wait()
                print("✅ Web app stopped")
        else:
            print("❌ Streamlit server failed to start")
            return False
            
    except Exception as e:
        print(f"❌ Error launching web app: {e}")
        return False
    
    return True

def main():
    """Main function."""
    print("🍎 TIKR Financial Scraper - Web App Launcher")
    print("=" * 60)
    
    # Check setup first
    if not check_setup():
        print("\n💥 Setup check failed. Please fix the issues and try again.")
        print("\n🔧 Common fixes:")
        print("   1. Make sure you're in the /tikr_standalone_app/web_app/ directory")
        print("   2. Run: pip install streamlit pandas plotly openpyxl")
        print("   3. Check that ../tikr_scraper/ directory exists")
        return 1
    
    # Launch the web app
    if not launch_webapp():
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 