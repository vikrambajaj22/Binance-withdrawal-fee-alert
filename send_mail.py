import os
import smtplib

SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "")
SMTP_APP_PASSWORD = os.getenv("SMTP_APP_PASSWORD", "")


def send_email_alert(coin_symbol, coin_details, message=""):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SMTP_APP_PASSWORD)

        mail_subject = f"Alert: Binance Withdrawal Fee for {coin_symbol} Dropped"
        mail_body = f"The withdrawal fee for {coin_symbol} has dropped.\nNetwork: {coin_details['network']}\nFee: {coin_details['fee']} {coin_symbol}\nFee Value: {coin_details['fee_value']} USDT @ 1 {coin_symbol} = {coin_details['usdt_price']} USDT\nWithdrawal Min: {coin_details['withdraw_min']} {coin_symbol}\nWithdrawal Max: {coin_details['withdraw_max']} {coin_symbol}"+"\n"+message
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, f"Subject: {mail_subject}\n\n{mail_body}")
        server.quit()
    except Exception as e:
        print(f"An error occurred when sending email alert: {repr(e)}")
