from __future__ import annotations

from typing import Any

from src.common.logger import logger
from src.rules.engine import FraudRulesEngine


class FraudRiskEngine:
    def __init__(self) -> None:
        self.rules_engine = FraudRulesEngine()

    def score(self, features: dict[str, Any]) -> dict[str, Any]:
        logger.info("Running fraud risk engine")
        rule_output = self.rules_engine.evaluate(features)

        response = {
            "transaction_id": features.get("transaction_id"),
            "customer_id": features.get("customer_id"),
            "merchant_id": features.get("merchant_id"),
            "rule_score": rule_output["rule_score"],
            "decision": rule_output["decision"],
            "triggered_rules": rule_output["triggered_rules"],
            "top_reasons": [r["name"] for r in rule_output["triggered_rules"]],
            "features_used": features,
        }

        logger.info(f"Risk engine response: {response}")
        return response