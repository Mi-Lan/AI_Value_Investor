#!/usr/bin/env python3
"""
TIKR Financial Scraper - Quick Start

A simple script that runs the TIKR scraper immediately without any prompts.
Perfect for automated workflows and quick data extraction.

Usage:
    python quick_start.py              # Scrapes AAPL
    python quick_start.py TSLA         # Scrapes Tesla
    python quick_start.py MSFT GOOGL   # Scrapes multiple companies
"""

import sys
from pathlib import Path
from .tikr_scraper import TIKRScraper

def quick_scrape(tickers):
    """Quick scrape function with no prompts."""
    
    print("🚀 TIKR Quick Start - Automated Scraping")
    print("=" * 50)
    
    if isinstance(tickers, str):
        tickers = [tickers]
    
    try:
        # Initialize scraper
        scraper = TIKRScraper(output_dir="outputs")
        print(f"✅ Scraper initialized for {len(tickers)} ticker(s)")
        
        results = []
        
        for i, ticker in enumerate(tickers, 1):
            print(f"\n[{i}/{len(tickers)}] 📊 Scraping {ticker}...")
            
            result = scraper.scrape_company(ticker, include_live_data=True)
            
            if result:
                results.append(result)
                filename = Path(result).name
                print(f"✅ {ticker} completed: {filename}")
            else:
                print(f"❌ {ticker} failed")
        
        # Summary
        print("\n" + "=" * 50)
        print("📋 SCRAPING SUMMARY")
        print("=" * 50)
        
        if results:
            print(f"✅ Successfully scraped {len(results)}/{len(tickers)} companies")
            print("\n📁 Output files:")
            for result in results:
                print(f"   • {Path(result).name}")
            print(f"\n💾 Files saved to: {Path('outputs').absolute()}")
        else:
            print("❌ No companies were successfully scraped")
            
        return results
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔧 Quick fixes:")
        print("1. Ensure config.py has your TIKR credentials")
        print("2. Run: python configure_credentials.py")
        print("3. Check internet connection")
        return []

def main():
    """Main function."""
    
    # Get tickers from command line or use default
    if len(sys.argv) > 1:
        tickers = [ticker.upper() for ticker in sys.argv[1:]]
    else:
        tickers = ["AAPL"]
    
    # Validate tickers
    valid_tickers = []
    for ticker in tickers:
        if ticker.isalpha() and len(ticker) <= 5:
            valid_tickers.append(ticker)
        else:
            print(f"⚠️  Skipping invalid ticker: {ticker}")
    
    if not valid_tickers:
        print("❌ No valid tickers provided")
        print("Usage: python quick_start.py AAPL TSLA MSFT")
        sys.exit(1)
    
    # Run scraping
    results = quick_scrape(valid_tickers)
    
    if results:
        print(f"\n🎉 Quick start completed! {len(results)} file(s) generated.")
    else:
        print("\n❌ Quick start failed.")
        sys.exit(1)

if __name__ == "__main__":
    main() 