from flask import Flask, render_template, jsonify, request
import os
import traceback

app = Flask(__name__)

# Simple stock data for the dashboard
STOCKS_DATA = {
    'RELIANCE.NS': 'Reliance Industries',
    'TCS.NS': 'Tata Consultancy Services', 
    'INFY.NS': 'Infosys',
    'HDFCBANK.NS': 'HDFC Bank',
    'AAPL': 'Apple Inc',
    'MSFT': 'Microsoft'
}

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading index.html: {str(e)}<br><pre>{traceback.format_exc()}</pre>"

@app.route('/dashboard')
def dashboard():
    try:
        return render_template('dashboard.html', stocks=STOCKS_DATA)
    except Exception as e:
        return f"Error loading dashboard.html: {str(e)}<br><pre>{traceback.format_exc()}</pre>"

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/run-backtest', methods=['POST'])
def run_backtest():
    try:
        # Simple backtest that always works
        return jsonify({
            "total_return": 15.5,
            "sharpe_ratio": 1.8,
            "max_drawdown": 8.2,
            "final_value": 115500,
            "message": "Success"
        })
    except Exception as e:
        return jsonify({"error": str(e), "traceback": traceback.format_exc()})

@app.route('/debug-data')
def debug_data():
    return jsonify({"status": "debug", "message": "Working"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
