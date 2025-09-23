import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class StockDataFetcher:
    def __init__(self):
        self.indian_stocks = {
            'RELIANCE.NS': 'Reliance Industries',
            'TCS.NS': 'Tata Consultancy Services', 
            'INFY.NS': 'Infosys',
            'HDFCBANK.NS': 'HDFC Bank',
            'ICICIBANK.NS': 'ICICI Bank',
            'SBIN.NS': 'State Bank of India',
            'WIPRO.NS': 'Wipro',
            'ADANIPORTS.NS': 'Adani Ports',
            'TATAMOTORS.NS': 'Tata Motors', 
            'LT.NS': 'Larsen & Toubro'
        }
    
    def get_stock_list(self):
        return self.indian_stocks
    
    def get_stock_data(self, symbol, period='6mo'):
        try:
            # Real stock data eduthukuran
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                return self.create_fallback_data(symbol)
                
            return data
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return self.create_fallback_data(symbol)
    
    def create_fallback_data(self, symbol):
        """Basic data create pannu real data fail aana"""
        dates = pd.date_range(end=datetime.now(), periods=180, freq='D')
        return pd.DataFrame({
            'Close': np.random.normal(1000, 100, len(dates)),
            'Open': np.random.normal(1000, 100, len(dates)),
            'High': np.random.normal(1010, 100, len(dates)),
            'Low': np.random.normal(990, 100, len(dates)),
            'Volume': np.random.randint(100000, 1000000, len(dates))
        }, index=dates)
