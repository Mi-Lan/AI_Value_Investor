#!/usr/bin/env python3
"""
TIKR Web App Launcher - Choose Your Version

Launch either the full-featured or simplified version of the TIKR web app.
"""

import subprocess
import sys
import os
from pathlib import Path

def show_menu():
    """Show version selection menu."""
    print("🍎 TIKR Financial Scraper - Web App Launcher")
    print("=" * 60)
    print()
    print("Choose your version:")
    print()
    print("1. 🚀 **Full Version** (app.py)")
    print("   ✅ Complete feature set with detailed logging")
    print("   ✅ Real-time progress updates")
    print("   ✅ Comprehensive error handling")
    print("   ⚠️  May have occasional threading issues")
    print()
    print("2. 🎯 **Simplified Version** (app_simple.py)")
    print("   ✅ No threading issues")
    print("   ✅ Reliable and stable")
    print("   ✅ Easier debugging")
    print("   ⚠️  Less detailed progress tracking")
    print()
    print("3. 🧪 **Debug Test** (debug_webapp.py)")
    print("   ✅ Test setup without launching web app")
    print()
    print("4. ❌ **Exit**")
    print()

def launch_app(app_file, port):
    """Launch the specified app."""
    print(f"\n🚀 Launching {app_file}...")
    print("=" * 50)
    
    try:
        # Start Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", app_file,
            "--server.port", str(port),
            "--browser.gatherUsageStats", "false"
        ]
        
        print(f"📡 Starting Streamlit server on port {port}...")
        print(f"🌐 URL: http://localhost:{port}")
        print("⚠️  Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Run the command
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping web app...")
    except Exception as e:
        print(f"❌ Error launching app: {e}")

def run_debug():
    """Run the debug test."""
    print("\n🧪 Running debug test...")
    print("=" * 50)
    
    try:
        result = subprocess.run([sys.executable, "debug_webapp.py"], 
                              capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Debug test error: {e}")
        return False

def main():
    """Main launcher function."""
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("❌ Error: app.py not found")
        print("Make sure you're running this from the /tikr_standalone_app/web_app/ directory")
        sys.exit(1)
    
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == "1":
                launch_app("app.py", 8507)
                break
            elif choice == "2":
                launch_app("app_simple.py", 8508)
                break
            elif choice == "3":
                if run_debug():
                    print("\n✅ Debug test passed!")
                    input("Press Enter to continue...")
                else:
                    print("\n❌ Debug test failed!")
                    input("Press Enter to continue...")
            elif choice == "4":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                input("Press Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main() 