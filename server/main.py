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

    if(login_robinhood(username, password)):
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        return jsonify({'success': False, 'message': 'Login failed'})

@app.route("/stock_list", methods=['GET'])
def stock_list():
    logging.debug("Received stock list request")
    data = get_data.get_stock_list()
    logging.debug(data)
    logging.debug(jsonify({'stock_list': data}))
    return jsonify({'stock_list': data})

@app.route("/advanced_data", methods=['POST'])
def advanced_data():
    input = request.json
    data = get_data.get_advanced_data(input.get('ticker'))
    logging.debug(jsonify({'data' : data}))
    return jsonify({'data' : data})

if __name__ == "__main__":
    app.run(debug=True)