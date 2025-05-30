#!/usr/bin/env python3
"""
Simple Stock Price Example - The EASIEST way to get stock prices!

This example shows how to get current stock prices using Yahoo Finance (yfinance).
No API key required, very reliable, and just a few lines of code.

Installation:
    pip install yfinance

Usage:
    python example_stock_prices.py
"""

try:
    import yfinance as yf
    import pandas as pd
except ImportError:
    print("❌ Missing required packages. Install with:")
    print("   pip install yfinance pandas")
    exit(1)


def get_simple_price(ticker):
    """Get just the current price - simplest possible way."""
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period="1d")
        if not history.empty:
            return history['Close'].iloc[-1]
        return None
    except:
        return None


def get_detailed_info(ticker):
    """Get comprehensive stock information."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        history = stock.history(period="2d")
        
        if history.empty:
            return None
            
        current_price = history['Close'].iloc[-1]
        previous_price = history['Close'].iloc[-2] if len(history) > 1 else current_price
        change = current_price - previous_price
        change_percent = (change / previous_price * 100) if previous_price != 0 else 0
        
        return {
            'current_price': current_price,
            'price_change': change,
            'change_percent': change_percent,
            'market_cap': info.get('marketCap'),
            'pe_ratio': info.get('trailingPE'),
            'company_name': info.get('longName'),
            'sector': info.get('sector')
        }
    except Exception as e:
        print(f"Error getting info for {ticker}: {e}")
        return None


def main():
    print("🚀 Simple Stock Price Example")
    print("=" * 50)
    
    # Example 1: Get just the price (simplest way)
    print("\n💰 Example 1: Just get the current price")
    print("-" * 30)
    
    tickers = ['AAPL', 'TSLA', 'MSFT', 'GOOGL']
    
    for ticker in tickers:
        price = get_simple_price(ticker)
        if price:
            print(f"{ticker}: ${price:.2f}")
        else:
            print(f"{ticker}: Failed to fetch")
    
    # Example 2: Get detailed information
    print("\n📊 Example 2: Detailed stock information")
    print("-" * 40)
    
    detailed_ticker = 'AAPL'
    info = get_detailed_info(detailed_ticker)
    
    if info:
        print(f"\n{detailed_ticker} - {info['company_name']}")
        print(f"Current Price: ${info['current_price']:.2f}")
        print(f"Price Change: ${info['price_change']:+.2f} ({info['change_percent']:+.2f}%)")
        print(f"Market Cap: ${info['market_cap']:,}" if info['market_cap'] else "Market Cap: N/A")
        print(f"P/E Ratio: {info['pe_ratio']:.2f}" if info['pe_ratio'] else "P/E Ratio: N/A")
        print(f"Sector: {info['sector']}" if info['sector'] else "Sector: N/A")
    else:
        print(f"Failed to get detailed info for {detailed_ticker}")
    
    # Example 3: Multiple stocks at once
    print("\n📈 Example 3: Multiple stocks at once")
    print("-" * 35)
    
    try:
        # Download data for multiple tickers
        data = yf.download(['AAPL', 'TSLA', 'MSFT', 'GOOGL'], period="1d")
        
        if not data.empty:
            for ticker in ['AAPL', 'TSLA', 'MSFT', 'GOOGL']:
                try:
                    price = data[ticker]['Close'].iloc[-1]
                    print(f"{ticker}: ${price:.2f}")
                except:
                    print(f"{ticker}: No data")
        else:
            print("No data retrieved for bulk download")
            
    except Exception as e:
        print(f"Error with bulk download: {e}")
    
    print("\n✅ That's it! Super easy to get stock prices with yfinance.")
    print("\n📚 Integration into your TIKR scraper:")
    print("   - Your enhanced TIKR scraper now includes both TIKR calculated prices")
    print("   - AND real-time Yahoo Finance prices for verification")
    print("   - Run: python tikr_scraper.py AAPL")
    print("   - Check the 'yahoo_finance_realtime' sheet in the output Excel file")


if __name__ == "__main__":
    main() 