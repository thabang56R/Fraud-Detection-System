from features.realtime_features import build_realtime_features
from src.common.paths import RAW_DATA_DIR
from src.data.ingestion import basic_cleaning, read_csv_data


def test_build_realtime_features():
    history_df = read_csv_data(str(RAW_DATA_DIR / "transactions_sample.csv"))
    history_df = basic_cleaning(history_df)

    payload = {
        "transaction_id": "txn_live_001",
        "customer_id": "cust_002",
        "merchant_id": "mrch_002",
        "amount": 12000.0,
        "currency": "ZAR",
        "country": "ZA",
        "device_type": "desktop",
        "ip_address": "196.10.1.2",
        "timestamp": "2026-03-21 10:30:00",
    }

    features = build_realtime_features(
        payload=payload,
        customer_history=history_df,
        merchant_history=history_df,
    )

    assert features["customer_id"] == "cust_002"
    assert "customer_prev_txn_count" in features
    assert "merchant_prev_fraud_rate" in features
    assert "is_high_amount" in features