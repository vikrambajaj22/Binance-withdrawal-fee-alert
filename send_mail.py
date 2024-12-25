import os
import smtplib

SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "")
SMTP_APP_PASSWORD = os.getenv("SMTP_APP_PASSWORD","")

def send_email_alert():
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SMTP_APP_PASSWORD)

        mail_subject = "Alert: Binance Withdrawal Fee Dropped"
        mail_body = "The withdrawal fee for DOGE has dropped to 10 USDT."
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, f"Subject: {mail_subject}\n\n{mail_body}")
        server.quit()
    except Exception as e:
        print(f"An error occurred when sending email alert: {repr(e)}")