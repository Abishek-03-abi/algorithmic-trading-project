from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data_fetcher import StockDataFetcher
from trading_strategies import sma_crossover_strategy, run_backtest
import os

app = Flask(__name__)
fetcher = StockDataFetcher()

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

@app.route('/debug-data')
def debug_data():
    try:
        from data_fetcher import StockDataFetcher
        fetcher = StockDataFetcher()
        
        # Test data fetching
        symbol = "RELIANCE.NS"
        data = fetcher.get_stock_data(symbol, "3mo")
        
        return jsonify({
            "symbol": symbol,
            "data_columns": list(data.columns) if data is not None else "No data",
            "data_shape": data.shape if data is not None else "No data",
            "sample_data": data.head(3).to_dict() if data is not None else "No data"
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/run-backtest', methods=['POST'])
def run_backtest_route():
    try:
        data = request.get_json()
        symbol = data.get('symbol', 'RELIANCE.NS')
        strategy_name = data.get('strategy', 'sma_crossover')
        period = data.get('period', '3mo')
        capital = float(data.get('capital', 100000))
        
        # Map strategy name to function
        if strategy_name == 'Moving Average Crossover':
            strategy_func = sma_crossover_strategy
        else:
            strategy_func = sma_crossover_strategy
            
        result = run_backtest(symbol, strategy_func, period, capital)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/debug-data')
def debug_data():
    try:
        symbol = "RELIANCE.NS"
        data = fetcher.get_stock_data(symbol, "3mo")
        
        return jsonify({
            "symbol": symbol,
            "data_columns": list(data.columns) if data is not None else "No data",
            "data_shape": data.shape if data is not None else "No data",
            "sample_data": data.head(3).to_dict() if data is not None else "No data"
        })
    except Exception as e:
        return jsonify({"error": str(e)})
