from flask import Flask, render_template
import schedule
import time
import os

from binance.client import Client
from get_withdrawal_fee import get_withdrawal_fee

app = Flask(__name__)

@app.route("/")
def index():
    data = job()
    print(data)
    return render_template("index.html", data=data)

def job():
    # each coin symbol has a tuple with network, threshold fee, and threshold fee_value
    coin_symbols = {"DOGE": ("DOGE", 50, 10), "BTC": ("BTC", 0.0004, 20), "SHIB": ("ETH", 100000, 2)}
    coin_details = {}
    for symbol, (network, threshold_fee, threshold_fee_value) in coin_symbols.items():
        coin_details[symbol] = get_withdrawal_fee(client, symbol, network, threshold_fee, threshold_fee_value)
    return coin_details

if __name__ == "__main__":
    api_key = os.getenv("BINANCE_API_ACCESS_KEY", "")
    api_secret = os.getenv("BINANCE_API_SECRET_KEY", "")

    client = Client(api_key, api_secret, tld="us")
    app.run(host=os.getenv("FLASK_HOST"), port=os.getenv("FLASK_PORT"), debug=True)
    schedule.every(30).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)