from __future__ import annotations

from typing import Any

from src.common.config import load_yaml_config
from src.common.logger import logger
from src.models.anomaly_inference import FraudAnomalyService
from src.models.inference import FraudModelService
from src.monitoring.audit import write_audit_event
from src.scoring.risk_engine import FraudRiskEngine


class HybridFraudScoringEngine:
    def __init__(self) -> None:
        self.rule_engine = FraudRiskEngine()
        self.model_service = FraudModelService()
        self.anomaly_service = FraudAnomalyService()

        config = load_yaml_config("model.yaml")
        hybrid_cfg = config.get("hybrid", {})

        self.weights = hybrid_cfg.get(
            "weights",
            {"rules": 0.30, "model": 0.45, "anomaly": 0.25},
        )
        self.thresholds = hybrid_cfg.get(
            "thresholds",
            {"approve_max": 39, "review_max": 69, "block_min": 70},
        )

    def score(self, features: dict[str, Any]) -> dict[str, Any]:
        logger.info("Running hybrid fraud scoring engine")

        rule_result = self.rule_engine.score(features)
        model_result = self.model_service.predict(features)
        anomaly_result = self.anomaly_service.predict(features)

        rule_score_normalized = min(float(rule_result["rule_score"]), 100.0) / 100.0
        model_probability = float(model_result["fraud_probability"])
        anomaly_score = float(anomaly_result["normalized_anomaly_score"])

        final_score = (
            self.weights["rules"] * rule_score_normalized
            + self.weights["model"] * model_probability
            + self.weights["anomaly"] * anomaly_score
        ) * 100.0

        final_score = round(float(final_score), 2)
        decision = self._decision_from_score(final_score)

        reasons = []
        reasons.extend(rule_result.get("top_reasons", []))

        if model_probability >= 0.5:
            reasons.append("high_model_probability")

        if anomaly_score >= float(anomaly_result.get("review_threshold", 0.65)):
            reasons.append("high_anomaly_score")

        deduped_reasons = list(dict.fromkeys(reasons))

        result = {
            "transaction_id": features.get("transaction_id"),
            "customer_id": features.get("customer_id"),
            "merchant_id": features.get("merchant_id"),
            "rule_score": rule_result["rule_score"],
            "fraud_probability": round(model_probability, 4),
            "anomaly_score": round(anomaly_score, 4),
            "final_score": final_score,
            "decision": decision,
            "top_reasons": deduped_reasons,
            "rule_result": rule_result,
            "model_result": model_result,
            "anomaly_result": anomaly_result,
        }

        write_audit_event(
            event_type="hybrid_score",
            payload={
                "transaction_id": result["transaction_id"],
                "customer_id": result["customer_id"],
                "merchant_id": result["merchant_id"],
                "rule_score": result["rule_score"],
                "fraud_probability": result["fraud_probability"],
                "anomaly_score": result["anomaly_score"],
                "final_score": result["final_score"],
                "decision": result["decision"],
                "top_reasons": result["top_reasons"],
            },
        )

        logger.info(f"Hybrid fraud scoring result: {result}")
        return result

    def _decision_from_score(self, score: float) -> str:
        approve_max = float(self.thresholds.get("approve_max", 39))
        review_max = float(self.thresholds.get("review_max", 69))
        block_min = float(self.thresholds.get("block_min", 70))

        if score >= block_min:
            return "block"
        if score <= approve_max:
            return "approve"
        if score <= review_max:
            return "review"
        return "block"