#!/usr/bin/env python3
"""
TIKR Financial Scraper - Web App Launcher

Quick launcher for the Streamlit web interface.
This script automatically opens the web browser and handles the Streamlit startup.
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed."""
    try:
        import streamlit
        import pandas
        import plotly
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Please run: python setup.py")
        return False

def launch_streamlit():
    """Launch the Streamlit web app."""
    try:
        print("🚀 Starting TIKR Financial Scraper Web App...")
        print("=" * 50)
        print("📊 Initializing Streamlit server...")
        
        # Start Streamlit in a subprocess
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Open browser
        url = "http://localhost:8501"
        print(f"🌐 Opening browser at {url}")
        webbrowser.open(url)
        
        print("✅ Web app launched successfully!")
        print("=" * 50)
        print("💡 Usage Tips:")
        print("   • Enter your TIKR credentials in the sidebar")
        print("   • Type any stock ticker (e.g., AAPL, TSLA)")
        print("   • Click 'Scrape Financial Data' to start")
        print("   • Preview and download Excel files")
        print("\n⚠️  Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Wait for the process to complete or be interrupted
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping web app...")
            process.terminate()
            process.wait()
            print("✅ Web app stopped")
            
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install dependencies:")
        print("   pip install streamlit")
    except Exception as e:
        print(f"❌ Error launching web app: {e}")

def main():
    """Main launcher function."""
    print("🍎 TIKR Financial Scraper - Web App Launcher")
    print("=" * 60)
    
    # Check if app.py exists
    if not Path("app.py").exists():
        print("❌ app.py not found. Make sure you're in the correct directory.")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Launch the web app
    launch_streamlit()

if __name__ == "__main__":
    main() 