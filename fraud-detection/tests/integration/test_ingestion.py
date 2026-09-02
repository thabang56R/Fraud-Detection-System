from features.batch_features import build_batch_features
from src.common.paths import RAW_DATA_DIR
from src.data.ingestion import basic_cleaning, read_csv_data, validate_required_columns


def test_ingestion_pipeline():
    df = read_csv_data(str(RAW_DATA_DIR / "transactions_sample.csv"))
    validate_required_columns(df)
    cleaned_df = basic_cleaning(df)

    assert not cleaned_df.empty
    assert "transaction_id" in cleaned_df.columns
    assert "amount" in cleaned_df.columns


def test_batch_feature_pipeline():
    df = read_csv_data(str(RAW_DATA_DIR / "transactions_sample.csv"))
    validate_required_columns(df)
    df = basic_cleaning(df)

    features_df = build_batch_features(df)

    expected_columns = [
        "transaction_hour",
        "customer_txn_count_1d",
        "customer_prev_amount_mean",
        "merchant_prev_fraud_rate",
        "is_new_device_for_customer",
    ]

    for col in expected_columns:
        assert col in features_df.columns

    assert not features_df.empty