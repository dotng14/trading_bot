from flask import Flask, request, jsonify
from log_in import login_robinhood

app = Flask(__name__)

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
        return jsonify({'success': True, 'message': 'Login successful', 'data': login_data})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == "__main__":
    app.run(debug=True)