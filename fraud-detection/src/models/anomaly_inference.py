from __future__ import annotations

import json
from typing import Any

import joblib
import numpy as np
import pandas as pd

from src.common.logger import logger
from src.common.paths import MODEL_ARTIFACTS_DIR


class FraudAnomalyService:
    def __init__(self, model_name: str = "isolation_forest_model.joblib") -> None:
        self.model_path = MODEL_ARTIFACTS_DIR / model_name
        self.metadata_path = MODEL_ARTIFACTS_DIR / "anomaly_metadata.json"

        if not self.model_path.exists():
            raise FileNotFoundError(f"Anomaly model artifact not found: {self.model_path}")

        self.model = joblib.load(self.model_path)
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> dict[str, Any]:
        if not self.metadata_path.exists():
            return {}
        with open(self.metadata_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def predict(self, features: dict[str, Any]) -> dict[str, Any]:
        df = pd.DataFrame([features])

        raw_score = float(self.model.named_steps["model"].score_samples(
            self.model.named_steps["preprocessor"].transform(df)
        )[0])

        train_min = float(self.metadata.get("raw_score_min", raw_score))
        train_max = float(self.metadata.get("raw_score_max", raw_score))

        inverted = -raw_score
        inv_min = -train_max
        inv_max = -train_min

        if inv_max - inv_min == 0:
            normalized_score = 0.0
        else:
            normalized_score = (inverted - inv_min) / (inv_max - inv_min)

        normalized_score = float(max(0.0, min(1.0, normalized_score)))

        review_threshold = float(self.metadata.get("review_threshold", 0.65))
        anomaly_label = int(normalized_score >= review_threshold)

        result = {
            "model_name": self.metadata.get("model_name", "isolation_forest"),
            "raw_anomaly_score": raw_score,
            "normalized_anomaly_score": normalized_score,
            "anomaly_prediction": anomaly_label,
            "review_threshold": review_threshold,
            "recommendation": "review" if anomaly_label == 1 else "approve",
        }

        logger.info(f"Anomaly inference result: {result}")
        return result