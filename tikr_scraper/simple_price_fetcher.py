"""
Simple Stock Price Fetcher using Yahoo Finance (yfinance)

This is the EASIEST way to get current stock prices with a free API.
No API key required, very reliable, and just a few lines of code.

Installation:
    pip install yfinance

Usage:
    from simple_price_fetcher import get_current_price, get_stock_info
    
    # Just get the current price
    price = get_current_price('AAPL')
    print(f"AAPL: ${price}")
    
    # Get comprehensive stock info
    info = get_stock_info('AAPL')
    print(f"Price: ${info['current_price']}")
    print(f"Market Cap: ${info['market_cap']:,.0f}")
"""

import yfinance as yf
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


def get_current_price(ticker: str) -> Optional[float]:
    """
    Get the current stock price for a ticker.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA')
        
    Returns:
        Current price as float, or None if failed
        
    Example:
        >>> price = get_current_price('AAPL')
        >>> print(f"AAPL: ${price:.2f}")
    """
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period="1d")
        
        if not history.empty:
            current_price = history['Close'].iloc[-1]
            return float(current_price)
        else:
            logger.warning(f"No price data found for {ticker}")
            return None
            
    except Exception as e:
        logger.error(f"Error fetching price for {ticker}: {e}")
        return None


def get_stock_info(ticker: str) -> Dict[str, Any]:
    """
    Get comprehensive stock information including price, market cap, etc.
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        Dictionary with stock information
        
    Example:
        >>> info = get_stock_info('AAPL')
        >>> print(f"Price: ${info['current_price']:.2f}")
        >>> print(f"Market Cap: ${info['market_cap']:,}")
    """
    try:
        stock = yf.Ticker(ticker)
        
        # Get current price from recent data
        history = stock.history(period="5d")
        current_price = None
        if not history.empty:
            current_price = float(history['Close'].iloc[-1])
        
        # Get additional info from stock.info
        info = stock.info
        
        # Compile results
        stock_data = {
            'ticker': ticker.upper(),
            'current_price': current_price,
            'market_cap': info.get('marketCap'),
            'shares_outstanding': info.get('sharesOutstanding'),
            'pe_ratio': info.get('trailingPE'),
            'forward_pe': info.get('forwardPE'),
            'eps': info.get('trailingEps'),
            'beta': info.get('beta'),
            '52_week_high': info.get('fiftyTwoWeekHigh'),
            '52_week_low': info.get('fiftyTwoWeekLow'),
            'volume': info.get('volume'),
            'avg_volume': info.get('averageVolume'),
            'dividend_yield': info.get('dividendYield'),
            'company_name': info.get('longName'),
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'currency': info.get('currency', 'USD'),
            'exchange': info.get('exchange'),
            'source': 'Yahoo Finance (yfinance)'
        }
        
        logger.info(f"Successfully fetched data for {ticker}: ${current_price:.2f}")
        return stock_data
        
    except Exception as e:
        logger.error(f"Error fetching stock info for {ticker}: {e}")
        return {
            'ticker': ticker.upper(),
            'current_price': None,
            'error': str(e),
            'source': 'Yahoo Finance (yfinance)'
        }


def get_multiple_prices(tickers: list) -> Dict[str, float]:
    """
    Get current prices for multiple tickers at once.
    
    Args:
        tickers: List of ticker symbols
        
    Returns:
        Dictionary mapping ticker to price
        
    Example:
        >>> prices = get_multiple_prices(['AAPL', 'TSLA', 'MSFT'])
        >>> for ticker, price in prices.items():
        ...     print(f"{ticker}: ${price:.2f}")
    """
    prices = {}
    
    try:
        # Use yfinance to download data for multiple tickers
        tickers_str = ' '.join(tickers)
        data = yf.download(tickers_str, period="1d", interval="1d", group_by='ticker')
        
        for ticker in tickers:
            try:
                if len(tickers) == 1:
                    # Single ticker case
                    price = data['Close'].iloc[-1]
                else:
                    # Multiple tickers case
                    price = data[ticker]['Close'].iloc[-1]
                    
                prices[ticker.upper()] = float(price)
                
            except (KeyError, IndexError) as e:
                logger.warning(f"Could not get price for {ticker}: {e}")
                prices[ticker.upper()] = None
                
    except Exception as e:
        logger.error(f"Error fetching multiple prices: {e}")
        # Fallback to individual requests
        for ticker in tickers:
            prices[ticker.upper()] = get_current_price(ticker)
    
    return prices


# Quick test function
def test_price_fetcher():
    """Test the price fetcher with common stocks."""
    print("🧪 Testing Yahoo Finance Price Fetcher")
    print("=" * 50)
    
    test_tickers = ['AAPL', 'TSLA', 'MSFT', 'GOOGL']
    
    print("\n📊 Individual Price Requests:")
    for ticker in test_tickers:
        price = get_current_price(ticker)
        if price:
            print(f"  {ticker}: ${price:.2f}")
        else:
            print(f"  {ticker}: Failed to fetch")
    
    print("\n📈 Bulk Price Request:")
    prices = get_multiple_prices(test_tickers)
    for ticker, price in prices.items():
        if price:
            print(f"  {ticker}: ${price:.2f}")
        else:
            print(f"  {ticker}: Failed to fetch")
    
    print("\n📋 Detailed Stock Info (AAPL):")
    info = get_stock_info('AAPL')
    if info.get('current_price'):
        print(f"  Company: {info.get('company_name', 'N/A')}")
        print(f"  Price: ${info['current_price']:.2f}")
        print(f"  Market Cap: ${info.get('market_cap', 0):,}")
        print(f"  P/E Ratio: {info.get('pe_ratio', 'N/A')}")
        print(f"  Beta: {info.get('beta', 'N/A')}")
        print(f"  52W High: ${info.get('52_week_high', 0):.2f}")
        print(f"  52W Low: ${info.get('52_week_low', 0):.2f}")
    else:
        print(f"  Failed to fetch detailed info: {info.get('error', 'Unknown error')}")


if __name__ == "__main__":
    test_price_fetcher() 