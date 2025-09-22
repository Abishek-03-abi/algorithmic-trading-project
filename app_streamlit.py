import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="Nubra Trading Dashboard", layout="wide")
st.title("📊 Nubra Algorithmic Trading Dashboard")

# Add your trading logic here
symbol = st.selectbox("Select Stock", ["RELIANCE.NS", "TCS.NS", "INFY.NS"])
if st.button("Run Analysis"):
    data = yf.download(symbol, period="3mo")
    st.line_chart(data['Close'])
    st.success("Analysis Complete!")
