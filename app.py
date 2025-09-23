from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data_fetcher import StockDataFetcher
from trading_strategies import sma_crossover_strategy, run_backtest
import os

app = Flask(__name__)
fetcher = StockDataFetcher()
# Removed: strategy = TradingStrategy() - using functions directly instead

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    stocks = fetcher.get_stock_list()
    return render_template('dashboard.html', stocks=stocks)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
