import robin_stocks.robinhood as r
import data_for_currentTrading as get
import data_to_plot as plot
import sys

def login_robinhood(USERNAME, PASSWORD):
    login_data = r.login(USERNAME, PASSWORD, pickle_name="pickle_name")
    print("Logged in successfully.")
    return login_data

def handle_mfa(username, password, challenge_id, mfa_code):
    # todo: handles bad mfa input
    r.respond_to_challenge(challenge_id, mfa_code)
    return r.login(username, password)

def logout():
    r.authentication.logout()
    print("Logged out.")

if __name__ == '__main__':
    args = sys.argv;
    if len(args) != 2:
        sys.exit(1);

    username = args[0];
    password = args[1];
    login_robinhood(username, password)

    get.get_stock_data_and_save_to_json("AAPL")
    plot.get_historical_stock_data(["AAPL"])