from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data_fetcher import StockDataFetcher
from trading_strategies import TradingStrategy
import os

app = Flask(__name__)
fetcher = StockDataFetcher()
strategy = TradingStrategy()

# ... (keep all your routes the same) ...

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)  # Changed for production
