from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline

from src.common.config import load_yaml_config
from src.models.preprocessing import build_preprocessor


@dataclass
class TrainedAnomalyModel:
    pipeline: Pipeline


def build_anomaly_model(random_state: int = 42) -> IsolationForest:
    config = load_yaml_config("model.yaml")
    anomaly_cfg = config.get("anomaly", {})

    return IsolationForest(
        n_estimators=int(anomaly_cfg.get("n_estimators", 200)),
        contamination=float(anomaly_cfg.get("contamination", 0.15)),
        random_state=random_state,
    )


def train_anomaly_model(
    X_train: pd.DataFrame,
    random_state: int = 42,
) -> TrainedAnomalyModel:
    preprocessor = build_preprocessor()

    model = build_anomaly_model(random_state=random_state)

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    pipeline.fit(X_train)
    return TrainedAnomalyModel(pipeline=pipeline)


def normalize_anomaly_scores(raw_scores: np.ndarray) -> np.ndarray:
    """
    IsolationForest score_samples():
    Higher = more normal, lower = more anomalous.
    We invert and min-max normalize so higher = more anomalous.
    """
    inverted = -raw_scores
    min_val = float(np.min(inverted))
    max_val = float(np.max(inverted))

    if max_val - min_val == 0:
        return np.zeros_like(inverted, dtype=float)

    return (inverted - min_val) / (max_val - min_val)