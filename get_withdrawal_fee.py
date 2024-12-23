from binance.client import Client
import schedule
import time

def get_withdrawal_fee(coin_symbol="DOGE", chosen_network="DOGE"):
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
                        break
                break
        return coin_details
    except Exception as e:
        print(f"An error occurred: {repr(e)}")

def job():
    coin_symbols = {"DOGE": "DOGE", "BTC": "BTC", "SHIB": "ETH"}  # symbol:network
    coin_details = {}
    for symbol, network in coin_symbols.items():
        coin_details[symbol] = get_withdrawal_fee(symbol, network)
    print(coin_details)

if __name__ == "__main__":
    with open("api-access-key.txt", "r") as f:
        api_key = f.read().strip()
    with open("api-secret-key.txt", "r") as f:
        api_secret = f.read().strip()

    client = Client(api_key, api_secret, tld="us")

    schedule.every(1).hour.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)