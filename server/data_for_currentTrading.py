import robin_stocks.robinhood as rs
import json

from robin_stocks.urls import fundamentals


def get_stock_data_and_save_to_json(symbol):
    """
    Retrieves stock data for a given symbol using Robinhood API (assuming already logged in)
    and saves it to a JSON file named after the stock ticker.

    Args:
        symbol (str): The stock symbol (e.g., "AAPL").
    """
    try:
        # Get stock quote data
        quote_data = rs.stocks.get_quotes(symbol)

        if quote_data and quote_data[0]:
            # Get historical stock data (optional)
            fundamentals_data = rs.stocks.get_fundamentals(symbol)

            # Combine data
            data_to_save = {
                "quote": quote_data[0],
                "fundamental": fundamentals_data[0] if fundamentals_data else [],
            }

            # Create filename based on stock ticker
            filename = f"{symbol.lower()}_stock_data.json"

            # Save to JSON
            with open(filename, "w") as f:
                json.dump(data_to_save, f, indent=4)

            print(f"Stock data for {symbol} saved to {filename}")

        else:
            print(f"Could not retrieve quote data for {symbol}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage (call this after successful login):
if __name__ == "__main__":
    stock_symbols = ["AAPL", "MSFT", "TSLA"]  # Example list of stock symbols
    for symbol in stock_symbols:
        get_stock_data_and_save_to_json(symbol)