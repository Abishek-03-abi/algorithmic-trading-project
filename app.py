from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data_fetcher import StockDataFetcher
from trading_strategies import sma_crossover_strategy, run_backtest
import os

app = Flask(__name__)
fetcher = StockDataFetcher()
strategy = TradingStrategy()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    stocks = fetcher.get_stock_list()
    return render_template('dashboard.html', stocks=stocks)

@app.route('/api/stock/<symbol>')
def get_stock_data(symbol):
    try:
        period = request.args.get('period', '3mo')
        data = fetcher.get_stock_data(symbol, period)
        if data is not None and not data.empty:
            chart_data = {
                'dates': data.index.strftime('%Y-%m-%d').tolist(),
                'prices': [float(round(price, 2)) for price in data['Close'].tolist()],
                'sma_20': [float(round(price, 2)) for price in data['SMA_20'].tolist()],
                'rsi': [float(round(rsi, 2)) for rsi in data['RSI'].tolist()]
            }
            return jsonify(chart_data)
        else:
            return jsonify({'error': 'No data available'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/backtest', methods=['POST'])
def run_backtest():
    try:
        data = request.json
        symbol = data['symbol']
        strategy_type = data['strategy']
        period = data.get('period', '3mo')
        
        stock_data = fetcher.get_stock_data(symbol, period)
        if stock_data is None or stock_data.empty:
            return jsonify({'error': 'Failed to generate stock data'}), 500
        
        if strategy_type == 'moving_average':
            results = strategy.moving_average_crossover(stock_data)
        elif strategy_type == 'rsi':
            results = strategy.rsi_strategy(stock_data)
        else:
            return jsonify({'error': 'Invalid strategy'}), 400
        
        price_data = {
            'dates': stock_data.index.strftime('%Y-%m-%d').tolist(),
            'prices': [float(round(price, 2)) for price in stock_data['Close'].tolist()],
            'sma_20': [float(round(price, 2)) for price in stock_data['SMA_20'].tolist()],
            'rsi': [float(round(rsi, 2)) for rsi in stock_data['RSI'].tolist()]
        }
        
        portfolio_data = {
            'dates': price_data['dates'],
            'market': [float(round(val, 3)) for val in results['portfolio']['cumulative_market'].tolist()],
            'strategy': [float(round(val, 3)) for val in results['portfolio']['cumulative_strategy'].tolist()]
        }
        
        response = {
            'metrics': results['metrics'],
            'price_data': price_data,
            'chart_data': portfolio_data
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
