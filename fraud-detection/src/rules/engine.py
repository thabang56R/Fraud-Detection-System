from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.common.config import load_yaml_config
from src.common.logger import logger


@dataclass
class RuleResult:
    name: str
    description: str
    weight: int
    action: str
    triggered: bool


class SafeEvaluator:
    """
    A minimal safe expression evaluator for boolean fraud rules.
    Supports Python boolean/comparison expressions over feature values.
    """

    ALLOWED_BUILTINS: dict[str, Any] = {
        "abs": abs,
        "min": min,
        "max": max,
        "round": round,
        "int": int,
        "float": float,
        "bool": bool,
    }

    @classmethod
    def evaluate(cls, expression: str, context: dict[str, Any]) -> bool:
        safe_globals = {"__builtins__": {}}
        safe_locals = dict(cls.ALLOWED_BUILTINS)
        safe_locals.update(context)

        result = eval(expression, safe_globals, safe_locals)
        return bool(result)


class FraudRulesEngine:
    def __init__(self, rules_config_path: str = "rules.yaml", model_config_path: str = "model.yaml"):
        rules_config = load_yaml_config(rules_config_path)
        model_config = load_yaml_config(model_config_path)

        self.rules: list[dict[str, Any]] = rules_config.get("rules", [])
        self.risk_bands: dict[str, int] = model_config.get(
            "risk_bands",
            {
                "approve_max": 29,
                "review_max": 69,
                "block_min": 70,
            },
        )

    def evaluate(self, features: dict[str, Any]) -> dict[str, Any]:
        logger.info("Evaluating fraud rules")

        results: list[RuleResult] = []
        total_score = 0

        for rule in self.rules:
            name = rule["name"]
            description = rule.get("description", "")
            condition = rule["condition"]
            weight = int(rule.get("weight", 0))
            action = rule.get("action", "review")

            try:
                triggered = SafeEvaluator.evaluate(condition, features)
            except Exception as exc:
                logger.warning(f"Failed to evaluate rule '{name}': {exc}")
                triggered = False

            if triggered:
                total_score += weight

            results.append(
                RuleResult(
                    name=name,
                    description=description,
                    weight=weight,
                    action=action,
                    triggered=triggered,
                )
            )

        decision = self._decision_from_score(total_score, results)

        output = {
            "rule_score": total_score,
            "decision": decision,
            "triggered_rules": [
                {
                    "name": r.name,
                    "description": r.description,
                    "weight": r.weight,
                    "action": r.action,
                }
                for r in results
                if r.triggered
            ],
            "all_rule_results": [
                {
                    "name": r.name,
                    "description": r.description,
                    "weight": r.weight,
                    "action": r.action,
                    "triggered": r.triggered,
                }
                for r in results
            ],
        }

        logger.info(f"Rules evaluation output: {output}")
        return output

    def _decision_from_score(self, score: int, results: list[RuleResult]) -> str:
        has_block_rule = any(r.triggered and r.action == "block" for r in results)

        if has_block_rule:
            return "block"

        approve_max = int(self.risk_bands.get("approve_max", 29))
        review_max = int(self.risk_bands.get("review_max", 69))
        block_min = int(self.risk_bands.get("block_min", 70))

        if score >= block_min:
            return "block"
        if score <= approve_max:
            return "approve"
        if score <= review_max:
            return "review"
        return "block"