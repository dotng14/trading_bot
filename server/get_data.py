import robin_stocks.robinhood as r


def get_basic_data(ticker):
    lastest_price = r.stocks.get_latest_price(ticker)

    historical_list = r.stocks.get_stock_historicals(ticker, interval='day', span='week')
    
    # day_change = ((float(lastest_price) / float(historical_list[0]['close_price'])) - 1) * 100
    day_change = 0

    return lastest_price, day_change

def get_advanced_data(ticker):
    lastest_price, day_change = basic_data(ticker)
    data = r.get_fundamentals(ticker)
    return {
        'description' : data['description'],
        'name': data['name'],
        'price': lastest_price,
        'day_change': day_change,
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
    return stock_symbols
