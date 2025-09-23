from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

STOCKS = {
    'RELIANCE.NS': 'Reliance Industries',
    'TCS.NS': 'Tata Consultancy Services', 
    'INFY.NS': 'Infosys',
    'AAPL': 'Apple Inc'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', stocks=STOCKS)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

# Frontend /api/backtest ku match pannu
@app.route('/api/backtest', methods=['POST'])
def run_backtest():
    return jsonify({
        "total_return": 15.5,
        "sharpe_ratio": 1.8,
        "max_drawdown": 8.2,
        "final_value": 115500
    })

# Old route um vachukalam (optional)
@app.route('/run-backtest', methods=['POST'])
def run_backtest_old():
    return jsonify({
        "total_return": 15.5,
        "sharpe_ratio": 1.8,
        "max_drawdown": 8.2,
        "final_value": 115500
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
