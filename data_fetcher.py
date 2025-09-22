import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class StockDataFetcher:
    def __init__(self):
        self.indian_stocks = {
            'RELIANCE': 'Reliance Industries',
            'TCS': 'Tata Consultancy Services', 
            'INFY': 'Infosys',
            'HDFCBANK': 'HDFC Bank',
            'ICICIBANK': 'ICICI Bank',
            'SBIN': 'State Bank of India',
            'WIPRO': 'Wipro',
            'ADANIPORTS': 'Adani Ports',
            'TATAMOTORS': 'Tata Motors',
            'LT': 'Larsen & Toubro'
        }
    
    def get_stock_list(self):
        return self.indian_stocks
    
    def get_stock_data(self, symbol, period='6mo'):
        # Create realistic mock data that looks like real stock data
        return self.create_realistic_mock_data(symbol)
    
    def create_realistic_mock_data(self, symbol):
        """Create realistic mock data that mimics real stock behavior"""
        # Generate dates for the last 6 months
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Remove weekends (no trading)
        dates = dates[dates.dayofweek < 5]
        
        # Create realistic price movement based on symbol hash for consistency
        np.random.seed(hash(symbol) % 10000)
        
        # Start with a realistic base price for Indian stocks
        base_price = 1500 + (hash(symbol) % 3500)
        
        # Generate realistic stock returns (volatility around 1-2% daily)
        daily_returns = np.random.normal(0.001, 0.015, len(dates))  # 0.1% mean, 1.5% std
        prices = base_price * (1 + np.cumsum(daily_returns))
        
        # Ensure prices don't go negative and have some trend
        prices = np.maximum(prices, base_price * 0.7)  # Max 30% drop
        prices = prices * (1 + np.arange(len(dates)) * 0.0001)  # Slight upward trend
        
        # Create OHLC data
        df = pd.DataFrame({
            'Open': prices * (1 + np.random.normal(0, 0.002, len(dates))),
            'High': prices * (1 + np.abs(np.random.normal(0.01, 0.005, len(dates)))),
            'Low': prices * (1 - np.abs(np.random.normal(0.008, 0.004, len(dates)))),
            'Close': prices,
            'Volume': np.random.randint(1000000, 5000000, len(dates))
        }, index=dates)
        
        return self.calculate_technical_indicators(df)
    
    def calculate_technical_indicators(self, df):
        # Simple Moving Averages
        df['SMA_20'] = df['Close'].rolling(window=20, min_periods=1).mean()
        df['SMA_50'] = df['Close'].rolling(window=50, min_periods=1).mean()
        
        # RSI Calculation - FIXED: Ensure it always works
        df['RSI'] = self.calculate_rsi(df['Close'])
        
        # Remove any remaining NaN values
        df = df.fillna(method='bfill').fillna(method='ffill')
        
        # Ensure RSI has reasonable values
        df['RSI'] = df['RSI'].clip(0, 100)  # Keep between 0-100
        
        print(f"✅ Technical indicators calculated: SMA_20, SMA_50, RSI")
        print(f"📊 RSI range: {df['RSI'].min():.1f} - {df['RSI'].max():.1f}")
        
        return df
    
    def calculate_rsi(self, prices, window=14):
        """Calculate Relative Strength Index - FIXED version"""
        try:
            delta = prices.diff()
            
            gain = (delta.where(delta > 0, 0)).rolling(window=window, min_periods=1).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window, min_periods=1).mean()
            
            # Avoid division by zero
            loss = loss.replace(0, 0.001)  # Small value instead of infinity
            rs = gain / loss
            
            rsi = 100 - (100 / (1 + rs))
            return rsi.fillna(50)  # Neutral RSI when not enough data
        except Exception as e:
            print(f"⚠️ RSI calculation error, using default values: {e}")
            return pd.Series([50] * len(prices), index=prices.index)  # Default RSI

# Test the data fetcher
if __name__ == "__main__":
    fetcher = StockDataFetcher()
    print("Testing data fetcher with RSI...")
    data = fetcher.get_stock_data('RELIANCE', '3mo')
    print(f"Data columns: {list(data.columns)}")
    print(f"RSI data sample: {data['RSI'].head()}")
