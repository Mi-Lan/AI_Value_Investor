#!/usr/bin/env python3
"""
TIKR Financial Scraper - Main Module Entry Point

Allows running the scraper as a module: python -m tikr_scraper [TICKER]
"""

from .tikr_scraper import main

if __name__ == "__main__":
    main() 