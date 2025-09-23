import streamlit as st
import pandas as pd
from trading_strategies import run_backtest
from src.data_loader import load_stock_data


st.title("📊 Algorithmic Trading Dashboard")

# --- User Inputs ---
symbol = st.text_input("Enter Stock Symbol (e.g., RELIANCE.NS)", "RELIANCE.NS")
strategy = st.selectbox("Select Strategy", ["sma_crossover", "rsi_strategy"])
period = st.selectbox("Select Period", ["6mo", "1y", "2y"])
capital = st.number_input("Initial Capital", min_value=1000, value=100000, step=1000)

if st.button("Run Backtest"):
    st.info(f"Fetching data for {symbol}...")

    # --- Load Data ---
    df = load_stock_data(symbol, "2022-01-01", "2024-12-31")

    if df.empty:
        st.error("❌ No data available for the given stock symbol.")
    else:
        # --- Run Strategy ---
        result = run_backtest(symbol, strategy, period, capital)

        if isinstance(result, dict):
            st.subheader("📈 Backtest Results")
            st.json(result)

            if "equity" in result and isinstance(result["equity"], pd.DataFrame):
                st.line_chart(result["equity"]["equity_curve"])
        else:
            st.warning("⚠️ Backtest did not return results.")
