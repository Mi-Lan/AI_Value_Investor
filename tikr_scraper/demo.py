#!/usr/bin/env python3
"""
TIKR Scraper Demo Script

This script demonstrates how to use the TIKR scraper programmatically.
It shows both single company scraping and batch processing of multiple companies.
All demos run automatically without user prompts.
"""

import os
import sys
from pathlib import Path
from .tikr_scraper import TIKRScraper

def demo_single_company():
    """Demo scraping a single company."""
    print("🍎 TIKR Scraper - Single Company Demo")
    print("=" * 50)
    
    try:
        # Initialize scraper
        scraper = TIKRScraper(output_dir="demo_outputs")
        print("✅ Scraper initialized successfully")
        
        # Scrape Apple as example
        ticker = "AAPL"
        print(f"\n🚀 Scraping {ticker}...")
        print("   (This may take a few minutes)")
        
        result = scraper.scrape_company(ticker, include_live_data=True)
        
        if result:
            print(f"\n✅ Successfully scraped {ticker}!")
            print(f"📊 Output file: {result}")
            print(f"📁 Full path: {Path(result).absolute()}")
            print("\n📋 The Excel file contains:")
            print("   • Income Statement")
            print("   • Cash Flow Statement") 
            print("   • Balance Sheet")
            print("   • Live Market Data")
        else:
            print(f"\n❌ Failed to scrape {ticker}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔧 Make sure you have:")
        print("1. Valid TIKR credentials in config.py file")
        print("2. Chrome browser installed")
        print("3. Stable internet connection")

def demo_multiple_companies():
    """Demo scraping multiple companies."""
    print("\n" + "="*50)
    print("📊 TIKR Scraper - Multiple Companies Demo")
    print("=" * 50)
    
    # List of popular tech stocks
    companies = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    
    try:
        scraper = TIKRScraper(output_dir="demo_outputs")
        print(f"✅ Scraper initialized for {len(companies)} companies")
        
        results = {}
        
        for i, ticker in enumerate(companies, 1):
            print(f"\n[{i}/{len(companies)}] 🚀 Scraping {ticker}...")
            
            result = scraper.scrape_company(ticker, include_live_data=True)
            results[ticker] = result
            
            if result:
                print(f"✅ {ticker} completed: {Path(result).name}")
            else:
                print(f"❌ {ticker} failed")
        
        # Summary
        print("\n" + "="*50)
        print("📋 BATCH SCRAPING SUMMARY")
        print("="*50)
        
        successful = [ticker for ticker, result in results.items() if result]
        failed = [ticker for ticker, result in results.items() if not result]
        
        print(f"✅ Successful: {len(successful)}/{len(companies)}")
        if successful:
            print(f"   {', '.join(successful)}")
        
        if failed:
            print(f"❌ Failed: {len(failed)}")
            print(f"   {', '.join(failed)}")
        
        print(f"\n📁 All files saved to: {Path('demo_outputs').absolute()}")
        
    except Exception as e:
        print(f"\n❌ Batch processing error: {e}")

def demo_programmatic_usage():
    """Show programmatic usage examples."""
    print("\n" + "="*50)
    print("💻 TIKR Scraper - Programmatic Usage Examples")
    print("=" * 50)
    
    print("""
# Basic usage
from tikr_scraper import TIKRScraper

# Initialize with custom output directory
scraper = TIKRScraper(output_dir="my_financial_data")

# Scrape a single company
result = scraper.scrape_company("NVDA", include_live_data=True)

# Check results
if result:
    print(f"Success! Data saved to: {result}")
else:
    print("Scraping failed")

# Batch processing with error handling
companies = ["AAPL", "MSFT", "GOOGL", "META", "NFLX"]
successful_scrapes = []

for ticker in companies:
    try:
        result = scraper.scrape_company(ticker)
        if result:
            successful_scrapes.append((ticker, result))
            print(f"✅ {ticker}: {result}")
        else:
            print(f"❌ {ticker}: Failed")
    except Exception as e:
        print(f"❌ {ticker}: Error - {e}")

print(f"Successfully scraped {len(successful_scrapes)} companies")
""")

def check_credentials():
    """Check if credentials are properly configured."""
    try:
        from . import config
        if hasattr(config, 'TIKR_EMAIL') and hasattr(config, 'TIKR_PASSWORD'):
            email = config.TIKR_EMAIL
            if email and email != "your_email@example.com":
                print(f"✅ Credentials found in config.py: {email}")
                return True
    except ImportError:
        pass
    
    # Check environment variables as fallback
    if os.getenv('TIKR_EMAIL') and os.getenv('TIKR_PASSWORD'):
        print("✅ Credentials found in environment variables")
        return True
    
    print("❌ No credentials found!")
    print("Please configure your credentials:")
    print("1. Run: python configure_credentials.py")
    print("2. Or edit config.py manually")
    print("3. Or create a .env file with TIKR_EMAIL and TIKR_PASSWORD")
    return False

def main():
    """Main demo function - runs all demos automatically."""
    print("🍎 TIKR Financial Scraper - Automated Demo")
    print("=" * 60)
    print("This demo runs automatically without prompts.")
    print("Credentials are loaded from config.py or environment variables.")
    print("=" * 60)
    
    # Check for credentials
    if not check_credentials():
        print("\n❌ Demo cancelled due to missing credentials")
        sys.exit(1)
    
    # Create outputs directory
    Path("demo_outputs").mkdir(exist_ok=True)
    
    # Run all demos automatically
    print("\n🚀 Running all demo scenarios...")
    
    # Demo 1: Single company
    demo_single_company()
    
    # Demo 2: Multiple companies (commented out by default to save time)
    print("\n" + "="*60)
    print("📝 Multiple companies demo available but skipped for time")
    print("   Uncomment demo_multiple_companies() call to enable")
    print("   This would scrape: AAPL, MSFT, GOOGL, AMZN, TSLA")
    # demo_multiple_companies()
    
    # Demo 3: Show code examples
    demo_programmatic_usage()
    
    print("\n🎉 Demo completed!")
    print("=" * 60)
    print("📁 Check the 'demo_outputs' directory for generated Excel files")
    print("🌐 To use the web interface, run: streamlit run app.py")
    print("💻 To scrape other companies, run: python tikr_scraper.py [TICKER]")

if __name__ == "__main__":
    main() 