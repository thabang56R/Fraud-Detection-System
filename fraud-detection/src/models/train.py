from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

from src.models.preprocessing import build_preprocessor


@dataclass
class TrainedModels:
    baseline_pipeline: Pipeline
    primary_pipeline: Pipeline


def build_baseline_model(random_state: int = 42) -> LogisticRegression:
    return LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=random_state,
    )


def build_primary_model(random_state: int = 42) -> XGBClassifier:
    return XGBClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.08,
        subsample=0.9,
        colsample_bytree=0.9,
        objective="binary:logistic",
        eval_metric="logloss",
        random_state=random_state,
        scale_pos_weight=1.0,
    )


def train_models(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    random_state: int = 42,
) -> TrainedModels:
    preprocessor = build_preprocessor()

    baseline_pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", build_baseline_model(random_state=random_state)),
        ]
    )

    primary_pipeline = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("model", build_primary_model(random_state=random_state)),
        ]
    )

    baseline_pipeline.fit(X_train, y_train)
    primary_pipeline.fit(X_train, y_train)

    return TrainedModels(
        baseline_pipeline=baseline_pipeline,
        primary_pipeline=primary_pipeline,
    )