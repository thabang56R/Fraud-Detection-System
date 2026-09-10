from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from src.common.logger import logger
from src.common.paths import MODEL_ARTIFACTS_DIR


class FraudModelService:
    def __init__(self, model_name: str = "xgboost_model.joblib") -> None:
        self.model_path = MODEL_ARTIFACTS_DIR / model_name
        self.metadata_path = MODEL_ARTIFACTS_DIR / "model_metadata.json"

        if not self.model_path.exists():
            raise FileNotFoundError(f"Model artifact not found: {self.model_path}")

        self.model = joblib.load(self.model_path)
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> dict[str, Any]:
        if not self.metadata_path.exists():
            return {}
        with open(self.metadata_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def predict(self, features: dict[str, Any]) -> dict[str, Any]:
        df = pd.DataFrame([features])
        probability = float(self.model.predict_proba(df)[0, 1])
        prediction = int(probability >= self.metadata.get("threshold", 0.5))

        result = {
            "model_name": self.metadata.get("primary_model", "xgboost"),
            "fraud_probability": probability,
            "prediction": prediction,
            "threshold": self.metadata.get("threshold", 0.5),
        }

        logger.info(f"Model inference result: {result}")
        return result