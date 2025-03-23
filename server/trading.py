import tensorflow as tf
from tensorflow import keras
import datetime as dt
import robin_stocks.robinhood as rs
import data_to_predict as data
import StandardScaler as s
import numpy as np
import get_data

ytd_return = []

def available_buying_power(num_of_stocks, allowance):
    if allowance == 0:
        account_info = rs.profiles.load_account_profile()
        buying_power = float(account_info['buying_power'])
    else:
        buying_power = allowance
    return buying_power / num_of_stocks


def making_decision(prediction_model):
    prediction_data = data.get_stock_data()
    latest_price = prediction_data.iloc[-1]['Close-1']

    scaler = s.StandardScaler()
    prediction_data = scaler.fit_transform(prediction_data.values)
    prediction_data = prediction_data.reshape(prediction_data.shape[0], prediction_data.shape[1], 1)

    do_prediction = prediction_model.predict(prediction_data[-2:, :, :])

    if do_prediction[0] < do_prediction[1] and latest_price < do_prediction[1]:
        return 1
    else:
        return 0

def buy_stock(ticker, decision, amount):
    if decision == 1:
        rs.orders.order_buy_fractional_by_price(ticker, amount)
        rs.orders.order_sell_limit(ticker, amount, float(rs.stocks.get_latest_price(ticker)[0]) * 0.98)
        return
    return
    
def sell_stock(ticker):
    holdings = rs.account.build_holdings()
    if ticker in holdings.keys():
        quantity = float(holdings[ticker]['quantity'])
        rs.orders.order_sell_fractional_by_quantity(ticker, quantity)
        return
    return

def one_day_profit_loss(list_of_stocks):
    holdings = rs.account.build_holdings()
    bought_price = 0
    return_value = 0

    for stock in list_of_stocks:
        if stock in holdings:
            quantity = float(holdings[stock]['quantity'])
            avg_price = float(holdings[stock]['average_buy_price'])
            current_price = float(holdings[stock]['price'])

            bought_price += quantity * avg_price
            return_value += (current_price - avg_price) * quantity

    ytd_return.append(return_value)
    return return_value


def ytd_profit_loss():
    return sum(ytd_return)


def choose_model(ticker):
    return f"{ticker}_model.h5"


def get_decision(ticker, num_of_stocks):
    model_path = choose_model(ticker)
    model = tf.keras.models.load_model(model_path)

    current_time = dt.datetime.now()

    if current_time.hour == 14 and current_time.minute == 0:
        decision = making_decision(model)
        available_amount = available_buying_power(num_of_stocks)
        buy_stock(ticker, decision, available_amount)

    if current_time.hour == 13 and current_time.minute == 58:
        sell_stock(ticker)

def main():
    stock_list = get_data.get_stock_list()
    for stock in stock_list:
        get_decision(stock['ticker'], len(stock_list))
        