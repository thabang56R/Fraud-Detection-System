from __future__ import annotations

from typing import Any

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from src.common.config import load_yaml_config


def build_preprocessor() -> ColumnTransformer:
    config = load_yaml_config("model.yaml")
    categorical_features: list[str] = config["features"]["categorical"]
    numeric_features: list[str] = config["features"]["numeric"]

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    return preprocessor


def get_feature_columns() -> dict[str, list[str]]:
    config = load_yaml_config("model.yaml")
    return {
        "categorical": config["features"]["categorical"],
        "numeric": config["features"]["numeric"],
        "drop_columns": config["features"]["drop_columns"],
    }