"""
TIKR Financial Scraper - Simplified Web App

A simplified Streamlit web interface that avoids threading issues.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import os
import sys
from datetime import datetime
import traceback
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Enhanced path resolution for Streamlit
def setup_import_paths():
    """Set up import paths for TIKRScraper with detailed logging."""
    try:
        current_file = Path(__file__).resolve()
        current_dir = current_file.parent
        parent_dir = current_dir.parent
        tikr_scraper_dir = parent_dir / "tikr_scraper"
        
        print(f"🔍 DEBUG: Current file: {current_file}")
        print(f"🔍 DEBUG: TIKRScraper dir: {tikr_scraper_dir}")
        print(f"🔍 DEBUG: TIKRScraper exists: {tikr_scraper_dir.exists()}")
        
        # Add paths to sys.path
        paths_to_add = [str(parent_dir), str(tikr_scraper_dir)]
        for path in paths_to_add:
            if path not in sys.path:
                sys.path.insert(0, path)
        
        return tikr_scraper_dir, tikr_scraper_dir.exists()
        
    except Exception as e:
        error_msg = f"Error in setup_import_paths: {e}"
        print(f"❌ {error_msg}")
        return None, False

# Try to import TIKRScraper
tikr_scraper_dir, tikr_exists = setup_import_paths()

TIKRScraper = None
import_error = None

if tikr_exists:
    try:
        print("🔍 DEBUG: Attempting import...")
        from tikr_scraper import TIKRScraper
        print("✅ TIKRScraper imported successfully")
        logger.info("TIKRScraper imported successfully")
    except ImportError as e:
        import_error = f"Import failed: {e}"
        print(f"❌ {import_error}")
        logger.error(import_error)
else:
    import_error = f"TIKRScraper directory not found at: {tikr_scraper_dir}"
    print(f"❌ {import_error}")
    logger.error(import_error)

# Page configuration
st.set_page_config(
    page_title="TIKR Financial Scraper (Simple)",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Main header
    st.title("📊 TIKR Financial Statements Scraper (Simplified)")
    
    # Show import status
    if import_error or TIKRScraper is None:
        st.error("🚨 **CRITICAL ERROR: TIKRScraper Import Failed**")
        with st.expander("🔍 **Click here to see detailed error information**", expanded=True):
            if import_error:
                st.code(import_error, language=None)
            st.write(f"**Looking for TIKRScraper at:** `{tikr_scraper_dir}`")
            st.write(f"**Directory exists:** {tikr_scraper_dir.exists() if tikr_scraper_dir else 'Unknown'}")
            st.write(f"**Current working directory:** `{Path.cwd()}`")
        st.stop()
    
    st.success("✅ **TIKRScraper loaded successfully!**")
    
    # Sidebar
    st.sidebar.header("🔧 Configuration")
    
    # Credentials
    st.sidebar.subheader("TIKR Credentials")
    email = st.sidebar.text_input("TIKR Email", value=os.getenv('TIKR_EMAIL', ''))
    password = st.sidebar.text_input("TIKR Password", type="password", value=os.getenv('TIKR_PASSWORD', ''))
    
    if email and password:
        st.sidebar.success("✅ Credentials provided")
        os.environ['TIKR_EMAIL'] = email
        os.environ['TIKR_PASSWORD'] = password
    else:
        st.sidebar.warning("⚠️ Please provide TIKR credentials")
    
    # Options
    include_live_data = st.sidebar.checkbox("Include Live Market Data", value=True)
    show_debug = st.sidebar.checkbox("Show Debug Information", value=True)
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Enter Stock Ticker")
        ticker = st.text_input("Stock Ticker Symbol", value="AAPL", placeholder="e.g., AAPL, TSLA, MSFT").upper()
        
        if ticker and (not ticker.isalpha() or len(ticker) > 5):
            st.error("❌ Invalid ticker format. Please use 1-5 letters only.")
            return
    
    with col2:
        st.subheader("🚀 Actions")
        
        # Check for existing token
        token_file = Path("outputs/token.tmp")
        if token_file.exists():
            st.success("🔑 Token file found")
        else:
            st.warning("⚠️ No token found")
            st.info("💡 First run will take longer to authenticate")
        
        scrape_button = st.button("Scrape Financial Data", type="primary", use_container_width=True)
    
    # Information section
    st.subheader("📋 What This Scraper Does")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📈 **Income Statement**\nRevenue, expenses, profit metrics")
    with col2:
        st.info("💰 **Cash Flow**\nOperating, investing, financing flows")
    with col3:
        st.info("🏦 **Balance Sheet**\nAssets, liabilities, equity")
    
    # Scraping functionality
    if scrape_button and ticker:
        if not email or not password:
            st.error("❌ Please provide TIKR credentials in the sidebar")
            return
        
        # Simple scraping without threading
        simple_scrape(ticker, include_live_data, show_debug)

def simple_scrape(ticker: str, include_live_data: bool, show_debug: bool):
    """Simplified scraping function without threading."""
    
    # Progress tracking
    progress = st.progress(0)
    status = st.empty()
    
    # Debug log container
    if show_debug:
        st.subheader("🔍 Debug Information")
        debug_area = st.empty()
        debug_logs = []
    
    def add_log(message):
        if show_debug:
            debug_logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
            debug_area.code("\n".join(debug_logs[-15:]), language=None)
        print(message)
    
    try:
        # Initialize
        add_log("Initializing TIKR scraper...")
        status.text("🔧 Initializing TIKR scraper...")
        progress.progress(10)
        
        scraper = TIKRScraper(output_dir="outputs")
        add_log("✅ Scraper initialized")
        
        # Check/generate token
        status.text("🔐 Checking authentication...")
        progress.progress(20)
        
        if not scraper.access_token:
            add_log("No token found, attempting to generate...")
            status.text("🔐 Generating authentication token...")
            st.warning("⚠️ **First-time authentication in progress...**\nThis may take 1-2 minutes. Please wait.")
            
            try:
                scraper.get_access_token()
                add_log("✅ Token generated successfully")
            except Exception as e:
                add_log(f"❌ Token generation failed: {str(e)}")
                st.error("❌ Authentication failed. Please check your credentials and try again.")
                if show_debug:
                    st.code(traceback.format_exc(), language=None)
                return
        else:
            add_log("✅ Using existing token")
        
        # Find company
        add_log(f"Searching for {ticker}...")
        status.text(f"🔍 Searching for {ticker}...")
        progress.progress(30)
        
        trading_id, company_id = scraper.find_company_info(ticker)
        if not trading_id:
            add_log(f"❌ Company {ticker} not found")
            st.error(f"❌ Could not find company information for {ticker}")
            return
        
        add_log(f"✅ Found {ticker} (ID: {trading_id})")
        
        # Fetch financials
        add_log("Fetching financial statements...")
        status.text("📊 Fetching financial statements...")
        progress.progress(60)
        
        scraper.get_financials(trading_id, company_id)
        add_log("✅ Financial statements fetched")
        
        # Fetch live data
        live_data = None
        if include_live_data:
            add_log("Fetching live market data...")
            status.text("📈 Fetching live market data...")
            progress.progress(80)
            
            try:
                live_data = scraper.get_live_market_data(ticker, trading_id)
                add_log("✅ Live market data fetched")
            except Exception as e:
                add_log(f"⚠️ Live data fetch failed: {str(e)}")
                st.warning(f"⚠️ Live market data unavailable: {str(e)}")
        
        # Export
        add_log("Exporting to Excel...")
        status.text("📁 Exporting to Excel...")
        progress.progress(90)
        
        filename = f"{ticker}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        result = scraper.export_to_excel(filename, live_data)
        
        progress.progress(100)
        status.text("✅ Completed!")
        add_log(f"✅ Export completed: {result}")
        
        # Success display
        st.success(f"🎉 **Successfully scraped {ticker} financial statements!**")
        
        # Download button
        if result and Path(result).exists():
            with open(result, "rb") as file:
                st.download_button(
                    label=f"📥 Download {ticker} Financial Data",
                    data=file.read(),
                    file_name=Path(result).name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        
        # Show recent files
        show_recent_files()
        
    except Exception as e:
        add_log(f"❌ Error: {str(e)}")
        st.error(f"❌ **Error during scraping:** {str(e)}")
        if show_debug:
            st.code(traceback.format_exc(), language=None)
    
    finally:
        progress.empty()
        status.empty()

def show_recent_files():
    """Show recently generated files."""
    st.subheader("📁 Recent Files")
    
    outputs_dir = Path("outputs")
    if outputs_dir.exists():
        excel_files = list(outputs_dir.glob("*.xlsx"))
        excel_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        if excel_files:
            for file in excel_files[:3]:  # Show last 3 files
                file_time = datetime.fromtimestamp(file.stat().st_mtime)
                st.write(f"📊 **{file.name}** - {file_time.strftime('%Y-%m-%d %H:%M')}")
        else:
            st.info("No recent files found.")
    else:
        st.info("No outputs directory found.")

if __name__ == "__main__":
    main() 