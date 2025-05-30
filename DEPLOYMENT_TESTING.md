# Deployment Testing Guide for TIKR Scraper

This guide helps you test the TIKR scraper locally in deployment-like conditions to catch issues before production deployment.

## 🧪 Testing Scenarios

### 1. **Clean Virtual Environment Test** (Basic Deployment Simulation)

```bash
# Create fresh environment
cd tikr_standalone_app
python -m venv deployment_test_env
source deployment_test_env/bin/activate  # or `deployment_test_env\Scripts\activate` on Windows

# Install only production dependencies
pip install --upgrade pip
pip install -r tikr_scraper/requirements.txt

# Test the scraper
cd tikr_scraper
python tikr_scraper.py AAPL
```

### 2. **Docker Environment Test** (Container Deployment)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

# Install Chrome dependencies for headless mode
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY tikr_scraper/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY tikr_scraper/ .
COPY tikr_scraper/static/ ./static/

CMD ["python", "tikr_scraper.py", "AAPL"]
```

Test with Docker:
```bash
# Build image
docker build -t tikr-scraper .

# Run with credentials
docker run -e TIKR_EMAIL="your_email" -e TIKR_PASSWORD="your_password" \
    -v $(pwd)/outputs:/app/outputs tikr-scraper
```

### 3. **Headless Mode Test** (Server Environment)

```bash
# Force headless mode by setting environment variable
export TIKR_HEADLESS=true
python tikr_scraper.py AAPL
```

### 4. **Memory Constraints Test** (Limited Resources)

```bash
# Simulate limited memory environment
ulimit -v 2000000  # Limit virtual memory to ~2GB
python tikr_scraper.py AAPL
```

### 5. **Network Restrictions Test** (Firewall/Proxy)

```bash
# Test with proxy (if your deployment uses one)
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
python tikr_scraper.py AAPL
```

### 6. **Different Python Versions Test**

```bash
# Test with Python 3.9 (minimum supported)
pyenv install 3.9.19
pyenv virtualenv 3.9.19 tikr-py39
pyenv activate tikr-py39
pip install -r requirements.txt
python tikr_scraper.py AAPL

# Test with Python 3.11 (recommended)
pyenv install 3.11.10
pyenv virtualenv 3.11.10 tikr-py311
pyenv activate tikr-py311
pip install -r requirements.txt
python tikr_scraper.py AAPL
```

## 🔧 Common Deployment Issues & Solutions

### Issue 1: `blinker._saferef` Module Not Found
**Solution**: Add compatible blinker version to requirements.txt
```
blinker<1.8
```

### Issue 2: `pkg_resources` Module Not Found
**Solution**: Add setuptools to requirements.txt
```
setuptools>=65.5.0
```

### Issue 3: Chrome/ChromeDriver Issues in Containers
**Solution**: Use these Chrome options for containers:
```python
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--remote-debugging-port=9222")
```

### Issue 4: File Permissions in Containers
**Solution**: Set proper permissions in Dockerfile:
```dockerfile
RUN chmod -R 755 /app
RUN chown -R 1000:1000 /app
USER 1000
```

### Issue 5: Missing Static Files
**Solution**: Ensure static folder is copied:
```dockerfile
COPY tikr_scraper/static/ ./static/
```

## 🚀 Production-Ready Configuration

### Environment Variables for Deployment
```bash
# Required credentials
TIKR_EMAIL=your_email@domain.com
TIKR_PASSWORD=your_secure_password

# Optional configuration
TIKR_HEADLESS=true                    # Force headless mode
TIKR_OUTPUT_DIR=/app/outputs          # Custom output directory
TIKR_LOG_LEVEL=INFO                   # Logging level
TIKR_TIMEOUT=30                       # Request timeout seconds
```

### Recommended Deployment Structure
```
production/
├── tikr_scraper/
│   ├── tikr_scraper.py
│   ├── keys.py
│   ├── static/
│   │   └── Valuation Base.xlsx
│   └── requirements.txt
├── .env                              # Production credentials
├── Dockerfile                        # Container definition
├── docker-compose.yml               # Multi-service setup
└── outputs/                         # Output directory
```

### Health Check Script
Create `health_check.py`:
```python
#!/usr/bin/env python3
"""Health check script for TIKR scraper deployment."""

import subprocess
import sys
import os

def test_dependencies():
    """Test that all required dependencies are installed."""
    try:
        import pandas
        import requests
        import selenium
        import yfinance
        import openpyxl
        print("✅ All dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def test_chrome():
    """Test Chrome/ChromeDriver availability."""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        
        driver = webdriver.Chrome(
            ChromeDriverManager().install(), 
            options=options
        )
        driver.quit()
        print("✅ Chrome/ChromeDriver working")
        return True
    except Exception as e:
        print(f"❌ Chrome/ChromeDriver issue: {e}")
        return False

def test_credentials():
    """Test TIKR credentials availability."""
    email = os.getenv('TIKR_EMAIL')
    password = os.getenv('TIKR_PASSWORD')
    
    if not email or not password:
        print("❌ Missing TIKR credentials in environment")
        return False
    
    if email == "your_email@example.com":
        print("❌ Default credentials detected - update with real credentials")
        return False
        
    print("✅ TIKR credentials configured")
    return True

def main():
    """Run all health checks."""
    print("🔍 Running deployment health checks...")
    
    checks = [
        test_dependencies(),
        test_chrome(),
        test_credentials()
    ]
    
    if all(checks):
        print("🎉 All health checks passed - ready for deployment!")
        sys.exit(0)
    else:
        print("❌ Some health checks failed - fix issues before deployment")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

Run health check:
```bash
python health_check.py
```

## 📦 Docker Compose for Production

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  tikr-scraper:
    build: .
    environment:
      - TIKR_EMAIL=${TIKR_EMAIL}
      - TIKR_PASSWORD=${TIKR_PASSWORD}
      - TIKR_HEADLESS=true
    volumes:
      - ./outputs:/app/outputs
    restart: unless-stopped
    command: ["python", "tikr_scraper.py", "AAPL"]
    
  # Optional: Add scheduling service
  scheduler:
    image: mcuadros/ofelia:latest
    depends_on:
      - tikr-scraper
    command: daemon --docker
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    labels:
      ofelia.job-run.scraper.schedule: "0 0 2 * * *"  # Daily at 2 AM
      ofelia.job-run.scraper.container: "tikr-scraper"
```

## 🧹 Cleanup After Testing

```bash
# Deactivate virtual environment
deactivate

# Remove test environment
rm -rf deployment_test_env

# Clean Docker
docker system prune -f
```

## 📊 Performance Testing

### Load Test Script
```python
import time
import concurrent.futures
from tikr_scraper import TIKRScraper

def scrape_ticker(ticker):
    """Scrape a single ticker."""
    start_time = time.time()
    scraper = TIKRScraper()
    result = scraper.scrape_company(ticker)
    end_time = time.time()
    return ticker, result, end_time - start_time

# Test multiple tickers concurrently
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(scrape_ticker, ticker) for ticker in tickers]
    
    for future in concurrent.futures.as_completed(futures):
        ticker, result, duration = future.result()
        status = "✅ Success" if result else "❌ Failed"
        print(f"{ticker}: {status} in {duration:.2f}s")
```

This guide ensures your TIKR scraper will work reliably in production environments! 