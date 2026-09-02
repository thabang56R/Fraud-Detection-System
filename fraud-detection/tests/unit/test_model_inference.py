from pipelines.training_pipeline import run_training_pipeline
from src.models.inference import FraudModelService


def test_model_service_predict_returns_expected_shape():
    run_training_pipeline()

    service = FraudModelService()

    features = {
        "amount": 12000.0,
        "currency": "ZAR",
        "country": "ZA",
        "device_type": "desktop",
        "ip_address": "196.10.1.2",
        "transaction_hour": 10,
        "transaction_dayofweek": 5,
        "is_weekend": 1,
        "is_night": 0,
        "customer_txn_count_1d": 3,
        "customer_txn_count_7d": 4,
        "customer_txn_count_30d": 4,
        "customer_amount_sum_1d": 30000.0,
        "customer_amount_sum_7d": 31000.0,
        "customer_amount_sum_30d": 31000.0,
        "customer_prev_txn_count": 3,
        "customer_prev_amount_mean": 10000.0,
        "customer_prev_amount_std": 500.0,
        "customer_amount_deviation": 2000.0,
        "customer_amount_zscore": 4.0,
        "customer_minutes_since_prev_txn": 12.0,
        "merchant_prev_txn_count": 5,
        "merchant_prev_fraud_count": 3.0,
        "merchant_prev_fraud_rate": 0.6,
        "merchant_prev_amount_mean": 9800.0,
        "is_foreign_transaction": 0,
        "is_high_amount": 1,
        "is_new_device_for_customer": 1,
    }

    result = service.predict(features)

    assert "fraud_probability" in result
    assert "prediction" in result
    assert 0.0 <= result["fraud_probability"] <= 1.0