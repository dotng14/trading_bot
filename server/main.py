from flask import Flask, request, jsonify
from log_in import login_robinhood
import psycopg2 as psycopg
import robin_stocks.robinhood as r
import logging
from flask_cors import CORS
import get_data
import time
import bcrypt
from get_conn import get_connection_uri

app = Flask(__name__)
CORS(app)
username = ''
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

# Azure SQL Database connection string
conn_string = get_connection_uri()

# Connect to the database
def get_db_connection():
    conn = psycopg.connect(conn_string)
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    create_table_query = """
        CREATE TABLE Users (
            Username VARCHAR(255) PRIMARY KEY,
            PasswordHash VARCHAR(255) NOT NULL,
            Email VARCHAR(255) UNIQUE NOT NULL,
            SavedStocks VARCHAR(255)[]
        );
    """

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()
# Register a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    email = data['email']

    # Hash the password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO Users (Username, PasswordHash, Email, SavedStocks) VALUES (%s, %s, %s, \'{}\')',
        (username, password_hash.decode('utf-8'), email)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'success': True, 'message': 'User registered successfully'}), 201

# Log in to the bot account
@app.route('/bot_login', methods=['POST'])
def bot_login():
    global username
    data = request.json
    username = data['username']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Get the user from the database
    cursor.execute('SELECT PasswordHash FROM Users WHERE Username = %s', (username,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        password_hash = row[0]
        # Check if the password matches
        if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            return jsonify({'success': True, 'message': 'Logged in successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

def update_saved_stocks(username, new_stocks):
    """Find user by Username and update the SavedStocks array."""
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Fetch existing saved stocks
        cursor.execute("SELECT SavedStocks FROM Users WHERE Username = %s;", (username,))
        result = cursor.fetchone()
        
        if result is None:
            print("User not found.")
            return
        
        # Update the database
        cursor.execute(
            "UPDATE Users SET SavedStocks = %s WHERE Username = %s;",
            (new_stocks, username)
        )
        
        cursor.execute("SELECT SavedStocks FROM Users WHERE Username = %s;", (username,))
        result = cursor.fetchone()
        
        if result is None:
            print("User not found.")
            return
        
        saved_stocks = result[0] if result[0] else []
        
        # Print the tickers
        print("Saved Stocks for", username, ":", saved_stocks)
        # Commit changes
        conn.commit()
        print("SavedStocks updated successfully.")
    
    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        conn.close()

@app.route('/save_stock', methods=['POST'])
def save():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    print(data)
    trading_stocks = [stock['ticker'] for stock in list(filter(lambda x: x['isTrading'] == True, data['stocks']))]
    update_saved_stocks(username, trading_stocks)
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'success': True, 'message': 'Stock saved successfully'}), 201

if __name__ == "__main__":
    app.run(debug=True)
    create_table()