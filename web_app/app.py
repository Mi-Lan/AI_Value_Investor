"""
TIKR Financial Scraper - Web App

A modern Streamlit web interface for the TIKR financial statements scraper.
This provides an easy-to-use GUI for scraping financial data from any publicly traded company.
"""

# Fix for yfinance cache issues on Streamlit Cloud
try:
    import appdirs as ad
    ad.user_cache_dir = lambda *args: "/tmp"
except ImportError:
    pass

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os
import time
from datetime import datetime
import sys
import traceback
import logging

# Set up logging for better error tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Enhanced path resolution for Streamlit
def setup_import_paths():
    """Set up import paths for TIKRScraper with detailed logging."""
    try:
        # Get the actual file location
        current_file = Path(__file__).resolve()
        current_dir = current_file.parent
        parent_dir = current_dir.parent
        tikr_scraper_dir = parent_dir / "tikr_scraper"
        
        print(f"🔍 DEBUG: Current file: {current_file}")
        print(f"🔍 DEBUG: Current dir: {current_dir}")
        print(f"🔍 DEBUG: Parent dir: {parent_dir}")
        print(f"🔍 DEBUG: TIKRScraper dir: {tikr_scraper_dir}")
        print(f"🔍 DEBUG: TIKRScraper exists: {tikr_scraper_dir.exists()}")
        print(f"🔍 DEBUG: Python path before: {sys.path[:3]}")
        
        # Add paths to sys.path if not already there
        paths_to_add = [str(parent_dir), str(tikr_scraper_dir)]
        for path in paths_to_add:
            if path not in sys.path:
                sys.path.insert(0, path)
                print(f"🔍 DEBUG: Added to path: {path}")
        
        print(f"🔍 DEBUG: Python path after: {sys.path[:5]}")
        
        return tikr_scraper_dir, tikr_scraper_dir.exists()
        
    except Exception as e:
        error_msg = f"Error in setup_import_paths: {e}"
        print(f"❌ {error_msg}")
        logger.error(error_msg)
        return None, False

# Try to import TIKRScraper with comprehensive error handling
tikr_scraper_dir, tikr_exists = setup_import_paths()

TIKRScraper = None
import_error = None

if tikr_exists:
    try:
        print("🔍 DEBUG: Attempting primary import...")
        from tikr_scraper.tikr_scraper import TIKRScraper
        print("✅ TIKRScraper imported successfully (primary method)")
        logger.info("TIKRScraper imported successfully")
    except ImportError as e:
        print(f"⚠️  Primary import failed: {e}")
        try:
            print("🔍 DEBUG: Attempting alternative import...")
            from tikr_scraper import TIKRScraper
            print("✅ TIKRScraper imported successfully (alternative method)")
            logger.info("TIKRScraper imported successfully (alternative method)")
        except ImportError as e2:
            import_error = f"Both import methods failed:\n1. Primary: {e}\n2. Alternative: {e2}"
            print(f"❌ {import_error}")
            logger.error(import_error)
else:
    import_error = f"TIKRScraper directory not found at: {tikr_scraper_dir}"
    print(f"❌ {import_error}")
    logger.error(import_error)

