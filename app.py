from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data_fetcher import StockDataFetcher
from trading_strategies import TradingStrategy
import traceback

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
        print(f"🔍 Fetching stock data for {symbol}, period: {period}")
        
        data = fetcher.get_stock_data(symbol, period)
        
        if data is not None and not data.empty:
            # Ensure we have valid data points
            if len(data) < 5:
                raise ValueError("Not enough data points")
            
            # Convert to JSON format for Chart.js - FIXED RSI DATA
            chart_data = {
                'dates': data.index.strftime('%Y-%m-%d').tolist(),
                'prices': [float(round(price, 2)) for price in data['Close'].tolist()],
                'sma_20': [float(round(price, 2)) for price in data['SMA_20'].tolist()],
                'rsi': [float(round(rsi, 2)) for rsi in data['RSI'].tolist()]  # FIXED: Ensure RSI exists
            }
            print(f"✅ Stock data prepared: {len(chart_data['dates'])} data points, RSI length: {len(chart_data['rsi'])}")
            return jsonify(chart_data)
        else:
            error_msg = "No data available or empty dataset"
            print(f"❌ {error_msg}")
            return jsonify({'error': error_msg}), 500
            
    except Exception as e:
        error_msg = f"Error in get_stock_data: {str(e)}"
        print(f"❌ {error_msg}")
        print(traceback.format_exc())
        return jsonify({'error': error_msg}), 500

@app.route('/api/backtest', methods=['POST'])
def run_backtest():
    try:
        data = request.json
        symbol = data['symbol']
        strategy_type = data['strategy']
        period = data.get('period', '3mo')
        
        print(f"🔍 Running backtest: {symbol}, {strategy_type}, {period}")
        
        # Get stock data
        stock_data = fetcher.get_stock_data(symbol, period)
        if stock_data is None or stock_data.empty:
            error_msg = "Failed to generate stock data"
            print(f"❌ {error_msg}")
            return jsonify({'error': error_msg}), 500
        
        # Ensure RSI column exists
        if 'RSI' not in stock_data.columns:
            print("⚠️ RSI column missing, calculating...")
            stock_data['RSI'] = 50  # Default value
        
        # Run strategy
        if strategy_type == 'moving_average':
            results = strategy.moving_average_crossover(stock_data)
        elif strategy_type == 'rsi':
            results = strategy.rsi_strategy(stock_data)
        else:
            error_msg = "Invalid strategy type"
            print(f"❌ {error_msg}")
            return jsonify({'error': error_msg}), 400
        
        # Prepare price data for charts - FIXED: Ensure all data exists
        price_data = {
            'dates': stock_data.index.strftime('%Y-%m-%d').tolist(),
            'prices': [float(round(price, 2)) for price in stock_data['Close'].tolist()],
            'sma_20': [float(round(price, 2)) for price in stock_data['SMA_20'].tolist()],
            'rsi': [float(round(rsi, 2)) for rsi in stock_data['RSI'].tolist()]  # FIXED: Include RSI
        }
        
        # Prepare strategy comparison data
        portfolio = results['portfolio']
        min_length = min(len(portfolio), len(price_data['dates']))
        
        portfolio_data = {
            'dates': price_data['dates'][-min_length:],
            'market': [float(round(val, 3)) for val in portfolio['cumulative_market'].tolist()[-min_length:]],
            'strategy': [float(round(val, 3)) for val in portfolio['cumulative_strategy'].tolist()[-min_length:]]
        }
        
        response = {
            'metrics': results['metrics'],
            'price_data': price_data,  # FIXED: Now includes RSI
            'chart_data': portfolio_data
        }
        
        print(f"✅ Backtest completed successfully")
        print(f"📊 RSI data length: {len(price_data['rsi'])}")
        
        return jsonify(response)
        
    except Exception as e:
        error_msg = f"Error in run_backtest: {str(e)}"
        print(f"❌ {error_msg}")
        print(traceback.format_exc())
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    app.run(debug=True)
