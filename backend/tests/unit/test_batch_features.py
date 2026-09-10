from features.batch_features import build_batch_features
from src.common.paths import RAW_DATA_DIR
from src.data.ingestion import basic_cleaning, read_csv_data


def test_build_batch_features_generates_expected_columns():
    df = read_csv_data(str(RAW_DATA_DIR / "transactions_sample.csv"))
    df = basic_cleaning(df)

    result = build_batch_features(df)

    expected_columns = [
        "transaction_hour",
        "transaction_dayofweek",
        "is_weekend",
        "is_night",
        "customer_txn_count_1d",
        "customer_txn_count_7d",
        "customer_txn_count_30d",
        "customer_amount_sum_1d",
        "customer_amount_sum_7d",
        "customer_amount_sum_30d",
        "customer_prev_txn_count",
        "customer_prev_amount_mean",
        "customer_prev_amount_std",
        "customer_amount_deviation",
        "customer_amount_zscore",
        "customer_minutes_since_prev_txn",
        "merchant_prev_txn_count",
        "merchant_prev_fraud_count",
        "merchant_prev_fraud_rate",
        "merchant_prev_amount_mean",
        "is_foreign_transaction",
        "is_high_amount",
        "is_new_device_for_customer",
    ]

    for col in expected_columns:
        assert col in result.columns


def test_batch_features_row_count_preserved():
    df = read_csv_data(str(RAW_DATA_DIR / "transactions_sample.csv"))
    df = basic_cleaning(df)

    result = build_batch_features(df)
    assert len(result) == len(df)