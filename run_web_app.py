#!/usr/bin/env python3
"""
TIKR Financial Scraper - Web App Launcher

Quick launcher for the Streamlit web interface from the root directory.
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
        print("Please run: pip install -r web_app/requirements.txt")
        return False

def launch_streamlit():
    """Launch the Streamlit web app."""
    try:
        print("🚀 Starting TIKR Financial Scraper Web App...")
        print("=" * 50)
        print("📊 Initializing Streamlit server...")
        
        # Try different ports if 8501 is busy
        ports_to_try = [8501, 8502, 8503, 8504, 8505]
        process = None
        
        for port in ports_to_try:
            print(f"   Trying port {port}...")
            
            # Start Streamlit in a subprocess with better error handling
            process = subprocess.Popen([
                sys.executable, "-m", "streamlit", "run", "web_app/app.py",
                "--server.port", str(port),
                "--server.headless", "true",
                "--browser.gatherUsageStats", "false"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Wait a moment for the server to start
            time.sleep(3)
            
            # Check if process is still running
            if process.poll() is not None:
                # Process has exited, check for errors
                stdout, stderr = process.communicate()
                if f"Port {port} is already in use" in stderr:
                    print(f"   Port {port} is busy, trying next port...")
                    continue
                else:
                    print(f"❌ Streamlit failed to start on port {port}:")
                    print(f"STDOUT: {stdout}")
                    print(f"STDERR: {stderr}")
                    return
            else:
                # Success! Process is running
                url = f"http://localhost:{port}"
                print(f"✅ Streamlit started successfully on port {port}")
                print(f"🌐 Opening browser at {url}")
                webbrowser.open(url)
                break
        
        if process is None or process.poll() is not None:
            print("❌ Failed to start Streamlit on any available port")
            return
        
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
        print("   pip install -r web_app/requirements.txt")
    except Exception as e:
        print(f"❌ Error launching web app: {e}")

def main():
    """Main launcher function."""
    print("🍎 TIKR Financial Scraper - Web App Launcher")
    print("=" * 60)
    
    # Check if app.py exists
    if not Path("web_app/app.py").exists():
        print("❌ web_app/app.py not found. Make sure you're in the tikr_standalone_app directory.")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Launch the web app
    launch_streamlit()

if __name__ == "__main__":
    main()