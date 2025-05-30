# 📊 TIKR Financial Scraper - Standalone App

A modern, user-friendly financial data scraper that extracts comprehensive financial statements from [TIKR](https://app.tikr.com/) and exports them to Excel. This standalone application provides both command-line and web interfaces for scraping financial data from any publicly traded company.

## 🌟 Features

### 📈 Financial Data Extraction
- **Income Statement** - Revenue, expenses, profit/loss metrics, EBITDA, EPS
- **Cash Flow Statement** - Operating, investing, financing cash flows, free cash flow
- **Balance Sheet** - Assets, liabilities, equity, debt levels, working capital
- **Live Market Data** - Current stock price, P/E ratios, market cap, shares outstanding

### 🎯 Two Ways to Use
1. **Web Interface** - Modern Streamlit app with real-time progress tracking
2. **Command Line** - Simple CLI for automated workflows and scripting

### 💼 Professional Features
- Clean Excel export with multiple sheets
- Real-time progress tracking
- Token caching for faster subsequent runs
- Error handling and retry logic
- Detailed logging and debugging options

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.7+
- Chrome browser (for Selenium automation)
- Valid TIKR account ([sign up here](https://app.tikr.com/))

### 2. Installation

```bash
# Clone or download the standalone app
cd tikr_standalone_app

# Install dependencies automatically
python setup.py
```

### 3. Configuration

**Option A: Interactive Configuration Script (Recommended)**
```bash
python tikr_scraper/configure_credentials.py
```
This script will guide you through setting up your TIKR credentials in the `tikr_scraper/config.py` file.

**Option B: Manual Configuration**
Edit the `tikr_scraper/config.py` file and replace the placeholder values:
```python
TIKR_EMAIL = "your_actual_email@example.com"
TIKR_PASSWORD = "your_actual_password"
```

**Option C: Environment Variables**
Create a `.env` file:
```bash
# .env file
TIKR_EMAIL=your_email@example.com
TIKR_PASSWORD=your_password
```

### 4. Usage Options

#### Option A: Quick Start (Fastest) ⚡
```bash
# Single company
python run_quick_start.py AAPL

# Multiple companies
python run_quick_start.py TSLA MSFT GOOGL NVDA

# Default (AAPL)
python run_quick_start.py
```

#### Option B: Web Interface (Most User-Friendly) 🌐
```bash
# Using the convenience launcher
python run_web_app.py

# Or directly with streamlit
streamlit run web_app/app.py
```
Then open http://localhost:8501 in your browser for a beautiful web interface!

#### Option C: Command Line (Classic) 💻
```bash
# Using the convenience launcher
python run_scraper.py           # Scrapes AAPL (default)
python run_scraper.py TSLA      # Tesla
python run_scraper.py MSFT      # Microsoft  
python run_scraper.py GOOGL     # Google
python run_scraper.py NVDA      # NVIDIA

# Or directly with the module
python -m tikr_scraper AAPL
```

#### Option D: Automated Demo 🎮
```bash
python run_demo.py
```
Runs automatically without prompts - perfect for testing!

#### Option E: Programmatic Usage 🐍
```python
from tikr_scraper import TIKRScraper

# Initialize scraper
scraper = TIKRScraper(output_dir="my_outputs")

# Scrape financial statements
result = scraper.scrape_company("AAPL", include_live_data=True)

if result:
    print(f"✅ Success! Output: {result}")
else:
    print("❌ Scraping failed")
```

## 📊 Output Format

The scraper exports data to Excel files with the following structure:

```
AAPL_2025-01-25.xlsx
├── income_statement      # Revenue, expenses, profit metrics
├── cashflow_statement    # Operating, investing, financing flows  
├── balancesheet_statement # Assets, liabilities, equity
└── live_market_data      # Current price, P/E, market cap
```

### Sample Data Structure

**Income Statement:**
| Metric | 2023 | 2022 | 2021 |
|--------|------|------|------|
| Revenue | 394,328 | 365,817 | 294,135 |
| Gross Profit | 169,148 | 152,836 | 152,836 |
| Operating Income | 114,301 | 119,437 | 108,949 |
| Net Income | 96,995 | 94,680 | 94,680 |

**Live Market Data:**
| Metric | Value |
|--------|-------|
| Current Price | $150.25 |
| LTM P/E Ratio | 25.2 |
| Market Cap | $2.4T |
| LTM EPS | $6.05 |

## 🖥️ Web Interface Features

The Streamlit web app provides:

### 🎨 Modern UI
- Beautiful, responsive design
- Real-time progress tracking
- Interactive data preview
- One-click Excel downloads

### 📋 Key Features
- **Credential Management** - Secure input in sidebar
- **Live Progress** - Visual progress bar and status updates
- **Data Preview** - Interactive tables with all scraped data
- **Recent Files** - Access to previously scraped files
- **Sample Data** - Preview expected output format
- **Error Handling** - Clear error messages and troubleshooting tips

### 🎯 Usage Flow
1. Enter TIKR credentials in sidebar (or configure them in config.py)
2. Type stock ticker (e.g., AAPL, TSLA)
3. Click "Scrape Financial Data"
4. Watch real-time progress
5. Preview data and download Excel file

## 🔧 Configuration Options

### Credential Sources (in order of priority)
1. **config.py file** (recommended)
2. **.env file**
3. **Environment variables**
4. **Demo credentials** (fallback)

### Configuration Files

**tikr_scraper/config.py:**
```python
TIKR_EMAIL = "your_email@example.com"
TIKR_PASSWORD = "your_password"
DEFAULT_OUTPUT_DIR = "outputs"
DEBUG_MODE = False
SHOW_BROWSER = False  # Set to True to see browser during scraping
```

**Environment Variables:**
```bash
TIKR_EMAIL=your_email@example.com          # Required
TIKR_PASSWORD=your_password                # Required
```

### Scraper Parameters
```python
scraper = TIKRScraper(
    output_dir="outputs"  # Directory for Excel files and token cache
)

# Scraping options
result = scraper.scrape_company(
    ticker="AAPL",              # Stock ticker symbol
    include_live_data=True      # Include current market metrics
)
```

## 📁 Project Structure

The project is organized into two main components:

```
tikr_standalone_app/
├── tikr_scraper/              # Core scraper package
│   ├── __init__.py           # Package initialization
│   ├── tikr_scraper.py       # Main scraper logic
│   ├── keys.py               # Data field mappings
│   ├── config.py             # Configuration settings
│   ├── configure_credentials.py  # Credential setup script
│   ├── demo.py               # Demo examples
│   ├── quick_start.py        # Quick start script
│   └── requirements.txt      # Scraper dependencies
├── web_app/                   # Streamlit web interface
│   ├── __init__.py           # Package initialization
│   ├── app.py                # Main web application
│   ├── run_web_app.py        # Web app launcher
│   └── requirements.txt      # Web app dependencies
├── run_scraper.py            # Convenience launcher for scraper
├── run_web_app.py            # Convenience launcher for web app
├── run_demo.py               # Convenience launcher for demo
├── run_quick_start.py        # Convenience launcher for quick start
├── setup.py                  # Installation script
├── requirements.txt          # Combined dependencies
└── README.md                 # This file
```

### Component Separation
- **tikr_scraper/**: Contains all the core scraping logic, independent of any UI
- **web_app/**: Contains the Streamlit web interface that uses the scraper
- **Root level**: Convenience scripts for easy access to all functionality

## ⚙️ How It Works

### 1. Authentication Flow
- Uses Selenium to automate TIKR login
- Extracts API access token from network requests
- Caches token for faster subsequent runs

### 2. Data Extraction
- Searches for company by ticker symbol
- Fetches financial statements via TIKR's API
- Processes and structures raw financial data
- Calculates derived metrics (free cash flow, ratios)

### 3. Live Market Data
- Extracts P/E ratio and EPS from latest financial data
- Calculates current stock price (P/E × EPS)
- Computes market capitalization
- Provides comprehensive market metrics

### 4. Export Process
- Structures data into clean DataFrames
- Exports to Excel with multiple sheets
- Applies professional formatting
- Generates timestamped filenames

## 🛠️ Troubleshooting

### Common Issues

**1. Credential Configuration**
```bash
# Use the configuration script
python configure_credentials.py

# Or manually edit config.py file
```

**2. Import Errors**
```bash
# Ensure you're in the correct directory
cd tikr_standalone_app
pip install -r requirements.txt
```

**3. Chrome Driver Issues**
- Ensure Chrome browser is installed
- The scraper auto-downloads ChromeDriver
- On macOS: `brew install google-chrome`
- On Ubuntu: `sudo apt-get install google-chrome-stable`

**4. Company Not Found**
- Verify ticker symbol is correct (1-5 letters only)
- Some companies may not be in TIKR's database
- Try alternative ticker symbols

**5. Access Token Errors**
- Delete `outputs/token.tmp` to force re-authentication
- Verify TIKR account is active
- Ensure no 2FA is enabled (not supported)

### Debug Mode

Enable detailed logging in `config.py`:
```python
DEBUG_MODE = True
SHOW_BROWSER = True  # Shows browser during scraping
```

## 📈 Data Quality & Coverage

### ✅ Strengths
- **High Accuracy** - Data sourced from TIKR's curated database
- **Standardization** - Consistent format across all companies
- **Historical Depth** - Typically 10+ years of data
- **Professional Quality** - Ready for financial analysis

### ⚠️ Limitations
- **TIKR Account Required** - Free accounts have limitations
- **Coverage Varies** - Some metrics may not be available for all companies
- **Rate Limits** - Built-in delays to respect TIKR servers
- **US Focus** - Primarily US-listed companies

### 💡 Best Practices
- Use paid TIKR account for full historical data
- Verify critical data points with official filings
- Respect rate limits and fair usage policies
- Cache tokens to minimize login requests

## 🤝 Contributing

This implementation is adapted from the original [TIKR Statements Scraper](https://github.com/membaby/tikr-statements-scraper) with significant enhancements:

- ✅ Modern Streamlit web interface
- ✅ Improved error handling and logging
- ✅ Live market data calculation
- ✅ Professional Excel formatting
- ✅ Token caching and management
- ✅ Multiple credential storage options
- ✅ Comprehensive documentation

## 📄 License

This project is for educational and research purposes. Please ensure compliance with TIKR's Terms of Service and respect their rate limits.

## 🆘 Support

If you encounter issues:

1. **Check Prerequisites** - Python 3.7+, Chrome browser, valid TIKR account
2. **Configure Credentials** - Run `python configure_credentials.py`
3. **Review Logs** - Enable debug mode for detailed error information
4. **Test Network** - Ensure stable internet connection
5. **Try Again** - Some issues are temporary (server load, network hiccups)

---

## 🎉 Example Usage

### Credential Setup
```bash
# Quick credential configuration
python configure_credentials.py

# Follow the prompts to enter your TIKR email and password
```

### Web Interface
```bash
streamlit run app.py
# Opens beautiful web interface at http://localhost:8501
```

### Command Line
```bash
python tikr_scraper.py NVDA
# Outputs: NVDA_2025-01-25.xlsx with complete financial statements
```

### Python Script
```python
from tikr_scraper import TIKRScraper

# Scrape multiple companies
companies = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
scraper = TIKRScraper()

for ticker in companies:
    print(f"Scraping {ticker}...")
    result = scraper.scrape_company(ticker)
    if result:
        print(f"✅ {ticker} completed: {result}")
    else:
        print(f"❌ {ticker} failed")
```

Ready to extract professional-grade financial data! 🚀📊 