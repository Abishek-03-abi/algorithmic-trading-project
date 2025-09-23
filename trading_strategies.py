import pandas as pd
import numpy as np

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
        if df.empty:
            return pd.DataFrame()
        df['SMA_short'] = df['Close'].rolling(short_window).mean()
        df['SMA_long'] = df['Close'].rolling(long_window).mean()
        df['Signal'] = 0
        df.loc[short_window:, 'Signal'] = np.where(
            df['SMA_short'][short_window:] > df['SMA_long'][short_window:], 1, 0
        )
        df['Position'] = df['Signal'].diff()
        return df

    @staticmethod
    def run_backtest(symbol, strategy, period="1y", capital=100000):
        from src.data_loader import load_stock_data
        import datetime

        end = datetime.date.today()
        start = end - pd.DateOffset(years=1)

        df = load_stock_data(symbol, str(start.date()), str(end.date()))
        df = TradingStrategy.ensure_datetime_index(df)

        if df.empty:
            return {"total_return":0, "sharpe_ratio":0, "max_drawdown":0,
                    "final_value":capital, "equity":df}

        df = strategy(df)

        # Equity curve based on Close prices
        df['Equity'] = capital * (1 + df['Close'].pct_change().fillna(0)).cumprod()

        total_return = (df['Equity'].iloc[-1] - capital) / capital * 100
        return {
            "total_return": total_return,
            "final_value": df['Equity'].iloc[-1],
            "equity": df
        }

# Keep the original functions for backward compatibility
def ensure_datetime_index(df):
    return TradingStrategy.ensure_datetime_index(df)

def sma_crossover_strategy(df, short_window=20, long_window=50):
    return TradingStrategy.sma_crossover_strategy(df, short_window, long_window)

def run_backtest(symbol, strategy, period="1y", capital=100000):
    return TradingStrategy.run_backtest(symbol, strategy, period, capital)
