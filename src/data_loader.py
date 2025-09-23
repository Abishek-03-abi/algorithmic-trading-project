import pandas as pd
import yfinance as yf
from nsepython import equity_history
from datetime import datetime, timedelta


def load_stock_data(symbol: str, start: str, end: str) -> pd.DataFrame:
    """
    Load stock data for given symbol using yfinance (fallback: NSEpython).
    Returns DataFrame with [Open, High, Low, Close, Volume].
    """
    # Try yfinance
    try:
        df = yf.download(symbol, start=start, end=end, interval="1d")
        if not df.empty:
            return df[["Open", "High", "Low", "Close", "Volume"]]
    except Exception as e:
        print(f"⚠️ yfinance failed for {symbol}: {e}")

    # Fallback: NSEpython (for NSE only)
    try:
        df = equity_history(
            symbol.replace(".NS", ""), "EQ",
            pd.to_datetime(start).strftime("%d-%m-%Y"),
            pd.to_datetime(end).strftime("%d-%m-%Y")
        )
        if not df.empty:
            df = df.rename(
                columns={
                    "CH_OPENING_PRICE": "Open",
                    "CH_TRADE_HIGH_PRICE": "High",
                    "CH_TRADE_LOW_PRICE": "Low",
                    "CH_CLOSING_PRICE": "Close",
                    "CH_TOT_TRADED_QTY": "Volume"
                }
            )
            df.index = pd.to_datetime(df["CH_TIMESTAMP"])
            return df[["Open", "High", "Low", "Close", "Volume"]]
    except Exception as e:
        print(f"❌ NSEpython failed for {symbol}: {e}")

    return pd.DataFrame()


def load_yfinance_multi(tickers, start: str, end: str) -> dict:
    """
    Load multiple tickers and return dict of DataFrames.
    """
    data_dict = {}
    for ticker in tickers:
        df = load_stock_data(ticker, start, end)
        data_dict[ticker] = df
    return data_dict


def pivot_to_panel(data_dict: dict) -> pd.DataFrame:
    """
    Convert dict of DataFrames into one panel-style DataFrame.
    """
    all_data = []
    for ticker, df in data_dict.items():
        if not df.empty:
            temp = df.copy()
            temp["Ticker"] = ticker
            all_data.append(temp)

    if all_data:
        return pd.concat(all_data)
    return pd.DataFrame()
