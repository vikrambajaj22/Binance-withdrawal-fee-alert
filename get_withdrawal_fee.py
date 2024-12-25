import os
import time

import schedule
from binance.client import Client

from send_mail import send_email_alert


def get_withdrawal_fee(coin_symbol="DOGE", chosen_network="DOGE", threshold_fee=50, threshold_fee_value=10):
    try:
        price = float(client.get_symbol_ticker(symbol=coin_symbol+"USDT")["price"])
        all_coins_info = client.get_all_coins_info()
        coin_details = {}
        for coin in all_coins_info:
            if coin["coin"] == coin_symbol:
                networks = coin["networkList"]
                for network in networks:
                    if network["network"] == chosen_network:
                        coin_details = {
                            "network": network["network"],
                            "fee": network["withdrawFee"],
                            "usdt_price": price,
                            "fee_value": float(network["withdrawFee"]) * price,
                            "withdraw_min": network["withdrawMin"],
                            "withdraw_max": network["withdrawMax"]
                        }
                        if float(coin_details["fee"]) < threshold_fee or coin_details["fee_value"] < threshold_fee_value:
                            send_email_alert(coin_symbol, coin_details)
                        break
                break
        return coin_details
    except Exception as e:
        print(f"An error occurred: {repr(e)}")

def job():
    # each coin symbol has a tuple with network, threshold fee, and threshold fee_value
    coin_symbols = {"DOGE": ("DOGE", 50, 10), "BTC": ("BTC", 0.0004, 20), "SHIB": ("ETH", 301765, 5)}
    coin_details = {}
    for symbol, (network, threshold_fee, threshold_fee_value) in coin_symbols.items():
        coin_details[symbol] = get_withdrawal_fee(symbol, network, threshold_fee, threshold_fee_value)

if __name__ == "__main__":
    api_key = os.genenv("BINANCE_API_ACCESS_KEY", "")
    api_secret = os.genenv("BINANCE_API_SECRET_KEY", "")

    client = Client(api_key, api_secret, tld="us")

    schedule.every(30).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)