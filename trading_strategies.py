import pandas as pd
import numpy as np
from data_fetcher import StockDataFetcher

class TradingStrategy:
    @staticmethod
    def ensure_datetime_index(df):
        """Make sure index is datetime"""
        if not isinstance(df.index, pd.DatetimeIndex):
            df = df.copy()
            df.index = pd.to_datetime(df.index)
        return df

    @staticmethod
    def sma_crossover_strategy(df, short_window=20, long_window=50):
        df = TradingStrategy.ensure_datetime_index(df)
        if df.empty or len(df) < long_window:
            return df
            
        df = df.copy()
        df['SMA_short'] = df['Close'].rolling(window=short_window).mean()
        df['SMA_long'] = df['Close'].rolling(window=long_window).mean()
        
        # Fix: Use .iloc for positional indexing
        df['Signal'] = 0
        if len(df) > short_window:
            # Correct way to assign values
            for i in range(short_window, len(df)):
                if df['SMA_short'].iloc[i] > df['SMA_long'].iloc[i]:
                    df.iloc[i, df.columns.get_loc('Signal')] = 1
                else:
                    df.iloc[i, df.columns.get_loc('Signal')] = 0
        
        df['Position'] = df['Signal'].diff()
        return df

    @staticmethod
    def run_backtest(symbol, strategy_func, period="3mo", capital=100000):
        # Use data_fetcher instead of src.data_loader
        fetcher = StockDataFetcher()
        df = fetcher.get_stock_data(symbol, period)
        
        if df is None or df.empty:
            return {
                "total_return": 0, 
                "sharpe_ratio": 0, 
                "max_drawdown": 0,
                "final_value": capital, 
                "message": "No data available"
            }

        df = TradingStrategy.ensure_datetime_index(df)

        if len(df) < 50:  # Need enough data for moving averages
            return {
                "total_return": 0, 
                "sharpe_ratio": 0, 
                "max_drawdown": 0,
                "final_value": capital,
                "message": "Insufficient data"
            }

        # Apply the strategy
        df = strategy_func(df)

        # Calculate returns
        df['Returns'] = df['Close'].pct_change().fillna(0)
        df['Equity'] = capital * (1 + df['Returns']).cumprod()

        total_return = (df['Equity'].iloc[-1] - capital) / capital * 100
        
        # Calculate max drawdown
        df['Peak'] = df['Equity'].cummax()
        df['Drawdown'] = (df['Peak'] - df['Equity']) / df['Peak'] * 100
        max_drawdown = df['Drawdown'].max()
        
        return {
            "total_return": round(total_return, 2),
            "sharpe_ratio": round(total_return / (df['Returns'].std() * np.sqrt(252)), 2) if df['Returns'].std() > 0 else 0,
            "max_drawdown": round(max_drawdown, 2),
            "final_value": round(df['Equity'].iloc[-1], 2),
            "message": "Success"
        }

# Simple function version
def sma_crossover_strategy(df, short_window=20, long_window=50):
    return TradingStrategy.sma_crossover_strategy(df, short_window, long_window)

def run_backtest(symbol, strategy_func, period="3mo", capital=100000):
    return TradingStrategy.run_backtest(symbol, strategy_func, period, capital)
