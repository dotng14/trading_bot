import robin_stocks.robinhood as r


def get_basic_data(ticker):
    lastest_price = r.stocks.get_latest_price(ticker)

    historical_list = r.stocks.get_stock_historicals(ticker, interval='day', span='week')

    if(lastest_price[0] == None or historical_list[0] == None):
        return None
    day_change = ((float(lastest_price[0]) / float(historical_list[len(historical_list)-1]['close_price'])) - 1) * 100

    day_change = round(day_change, 2)
    lastest_price = round(float(lastest_price[0]), 2)
    return {
        'ticker': ticker,
        'price': lastest_price,
        'day_change': day_change
    }

def get_advanced_data(ticker):
    basic_data = get_basic_data(ticker)
    data = r.get_fundamentals(ticker)[0]
    return {
        'description' : data['description'],
        'name': basic_data['ticker'],
        'price': basic_data['price'],
        'day_change': basic_data['day_change'],
        'open': data['open'],
        'high': data['high'],
        'low': data['low'],
        'volume': data['volume'],
        'average_volume': data['average_volume'],
        'market_cap': data['market_cap'],
        'pe_ratio': data['pe_ratio'],
        'dividend_yield': data['dividend_yield']
    }

def get_stock_list():
    symbols = r.get_watchlist_by_name("My First List")
    stock_symbols = [item['symbol'] for item in symbols['results']]
    data = [get_basic_data(symbol) for symbol in stock_symbols]
    return list(filter(lambda x: x is not None, data))
