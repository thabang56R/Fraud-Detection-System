from fastapi.testclient import TestClient

from apps.api.main import app
from pipelines.training_pipeline import run_training_pipeline

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_model_info_endpoint():
    run_training_pipeline()
    response = client.get("/model/info")
    assert response.status_code == 200
    data = response.json()
    assert "supervised_model_metadata" in data
    assert "anomaly_model_metadata" in data


def test_monitoring_report_endpoint():
    response = client.get("/monitoring/report")
    assert response.status_code == 200
    data = response.json()
    assert "report" in data
    assert "report_path" in data


def test_realtime_feature_endpoint():
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

    response = client.post("/features/realtime", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "features" in data
    assert "merchant_prev_fraud_rate" in data["features"]


def test_rules_evaluate_endpoint():
    payload = {
        "transaction_id": "txn_live_002",
        "customer_id": "cust_002",
        "merchant_id": "mrch_002",
        "amount": 12000.0,
        "currency": "ZAR",
        "country": "ZA",
        "device_type": "desktop",
        "ip_address": "196.10.1.2",
        "timestamp": "2026-03-21 10:30:00",
    }

    response = client.post("/rules/evaluate", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "rules_result" in data
    assert "rule_score" in data["rules_result"]


def test_score_rules_endpoint():
    payload = {
        "transaction_id": "txn_live_003",
        "customer_id": "cust_002",
        "merchant_id": "mrch_002",
        "amount": 12000.0,
        "currency": "ZAR",
        "country": "ZA",
        "device_type": "desktop",
        "ip_address": "196.10.1.2",
        "timestamp": "2026-03-21 10:30:00",
    }

    response = client.post("/score/rules", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "result" in data
    assert "decision" in data["result"]


def test_score_model_endpoint():
    run_training_pipeline()

    payload = {
        "transaction_id": "txn_live_004",
        "customer_id": "cust_002",
        "merchant_id": "mrch_002",
        "amount": 12000.0,
        "currency": "ZAR",
        "country": "ZA",
        "device_type": "desktop",
        "ip_address": "196.10.1.2",
        "timestamp": "2026-03-21 10:30:00",
    }

    response = client.post("/score/model", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "result" in data
    assert "fraud_probability" in data["result"]


def test_score_anomaly_endpoint():
    run_training_pipeline()

    payload = {
        "transaction_id": "txn_live_005",
        "customer_id": "cust_002",
        "merchant_id": "mrch_002",
        "amount": 12000.0,
        "currency": "ZAR",
        "country": "ZA",
        "device_type": "desktop",
        "ip_address": "196.10.1.2",
        "timestamp": "2026-03-21 10:30:00",
    }

    response = client.post("/score/anomaly", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "result" in data
    assert "normalized_anomaly_score" in data["result"]


def test_score_hybrid_endpoint():
    run_training_pipeline()

    payload = {
        "transaction_id": "txn_live_006",
        "customer_id": "cust_002",
        "merchant_id": "mrch_002",
        "amount": 12000.0,
        "currency": "ZAR",
        "country": "ZA",
        "device_type": "desktop",
        "ip_address": "196.10.1.2",
        "timestamp": "2026-03-21 10:30:00",
    }

    response = client.post("/score/hybrid", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "result" in data
    assert "final_score" in data["result"]
    assert "decision" in data["result"]