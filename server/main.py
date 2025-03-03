from flask import Flask, request, jsonify
from log_in import login_robinhood
from log_in import handle_mfa
import robin_stocks.robinhood as r
import logging
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/api")
def api():
    return jsonify({"data": "Hello, World!"})

@app.route('/login', methods=['POST'])
def login():

    data = request.json
    username = data.get('username')
    password = data.get('password')

    try:
        login_data = login_robinhood(username, password)
        challenge_id = r.get_current_challenge_id()
        return jsonify({'success': True, 'message': 'Login successful', 'data': login_data, 'challenge_id': challenge_id})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    challenge_id = data.get('challenge_id')
    mfa = data.get('mfa')

    try:
        handle_mfa(username, password, challenge_id, mfa)
        return jsonify({'success': True, 'message': 'MFA successful'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
if __name__ == "__main__":
    app.run(debug=True)