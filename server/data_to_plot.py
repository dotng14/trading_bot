import robin_stocks.robinhood as rh
import json
import time
from datetime import datetime, timedelta
import os

def get_historical_stock_data(symbols, output_directory="stock_data"):
    """
    Retrieves historical stock data for specified symbols and saves it to JSON files.

    Args:
        symbols (list): A list of stock symbols (e.g., ["AAPL", "GOOG"]).
        output_directory (str): The directory to save the JSON files.
    """

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for symbol in symbols:
        try:
            # 1 Day data
            one_day_data = rh.stocks.get_stock_historicals(symbol, interval="5minute", span="day")
            save_to_json(one_day_data, symbol, "1day", output_directory)

            # 1 Week data
            one_week_data = rh.stocks.get_stock_historicals(symbol, interval="10minute", span="week")
            save_to_json(one_week_data, symbol, "1week", output_directory)

            # 1 Month data
            one_month_data = rh.stocks.get_stock_historicals(symbol, interval="hour", span="month")
            save_to_json(one_month_data, symbol, "1month", output_directory)

            # 1 Year data
            one_year_data = rh.stocks.get_stock_historicals(symbol, interval="day", span="year")
            save_to_json(one_year_data, symbol, "1year", output_directory)

            print(f"Historical data for {symbol} retrieved and saved.")

        except Exception as e:
            print(f"Error retrieving historical data for {symbol}: {e}")

def save_to_json(data, symbol, span, output_directory):
    """Saves stock data to a JSON file."""
    output_file = os.path.join(output_directory, f"{symbol}_{span}_data.json")
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":

    stock_symbols = ["AAPL", "MSFT", "TSLA"]
    get_historical_stock_data(stock_symbols)