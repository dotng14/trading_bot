import yfinance as yf
import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta
def get_stock_data(ticker, period="1y"):
    """
    Fetches stock data from Yahoo Finance.
    """
    try:
        tomorrow = dt.date.today() + timedelta(days=1)
        data = yf.download(ticker, start="2020-01-01", end=tomorrow)
        print(data.iloc[-1])
        if data.empty:
            print(f"No data found for ticker: {ticker}")
            return None
        data = calculate_indicators(data, ticker)
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def calculate_indicators(data, ticker):
    """
    Calculates technical indicators, including log(Price_t / Price_{t-1}).
    """
    if data.empty:
        return data

    data['Price_Change'] = data['Close'].pct_change() * 100
    # --- Manual Calculations (for learning purposes) ---
    # Moving Averages
    data['SMA_20'] = data['Close'].rolling(window=20, closed='left').mean()
    data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()

    # Relative Strength Index (RSI)
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0.0)).fillna(0)
    loss = (-delta.where(delta < 0, 0.0)).fillna(0)
    avg_gain = gain.rolling(window=14, closed='left').mean()
    avg_loss = loss.rolling(window=14, closed='left').mean()
    rs = avg_gain / (avg_loss + 1e-8)  # Add small value to avoid division by zero
    data['RSI'] = 100 - (100 / (1 + rs))

    # Moving Average Convergence Divergence (MACD)
    ema_12 = data['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = ema_12 - ema_26
    data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()

    # Bollinger Bands
    data['StdDev'] = data['Close'].rolling(window=20, closed='left').std()
    data['UpperBollinger'] = data['SMA_20'] + (data['StdDev'] * 2)
    data['LowerBollinger'] = data['SMA_20'] - (data['StdDev'] * 2)


    # --- Log Price Ratio ---
    data['Log_Price_Ratio'] = np.log(data['Close'] / data['Close'].shift(1))


    # --- Relationships between Open, High, Low, Close ---
    data['Open_Close_Diff'] = (data['Close'] - data['Open']) / data['Open'] * 100
    data['High_Low_Diff'] = (data['High'] - data['Low']) / data['Open'] * 100
    data['Body_Size'] = abs(data['Close'] - data['Open'])
    data['Upper_Shadow'] = data['High'] - np.maximum(data['Close'], data['Open'])
    data['Lower_Shadow'] = np.minimum(data['Close'], data['Open']) - data['Low']

    # Volume Indicators
    data['OBV'] = np.where(data['Close'] > data['Close'].shift(1), data['Volume'],
                           np.where(data['Close'] < data['Close'].shift(1), -data['Volume'], 0)).cumsum()

    data['VWAP'] = (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()

    # Money Flow Index (MFI)
    typical_price = (data['High'] + data['Low'] + data['Close']) / 3
    money_flow = typical_price * data['Volume']
    positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
    negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0)
    positive_mf = positive_flow.rolling(window=14, closed='left').sum()
    negative_mf = negative_flow.rolling(window=14, closed='left').sum()
    mfi_ratio = positive_mf / (negative_mf + 1e-8)
    data['MFI'] = 100 - (100 / (1 + mfi_ratio))

    # Average Directional Index (ADX)
    high_low = data['High'] - data['Low']
    high_close = np.abs(data['High'] - data['Close'].shift(1))
    low_close = np.abs(data['Low'] - data['Close'].shift(1))
    tr = np.maximum(high_low, np.maximum(high_close, low_close))
    data['TR'] = tr
    data['ATR'] = tr.rolling(window=14, closed='left').mean()

    data['DM_plus'] = np.where((data['High'] - data['High'].shift(1)) > (data['Low'].shift(1) - data['Low']),
                               np.maximum(data['High'] - data['High'].shift(1), 0), 0)
    data['DM_minus'] = np.where((data['Low'].shift(1) - data['Low']) > (data['High'] - data['High'].shift(1)),
                                np.maximum(data['Low'].shift(1) - data['Low'], 0), 0)

    data['DI_plus'] = 100 * (data['DM_plus'].rolling(window=14, closed='left').mean() / data['ATR'])
    data['DI_minus'] = 100 * (data['DM_minus'].rolling(window=14, closed='left').mean() / data['ATR'])
    dx = 100 * np.abs(data['DI_plus'] - data['DI_minus']) / (data['DI_plus'] + data['DI_minus'] + 1e-8)
    data['ADX'] = dx.rolling(window=14, closed='left').mean()

    # Commodity Channel Index (CCI)
    mean_dev = (typical_price - typical_price.rolling(window=20, closed='left').mean()).abs().rolling(window=20, closed='left').mean()
    data['CCI'] = (typical_price - typical_price.rolling(window=20, closed='left').mean()) / (0.015 * mean_dev + 1e-8)

    # Stochastic Oscillator
    lowest_low = data['Low'].rolling(window=14, closed='left').min()
    highest_high = data['High'].rolling(window=14, closed='left').max()
    data['Stoch_%K'] = ((data['Close'] - lowest_low) / (highest_high - lowest_low + 1e-8)) * 100
    data['Stoch_%D'] = data['Stoch_%K'].rolling(window=3, closed='left').mean()

    # Williams %R
    highest_high_wr = data['High'].rolling(window=14, closed='left').max()
    lowest_low_wr = data['Low'].rolling(window=14, closed='left').min()
    data['Williams_%R'] = ((highest_high_wr - data['Close']) / (highest_high_wr - lowest_low_wr + 1e-8)) * -100

    # Historical Volatility
    data['Historical_Volatility'] = data['Close'].rolling(window=20, closed='left').std()
    # Price Rate of Change (ROC)
    data['ROC'] = 100 * (data['Close'].diff(12) / (data['Close'].shift(12) + 1e-8))

    data = data.drop(columns=['Low', 'High', 'Volume', 'Open'])
    data = process_data(data, ticker)
    return data

def process_data(data, ticker):
    """Processes data, adds a prediction row, renames columns, adds ASCII ticker."""
    if data is not None:
        data = calculate_indicators(data)  # Assuming this function exists
        if not data.empty:
            data = data.groupby(level=0, axis=1).first()
            # data = data.reset_index().drop(columns=['Date'])
            data.columns.name = None
            # data.drop(columns=['DM_minus', 'DM_plus'], inplace=True)

            # Store original column order (excluding 'Close', which will be added later if needed)
            original_columns = [col for col in data.columns if col != 'Close'] + ['Close']

            data['Ticker'] = ''.join([str(ord(c)) for c in ticker])

            # Reorder columns to original order (before dropping rows)
            cols = ['Ticker'] + [col for col in data.columns if col != 'Ticker']
            data = data[cols]
            data = data.astype(float).round(2)
            data = data.dropna(subset=[col for col in data.columns if col != 'Close' and col != 'Ticker'])  # Keep Close if it exists




            # --- End Modification ---

            # Rename columns (after row deletion, so we work with the correct rows)
            new_columns = []
            for col in data.columns:
                if col not in ['Ticker']:
                    new_columns.append(col + '-1')
                else:
                    new_columns.append(col)
            data.columns = new_columns
            last_row = data.iloc[-2:]
            rows_to_keep = []
            for i in range(len(data)):
                rows_to_keep.append(i)

            data = data.iloc[rows_to_keep]
            data = pd.concat([data, last_row], ignore_index=True)
            column_to_move = data.pop('Close-1')
            data.drop(columns = 'Ticker', inplace=True)
            data['Close-1'] = column_to_move
            return data

    return pd.DataFrame()


