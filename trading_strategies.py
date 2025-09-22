import pandas as pd
import numpy as np

class TradingStrategy:
    def __init__(self, initial_capital=100000):
        self.initial_capital = initial_capital
    
    def moving_average_crossover(self, df, short_window=20, long_window=50):
        try:
            signals = pd.DataFrame(index=df.index)
            signals['price'] = df['Close']
            
            # Calculate moving averages
            signals['short_ma'] = df['Close'].rolling(window=short_window, min_periods=1).mean()
            signals['long_ma'] = df['Close'].rolling(window=long_window, min_periods=1).mean()
            
            # Generate signals
            signals['signal'] = 0
            if len(signals) > long_window:
                signals['signal'][long_window:] = np.where(
                    signals['short_ma'][long_window:] > signals['long_ma'][long_window:], 1, 0
                )
            
            return self.backtest_strategy(signals)
        except Exception as e:
            print(f"Error in moving_average_crossover: {e}")
            raise
    
    def rsi_strategy(self, df, rsi_oversold=30, rsi_overbought=70):
        try:
            signals = pd.DataFrame(index=df.index)
            signals['price'] = df['Close']
            signals['rsi'] = df['RSI']
            
            # Generate signals based on RSI
            signals['signal'] = 0
            signals['signal'] = np.where(signals['rsi'] < rsi_oversold, 1, 
                                      np.where(signals['rsi'] > rsi_overbought, -1, 0))
            
            return self.backtest_strategy(signals)
        except Exception as e:
            print(f"Error in rsi_strategy: {e}")
            raise
    
    def backtest_strategy(self, signals):
        try:
            portfolio = pd.DataFrame(index=signals.index)
            portfolio['price'] = signals['price']
            portfolio['signal'] = signals['signal']
            
            # Calculate returns
            portfolio['returns'] = portfolio['price'].pct_change().fillna(0)
            portfolio['strategy_returns'] = portfolio['signal'].shift(1).fillna(0) * portfolio['returns']
            
            # Calculate cumulative returns
            portfolio['cumulative_market'] = (1 + portfolio['returns']).cumprod()
            portfolio['cumulative_strategy'] = (1 + portfolio['strategy_returns']).cumprod()
            
            # Fill NaN values
            portfolio = portfolio.fillna(method='ffill').fillna(1)
            
            # Calculate performance metrics
            total_return = (portfolio['cumulative_strategy'].iloc[-1] - 1) * 100
            volatility = portfolio['strategy_returns'].std() * np.sqrt(252) * 100 if len(portfolio) > 1 else 0
            
            # Sharpe ratio (annualized)
            if portfolio['strategy_returns'].std() > 0 and len(portfolio) > 1:
                sharpe = portfolio['strategy_returns'].mean() / portfolio['strategy_returns'].std() * np.sqrt(252)
            else:
                sharpe = 0
            
            # Maximum drawdown
            portfolio['cumulative_max'] = portfolio['cumulative_strategy'].cummax()
            portfolio['drawdown'] = (portfolio['cumulative_strategy'] - portfolio['cumulative_max']) / portfolio['cumulative_max']
            max_drawdown = portfolio['drawdown'].min() * 100
            
            results = {
                'portfolio': portfolio,
                'metrics': {
                    'total_return': round(float(total_return), 2),
                    'volatility': round(float(volatility), 2),
                    'sharpe_ratio': round(float(sharpe), 2),
                    'max_drawdown': round(float(max_drawdown), 2),
                    'final_value': round(float(self.initial_capital * portfolio['cumulative_strategy'].iloc[-1]), 2)
                }
            }
            
            return results
            
        except Exception as e:
            print(f"Error in backtest_strategy: {e}")
            # Return default results in case of error
            return {
                'portfolio': pd.DataFrame(),
                'metrics': {
                    'total_return': 0,
                    'volatility': 0,
                    'sharpe_ratio': 0,
                    'max_drawdown': 0,
                    'final_value': self.initial_capital
                }
            }

if __name__ == "__main__":
    print("Trading strategies module ready!")
