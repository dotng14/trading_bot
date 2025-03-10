from flask import Flask, request, jsonify
from log_in import login_robinhood
import robin_stocks.robinhood as r
import logging
from flask_cors import CORS
import get_data
import time

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/api")
def api():
    return jsonify({"data": "Hello, World!"})

@app.route('/login', methods=['POST'])
def login():
    logging.debug("Received login request")

    data = request.json
    username = data.get('username')
    password = data.get('password')

    logging.debug(f"Username: {username}")
    logging.debug(f"Password: {password}")

    if(login_robinhood(username, password)):
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        return jsonify({'success': False, 'message': 'Login failed'})

@app.route("/basic_data", methods=['POST'])
def basic_data():
    logging.debug("Received basic data request")
    data = request.json
    ticker = data.get('name')
    data = get_data.get_basic_data(ticker)
    logging.debug(data)
    return jsonify({'price': time.time(), 'day_change': data[1]})

@app.route("/stock_list", methods=['GET'])
def stock_list():
    logging.debug("Received stock list request")
    symbols = get_data.get_stock_list()
    print(symbols)
    return jsonify({'stock_list': symbols})

if __name__ == "__main__":
    app.run(debug=True)