from src.scoring.risk_engine import FraudRiskEngine


def test_risk_engine_returns_expected_shape():
    engine = FraudRiskEngine()

    features = {
        "transaction_id": "txn_test_003",
        "customer_id": "cust_003",
        "merchant_id": "mrch_003",
        "amount": 8000.0,
        "is_high_amount": 1,
        "is_foreign_transaction": 0,
        "is_new_device_for_customer": 1,
        "customer_minutes_since_prev_txn": 4,
        "customer_txn_count_1d": 3,
        "customer_prev_txn_count": 3,
        "customer_amount_zscore": 2.7,
        "merchant_prev_txn_count": 4,
        "merchant_prev_fraud_rate": 0.5,
    }

    result = engine.score(features)

    assert "rule_score" in result
    assert "decision" in result
    assert "triggered_rules" in result
    assert "top_reasons" in result