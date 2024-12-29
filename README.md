# Binance Withdrawal Fee Alert

Hosted on Google Cloud App Engine. Sends custom email alerts when withdrawal fees drop below preset thresholds.

Environment setup:
```
conda create -n binance-withdrawal python=3.12
conda activate binance-withdrawal
pip install -r requirements.txt
```

To test changes locally:
```
conda activate binance-withdrawal
source .env.sh
python main.py
```

To re-deploy after making any changes:

```
gcloud app deploy
```

To stream Google Cloud logs:
```
gcloud app logs tail -s default
```