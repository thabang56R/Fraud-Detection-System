from src.rules.engine import FraudRulesEngine


def test_rules_engine_triggers_expected_rules():
    engine = FraudRulesEngine()

    features = {
        "transaction_id": "txn_test_001",
        "customer_id": "cust_001",
        "merchant_id": "mrch_001",
        "amount": 12000.0,
        "is_high_amount": 1,
        "is_foreign_transaction": 1,
        "is_new_device_for_customer": 1,
        "customer_minutes_since_prev_txn": 5,
        "customer_txn_count_1d": 5,
        "customer_prev_txn_count": 4,
        "customer_amount_zscore": 3.1,
        "merchant_prev_txn_count": 5,
        "merchant_prev_fraud_rate": 0.5,
    }

    result = engine.evaluate(features)

    assert result["rule_score"] > 0
    assert result["decision"] in {"review", "block"}
    assert len(result["triggered_rules"]) > 0


def test_rules_engine_returns_approve_for_low_risk():
    engine = FraudRulesEngine()

    features = {
        "transaction_id": "txn_test_002",
        "customer_id": "cust_002",
        "merchant_id": "mrch_002",
        "amount": 100.0,
        "is_high_amount": 0,
        "is_foreign_transaction": 0,
        "is_new_device_for_customer": 0,
        "customer_minutes_since_prev_txn": 200,
        "customer_txn_count_1d": 1,
        "customer_prev_txn_count": 5,
        "customer_amount_zscore": 0.2,
        "merchant_prev_txn_count": 10,
        "merchant_prev_fraud_rate": 0.0,
    }

    result = engine.evaluate(features)

    assert result["rule_score"] == 0
    assert result["decision"] == "approve"