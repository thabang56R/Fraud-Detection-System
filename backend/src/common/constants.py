APP_NAME = "FinShield Fraud Detection Platform"
APP_ENV_DEFAULT = "development"
APP_VERSION = "0.1.0"

DEFAULT_SAMPLE_DATA_FILE = "transactions_sample.csv"

REQUIRED_TRANSACTION_COLUMNS = [
    "transaction_id",
    "customer_id",
    "merchant_id",
    "amount",
    "currency",
    "country",
    "device_type",
    "ip_address",
    "timestamp",
    "is_fraud",
]

HIGH_AMOUNT_THRESHOLD = 5000.0