import requests

from send_mail import send_email_alert

requests.packages.urllib3.util.connection.HAS_IPV6 = False


def get_withdrawal_fee(binance_client, coin_symbol="DOGE", chosen_network="DOGE", threshold_fee=50, threshold_fee_value=10):
    try:
        price = float(binance_client.get_symbol_ticker(symbol=coin_symbol+"USDT")["price"])
        all_coins_info = binance_client.get_all_coins_info()
        coin_details = {}
        for coin in all_coins_info:
            if coin["coin"] == coin_symbol:
                networks = coin["networkList"]
                for network in networks:
                    if network["network"] == chosen_network:
                        coin_details = {
                            "network": network["network"],
                            "fee": network["withdrawFee"],
                            "usdt_price": float(price),
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
        return {}