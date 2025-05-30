#!/usr/bin/env python3
"""
Main entry point for TIKR Financial Scraper Web App
Optimized for Streamlit Cloud deployment
"""

import sys
import os

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import and run the main web app
try:
    # Try to import and run the main streamlit app
    import streamlit as st
    from web_app.app import main
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    import streamlit as st
    st.error(f"""
    🚨 **Import Error**: {str(e)}
    
    This usually means some dependencies are missing.
    
    **For local development:**
    ```bash
    pip install -r requirements.txt
    ```
    
    **For Streamlit Cloud:**
    Make sure your `requirements.txt` includes all necessary packages.
    """)
    st.stop()

except Exception as e:
    import streamlit as st
    st.error(f"""
    🚨 **Application Error**: {str(e)}
    
    Something went wrong while starting the app.
    Please check the logs or contact the developer.
    """)
    st.stop() 