# Page configuration
st.set_page_config(
    page_title="TIKR Financial Scraper",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-box {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Main header
    st.markdown('<h1 class="main-header">📊 TIKR Financial Statements Scraper</h1>', unsafe_allow_html=True)
    
    # Show import status and errors prominently
    if import_error or TIKRScraper is None:
        st.error("🚨 **CRITICAL ERROR: TIKRScraper Import Failed**")
        
        with st.expander("🔍 **Click here to see detailed error information**", expanded=True):
            st.markdown("### Import Error Details:")
            if import_error:
                st.code(import_error, language=None)
            
            st.markdown("### Debug Information:")
            if tikr_scraper_dir:
                st.write(f"**Looking for TIKRScraper at:** `{tikr_scraper_dir}`")
                st.write(f"**Directory exists:** {tikr_scraper_dir.exists() if tikr_scraper_dir else 'Unknown'}")
            
            st.write(f"**Current working directory:** `{Path.cwd()}`")
            st.write(f"**App file location:** `{Path(__file__).resolve()}`")
            
            st.markdown("### Python Path:")
            for i, path in enumerate(sys.path[:10]):
                st.write(f"{i+1}. `{path}`")
            
            st.markdown("### Troubleshooting Steps:")
            st.markdown("""
            1. **Check file structure:** Make sure you're running from `/tikr_standalone_app/web_app/`
            2. **Verify tikr_scraper exists:** The folder `../tikr_scraper/` should exist
            3. **Check permissions:** Make sure all files are readable
            4. **Try command line:** Run `python debug_webapp.py` first
            5. **Restart Streamlit:** Sometimes a fresh restart helps
            """)
        
        st.stop()
    
    # Success message
    st.success("✅ **TIKRScraper loaded successfully!**")
    
    # Sidebar for configuration
    st.sidebar.header("🔧 Configuration")
    
    # System status in sidebar
    with st.sidebar.expander("🔍 System Status"):
        st.write("**Import Status:** ✅ Success")
        st.write(f"**TIKRScraper Location:** `{tikr_scraper_dir}`")
        st.write(f"**Python Version:** {sys.version_info.major}.{sys.version_info.minor}")
    
    # Try to get credentials from Streamlit secrets or environment variables
    email = ''
    password = ''
    credentials_source = 'None'
    
    # Priority 1: Check Streamlit secrets
    try:
        if 'TIKR_EMAIL' in st.secrets and 'TIKR_PASSWORD' in st.secrets:
            email = st.secrets['TIKR_EMAIL']
            password = st.secrets['TIKR_PASSWORD']
            if email and password and email != "your_email@example.com":
                credentials_source = 'Streamlit Secrets'
                # Set environment variables for TIKRScraper to use
                os.environ['TIKR_EMAIL'] = email
                os.environ['TIKR_PASSWORD'] = password
    except Exception:
        pass
    
    # Priority 2: Check environment variables if not in secrets
    if not email or not password or email == "your_email@example.com":
        env_email = os.getenv('TIKR_EMAIL', '')
        env_password = os.getenv('TIKR_PASSWORD', '')
        if env_email and env_password and env_email != "your_email@example.com":
            email = env_email
            password = env_password
            credentials_source = 'Environment Variables'
    
    # Display credentials source
    if credentials_source != 'None':
        st.sidebar.success(f"✅ Credentials loaded from {credentials_source}")
    
    # Priority 3: Ask user for credentials if not found elsewhere
    show_credential_inputs = not (email and password and email != "your_email@example.com")
    
    if show_credential_inputs:
        # Credentials section
        st.sidebar.subheader("TIKR Credentials")
        st.sidebar.warning("⚠️ Credentials not found in secrets or environment")
        
        email_input = st.sidebar.text_input("TIKR Email", value=email)
        password_input = st.sidebar.text_input("TIKR Password", type="password", value='')
        
        if email_input and password_input:
            st.sidebar.success("✅ Credentials provided")
            # Temporarily set environment variables
            os.environ['TIKR_EMAIL'] = email_input
            os.environ['TIKR_PASSWORD'] = password_input
            email = email_input
            password = password_input
        else:
            st.sidebar.warning("⚠️ Please provide TIKR credentials")
    
    # Options
    st.sidebar.subheader("Options")
    include_live_data = st.sidebar.checkbox("Include Live Market Data", value=True)
    show_debug_logs = st.sidebar.checkbox("Show Debug Logs", value=True)  # Default to True for debugging
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Enter Stock Ticker")
        ticker_input = st.text_input(
            "Stock Ticker Symbol", 
            value="AAPL",
            placeholder="e.g., AAPL, TSLA, MSFT, GOOGL",
            help="Enter a valid stock ticker symbol (1-5 letters)"
        ).upper()
        
        # Validate ticker
        if ticker_input and (not ticker_input.isalpha() or len(ticker_input) > 5):
            st.error("❌ Invalid ticker format. Please use 1-5 letters only.")
            return
    
    with col2:
        st.subheader("🚀 Actions")
        scrape_button = st.button("Scrape Financial Data", type="primary", use_container_width=True)
        
        if st.button("View Sample Data", use_container_width=True):
            show_sample_data()
    
    # Information cards
    st.subheader("📋 What This Scraper Does")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>📈 Income Statement</h4>
            <p>Revenue, expenses, profit/loss metrics, operating income, net income, EPS</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>💰 Cash Flow</h4>
            <p>Operating, investing, financing cash flows, free cash flow, capex</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>🏦 Balance Sheet</h4>
            <p>Assets, liabilities, equity, debt levels, working capital</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 Live Market Data</h4>
            <p>Current price, P/E ratios, market cap, shares outstanding</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main scraping functionality
    if scrape_button and ticker_input:
        if not email or not password or email == "your_email@example.com":
            st.error("❌ Please provide valid TIKR credentials")
            return
        
        scrape_financial_data(ticker_input, include_live_data, show_debug_logs)
    
    # Show recent files
    show_recent_files()

def scrape_financial_data(ticker: str, include_live_data: bool, show_debug_logs: bool):
    """Main scraping function with Streamlit UI integration and comprehensive error handling."""
    
    # Create progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Create a log display area for real-time updates
    logs = []
    if show_debug_logs:
        log_container = st.container()
        with log_container:
            st.subheader("🔍 Debug Logs")
            log_area = st.empty()
    
    def log_message(message, level="INFO", update_ui=True):
        """Add a message to both console and UI logs."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_message = f"[{timestamp}] {level}: {message}"
        print(full_message)
        logger.info(f"{level}: {message}")
        
        logs.append(full_message)
        
        # Only update UI if we're in the main thread and show_debug_logs is True
        if show_debug_logs and update_ui:
            try:
                log_area.code("\n".join(logs[-20:]), language=None)  # Show last 20 logs
            except Exception:
                # Ignore UI update errors (likely from background threads)
                pass
    
    def update_logs_display():
        """Update the logs display - call this from main thread only."""
        if show_debug_logs and logs:
            try:
                log_area.code("\n".join(logs[-20:]), language=None)
            except Exception:
                pass
    
    try:
        # Initialize scraper
        log_message("Initializing TIKR scraper...")
        status_text.text("🔧 Initializing TIKR scraper...")
        progress_bar.progress(10)
        
        try:
            scraper = TIKRScraper(output_dir="outputs")
            log_message("✅ Scraper initialized successfully")
        except Exception as e:
            error_msg = f"Failed to initialize scraper: {str(e)}"
            log_message(error_msg, "ERROR")
            st.error(f"❌ {error_msg}")
            if show_debug_logs:
                st.code(traceback.format_exc(), language=None)
            return
        
        # Get access token
        log_message("Starting authentication process...")
        status_text.text("🔐 Authenticating with TIKR...")
        progress_bar.progress(20)
        
        # First check if we have a valid existing token
        if scraper.access_token:
            log_message("Found existing token, validating...")
            status_text.text("🔐 Validating existing token...")
            try:
                # Test the token with a simple API call
                test_trading_id, test_company_id = scraper.find_company_info("AAPL")
                if test_trading_id:
                    log_message("✅ Existing token is valid")
                else:
                    log_message("Token appears invalid, will generate new one")
                    scraper.access_token = ""
            except Exception as e:
                log_message(f"Token validation failed: {str(e)}")
                scraper.access_token = ""
        
        if not scraper.access_token:
            try:
                # Check if we're in deployment mode
                is_deployment = False
                try:
                    is_deployment = st.secrets.get("IS_DEPLOYMENT", "").lower() == "true"
                except (AttributeError, KeyError):
                    is_deployment = os.environ.get("DEPLOYMENT", "").lower() == "true"
                
                # Handle deployment mode separately
                if is_deployment:
                    log_message("Running in deployment environment - checking for pre-configured token...")
                    # Try to get token from secrets or environment variables
                    try:
                        # This will raise an exception if no token is available
                        scraper.get_access_token()
                        log_message("✅ Successfully loaded token from secrets/environment")
                    except Exception as e:
                        error_msg = f"Failed to load token in deployment mode: {str(e)}"
                        log_message(error_msg, "ERROR")
                        st.error(f"❌ {error_msg}")
                        st.info("""
                        ### Deployment Token Setup Required
                        
                        This app is running in deployment mode but no valid token was found.
                        
                        To fix this:
                        1. Run the app locally to generate a token
                        2. Copy the token from `outputs/token.tmp`
                        3. Add it to your Streamlit secrets as described in the deployment guide
                        
                        See `streamlit_deploy_guide.md` for detailed instructions.
                        """)
                        return
                else:
                    # Regular token generation with browser automation
                    log_message("Generating new authentication token...")
                    status_text.text("🔐 Generating new authentication token...")
                    st.info("🔄 This may take 1-2 minutes for first-time authentication...")
                    
                    # Add timeout for token generation using threading
                    import threading
                    import queue
                    
                    def get_token_with_timeout():
                        result_queue = queue.Queue()
                        
                        def token_worker():
                            try:
                                # Don't update UI from background thread
                                log_message("Starting browser automation for token generation...", update_ui=False)
                                scraper.get_access_token()
                                result_queue.put(("success", None))
                            except Exception as e:
                                result_queue.put(("error", e))
                        
                        thread = threading.Thread(target=token_worker)
                        thread.daemon = True
                        thread.start()
                        
                        # Wait for result with timeout
                        thread.join(timeout=120)  # 2 minute timeout
                        
                        if thread.is_alive():
                            log_message("Authentication timed out after 2 minutes", "ERROR")
                            update_logs_display()  # Update UI from main thread
                            st.error("❌ Authentication timed out. This may be due to browser issues or network problems.")
                            st.info("💡 Try running the scraper directly from command line first to generate a token.")
                            return False
                        
                        try:
                            result_type, error = result_queue.get_nowait()
                            if result_type == "error":
                                raise error
                            log_message("✅ Token generated successfully")
                            update_logs_display()  # Update UI from main thread
                            return True
                        except queue.Empty:
                            log_message("Authentication failed with unknown error", "ERROR")
                            update_logs_display()  # Update UI from main thread
                            st.error("❌ Authentication failed with unknown error.")
                            return False
                    
                    if not get_token_with_timeout():
                        return
                    
            except Exception as e:
                error_msg = f"Authentication failed: {str(e)}"
                log_message(error_msg, "ERROR")
                
                # Check if this is a deployment-related error
                if ("DEPLOYMENT MODE" in str(e) or 
                    "Chrome browser not available" in str(e) or
                    "Failed to initialize browser" in str(e)):
                    
                    st.error("🚀 **Deployment Environment Detected**")
                    st.markdown("""
                    <div style="background-color: #fff3cd; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #ffc107;">
                        <h4>🔧 Setup Required for Deployment</h4>
                        <p>This app is running in a deployment environment where Chrome browser is not available.</p>
                        <p><strong>To fix this, you need to:</strong></p>
                        <ol>
                            <li><strong>Generate a token locally:</strong>
                                <br>Run <code>python generate_token.py</code> on your local machine</li>
                            <li><strong>Set environment variables:</strong>
                                <br>Add <code>TIKR_ACCESS_TOKEN</code> and <code>DEPLOYMENT=true</code> to your deployment</li>
                            <li><strong>Use deployment requirements:</strong>
                                <br>Use <code>requirements_deployment.txt</code> instead of <code>requirements.txt</code></li>
                        </ol>
                        <p>📖 See <code>DEPLOYMENT_GUIDE.md</code> for detailed instructions.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Show specific platform instructions
                    st.markdown("### Platform-Specific Instructions:")
                    
                    tab1, tab2, tab3 = st.tabs(["Streamlit Cloud", "Heroku", "Railway"])
                    
                    with tab1:
                        st.code("""
# In your Streamlit Cloud secrets.toml:
TIKR_EMAIL = "your_email@example.com"
TIKR_PASSWORD = "your_password"
TIKR_ACCESS_TOKEN = "your_generated_token_here"
DEPLOYMENT = "true"
                        """)
                    
                    with tab2:
                        st.code("""
# Heroku config commands:
heroku config:set TIKR_EMAIL=your_email@example.com
heroku config:set TIKR_PASSWORD=your_password
heroku config:set TIKR_ACCESS_TOKEN=your_generated_token_here
heroku config:set DEPLOYMENT=true
                        """)
                    
                    with tab3:
                        st.code("""
# Railway config commands:
railway env set TIKR_EMAIL=your_email@example.com
railway env set TIKR_PASSWORD=your_password
railway env set TIKR_ACCESS_TOKEN=your_generated_token_here
railway env set DEPLOYMENT=true
                        """)
                    
                else:
                    # Regular error handling
                    st.error(f"❌ {error_msg}")
                    st.info("💡 Common issues: Chrome not installed, credentials incorrect, or network problems.")
                
                if show_debug_logs:
                    st.error(f"Debug details: {repr(e)}")
                    st.code(traceback.format_exc(), language=None)
                return
        
        log_message("✅ Authentication successful")
        
        # Find company
        log_message(f"Searching for company: {ticker}")
        status_text.text(f"🔍 Searching for {ticker}...")
        progress_bar.progress(30)
        
        try:
            trading_id, company_id = scraper.find_company_info(ticker)
            if not trading_id:
                error_msg = f"Could not find company information for {ticker}"
                log_message(error_msg, "ERROR")
                st.error(f"❌ {error_msg}")
                return
            
            log_message(f"✅ Found {ticker}: trading_id={trading_id}, company_id={company_id}")
        except Exception as e:
            error_msg = f"Error searching for {ticker}: {str(e)}"
            log_message(error_msg, "ERROR")
            st.error(f"❌ {error_msg}")
            return
        
        # Fetch financial statements
        log_message("Fetching financial statements...")
        status_text.text("📊 Fetching financial statements...")
        progress_bar.progress(50)
        
        try:
            scraper.get_financials(trading_id, company_id)
            log_message("✅ Successfully fetched all financial statements")
        except Exception as e:
            error_msg = f"Failed to fetch financial statements: {str(e)}"
            log_message(error_msg, "ERROR")
            st.error(f"❌ {error_msg}")
            if show_debug_logs:
                st.code(traceback.format_exc(), language=None)
            return
        
        # Fetch live data if requested
        live_data = None
        yfinance_data = None
        if include_live_data:
            log_message("Fetching live market data...")
            status_text.text("📈 Fetching live market data...")
            progress_bar.progress(75)
            try:
                live_data = scraper.get_live_market_data(ticker, trading_id)
                log_message("✅ Live market data fetched")
            except Exception as e:
                log_message(f"Warning: Failed to fetch live data: {str(e)}", "WARNING")
                st.warning(f"⚠️ Live market data fetch failed: {str(e)}")
            
            # Also fetch Yahoo Finance real-time data
            log_message("Fetching Yahoo Finance real-time data...")
            status_text.text("📈 Fetching Yahoo Finance real-time data...")
            progress_bar.progress(80)
            try:
                yfinance_data = scraper.get_realtime_price_yfinance(ticker)
                log_message("✅ Yahoo Finance real-time data fetched")
            except Exception as e:
                log_message(f"Warning: Failed to fetch Yahoo Finance data: {str(e)}", "WARNING")
                st.warning(f"⚠️ Yahoo Finance data fetch failed: {str(e)}")
        
        # Export to Excel
        log_message("Exporting to Excel...")
        status_text.text("🏁 Exporting to Excel...")
        progress_bar.progress(90)
        
        try:
            filename = f"{ticker}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
            result = scraper.export_to_excel(filename, live_data, yfinance_data)
            log_message(f"✅ Export completed: {result}")
        except Exception as e:
            error_msg = f"Failed to export to Excel: {str(e)}"
            log_message(error_msg, "ERROR")
            st.error(f"❌ {error_msg}")
            if show_debug_logs:
                st.code(traceback.format_exc(), language=None)
            return
        
        progress_bar.progress(100)
        status_text.text("✅ Scraping completed!")
        log_message("🎉 Scraping process completed successfully!")
        
        if result:
            # Success message
            st.markdown(f"""
            <div class="success-box">
                <h3>🎉 Successfully scraped {ticker} financial statements!</h3>
                <p><strong>📁 Output file:</strong> {result}</p>
                <p><strong>📊 Contains:</strong> Income Statement, Cash Flow, Balance Sheet{', Live Market Data' if include_live_data else ''}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Download button
            if Path(result).exists():
                with open(result, "rb") as file:
                    st.download_button(
                        label=f"📥 Download {ticker} Financial Data",
                        data=file.read(),
                        file_name=Path(result).name,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
            
            # Preview data
            preview_data(result, ticker)
            
        else:
            log_message("Export returned no result", "ERROR")
            st.markdown("""
            <div class="error-box">
                <h3>❌ Failed to scrape financial statements</h3>
                <p>Please check your credentials and try again.</p>
            </div>
            """, unsafe_allow_html=True)
    
    except Exception as e:
        error_msg = f"Unexpected error during scraping: {str(e)}"
        log_message(error_msg, "ERROR")
        st.markdown(f"""
        <div class="error-box">
            <h3>❌ Error during scraping</h3>
            <p><strong>Error:</strong> {str(e)}</p>
            <p>Please check your TIKR credentials and internet connection.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if show_debug_logs:
            st.error(f"Debug error details: {repr(e)}")
            st.code(traceback.format_exc(), language=None)
    
    finally:
        # Final update to logs display
        update_logs_display()
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()

def preview_data(filepath: str, ticker: str):
    """Preview the scraped data in the Streamlit interface."""
    
    st.subheader(f"📊 Data Preview for {ticker}")
    
    try:
        # Read Excel file
        excel_file = pd.ExcelFile(filepath)
        sheet_names = excel_file.sheet_names
        
        # Create tabs for each sheet
        tabs = st.tabs([sheet.replace('_', ' ').title() for sheet in sheet_names])
        
        for tab, sheet_name in zip(tabs, sheet_names):
            with tab:
                df = pd.read_excel(filepath, sheet_name=sheet_name)
                
                if not df.empty:
                    st.dataframe(df, use_container_width=True)
                    
                    # Show basic stats
                    st.caption(f"📈 {len(df)} rows × {len(df.columns)} columns")
                    
                    # Special handling for live market data
                    if (sheet_name in ['live_market_data', 'yahoo_finance_realtime'] and 
                        'Metric' in df.columns and 'Value' in df.columns):
                        show_market_data_visualization(df, ticker)
                else:
                    st.info("No data available for this sheet")
    
    except Exception as e:
        st.error(f"Error previewing data: {str(e)}")

def show_market_data_visualization(df: pd.DataFrame, ticker: str):
    """Create visualizations for market data."""
    
    st.subheader(f"📊 Market Metrics for {ticker}")
    
    # Create metrics display
    metrics_data = df.set_index('Metric')['Value'].to_dict()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Try Yahoo Finance current price first, then TIKR calculated price
        price = (metrics_data.get('Current Price') or 
                metrics_data.get('Current Price (Calculated)') or 'N/A')
        st.metric("Current Price", price)
    
    with col2:
        # Try both P/E ratio sources
        pe = (metrics_data.get('P/E Ratio') or 
              metrics_data.get('LTM P/E Ratio') or 'N/A')
        st.metric("P/E Ratio", pe)
    
    with col3:
        # Try EPS from different sources
        eps = (metrics_data.get('EPS (TTM)') or 
               metrics_data.get('LTM EPS') or 'N/A')
        st.metric("LTM EPS", eps)
    
    with col4:
        # Try market cap from different sources
        market_cap = (metrics_data.get('Market Cap') or 
                     metrics_data.get('Market Cap (Calculated)') or 'N/A')
        st.metric("Market Cap", market_cap)

def show_sample_data():
    """Show sample data structure."""
    
    st.subheader("📋 Sample Data Structure")
    
    # Sample data for demonstration
    sample_income = pd.DataFrame({
        'Metric': ['Revenue', 'Gross Profit', 'Operating Income', 'Net Income'],
        '2023': [394328, 169148, 114301, 96995],
        '2022': [365817, 152836, 119437, 94680],
        '2021': [294135, 152836, 108949, 94680]
    })
    
    sample_market = pd.DataFrame({
        'Metric': ['Current Price', 'P/E Ratio', 'Market Cap', 'LTM EPS'],
        'Value': ['$150.25', '25.2', '$2.4T', '$6.05']
    })
    
    tab1, tab2 = st.tabs(["Income Statement Sample", "Market Data Sample"])
    
    with tab1:
        st.dataframe(sample_income, use_container_width=True)
        st.caption("Sample income statement data (in millions)")
    
    with tab2:
        st.dataframe(sample_market, use_container_width=True)
        st.caption("Sample live market data")

def show_recent_files():
    """Show recently generated files."""
    
    st.subheader("📁 Recent Files")
    
    outputs_dir = Path("outputs")
    if outputs_dir.exists():
        excel_files = list(outputs_dir.glob("*.xlsx"))
        excel_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        if excel_files:
            for file in excel_files[:5]:  # Show last 5 files
                file_time = datetime.fromtimestamp(file.stat().st_mtime)
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.text(f"📊 {file.name}")
                
                with col2:
                    st.text(f"🕒 {file_time.strftime('%Y-%m-%d %H:%M')}")
                
                with col3:
                    if st.button("📥", key=f"download_{file.name}"):
                        with open(file, "rb") as f:
                            st.download_button(
                                label="Download",
                                data=f.read(),
                                file_name=file.name,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key=f"dl_{file.name}"
                            )
        else:
            st.info("No recent files found. Scrape some data to get started!")
    else:
        st.info("No outputs directory found. Files will appear here after scraping.")

if __name__ == "__main__":
    main() 