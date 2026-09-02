from __future__ import annotations

from features.realtime_features import build_realtime_features
from src.common.logger import logger
from src.common.paths import RAW_DATA_DIR
from src.data.ingestion import basic_cleaning, read_csv_data
from src.models.anomaly_inference import FraudAnomalyService
from src.models.inference import FraudModelService
from src.scoring.hybrid_engine import HybridFraudScoringEngine
from src.scoring.risk_engine import FraudRiskEngine


def run_scoring_pipeline() -> dict:
    logger.info("Scoring pipeline started")

    history_df = read_csv_data(str(RAW_DATA_DIR / "transactions_sample.csv"))
    history_df = basic_cleaning(history_df)

    sample_payload = {
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

    realtime_features = build_realtime_features(
        payload=sample_payload,
        customer_history=history_df,
        merchant_history=history_df,
    )

    rule_result = FraudRiskEngine().score(realtime_features)
    model_result = FraudModelService().predict(realtime_features)
    anomaly_result = FraudAnomalyService().predict(realtime_features)
    hybrid_result = HybridFraudScoringEngine().score(realtime_features)

    result = {
        "rule_result": rule_result,
        "model_result": model_result,
        "anomaly_result": anomaly_result,
        "hybrid_result": hybrid_result,
    }

    logger.info(f"Scoring pipeline result: {result}")
    logger.info("Scoring pipeline completed")

    return result


if __name__ == "__main__":
    result = run_scoring_pipeline()
    print(result)