import robin_stocks.robinhood as r
import data_for_currentTrading as get
import data_to_plot as plot
import sys

def login_robinhood(USERNAME, PASSWORD):
    print(USERNAME + " " + PASSWORD)
    login_data = r.login(USERNAME, PASSWORD, store_session=True)
    return login_data


def logout():
    r.authentication.logout()
    print("Logged out.")

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        sys.exit(1)

    username = args[0]
    password = args[1]
    login_robinhood(username, password)

    get.get_stock_data_and_save_to_json("MSFT")
    plot.get_historical_stock_data(["MSFT"])