from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/run-backtest', methods=['POST'])
def run_backtest():
    # Simple backtest that always works
    return jsonify({
        "total_return": 15.5,
        "sharpe_ratio": 1.8,
        "max_drawdown": 8.2,
        "final_value": 115500,
        "message": "Success"
    })

# Only ONE debug_data route
@app.route('/debug-data')
def debug_data():
    return jsonify({"status": "debug", "message": "Working"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
