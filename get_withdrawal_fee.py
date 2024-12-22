from binance.client import Client
import schedule
import time

def get_withdrawal_fee(coin_symbol="DOGE"):
    try:
        price = float(client.get_symbol_ticker(symbol=coin_symbol+"USDT")["price"])
        all_coins_info = client.get_all_coins_info()
        for coin in all_coins_info:
            if coin["coin"] == coin_symbol:
                networks = coin["networkList"]
                for network in networks:
                    print(f"network: {network['network']}, fee: {network['withdrawFee']}, fee_value: ${float(network['withdrawFee'])*price} @ ${price}, withdraw_min: {network['withdrawMin']}, , withdraw_max: {network['withdrawMax']}")
                break
    except Exception as e:
        print(f"An error occurred: {repr(e)}")

def job():
    coin_symbols = ["DOGE", "BTC", "SHIB"]
    for symbol in coin_symbols:
        get_withdrawal_fee(symbol)

if __name__ == "__main__":
    with open("api-access-key.txt", "r") as f:
        api_key = f.read().strip()
    with open("api-secret-key.txt", "r") as f:
        api_secret = f.read().strip()

    client = Client(api_key, api_secret, tld="us")

    schedule.every(30).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)