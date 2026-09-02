from __future__ import annotations

import json
from typing import Any

import pandas as pd

from src.common.logger import logger
from src.common.paths import REPORTS_DIR


def generate_simple_drift_report(reference_df: pd.DataFrame, current_df: pd.DataFrame) -> dict[str, Any]:
    numeric_columns = [
        col for col in reference_df.columns
        if col in current_df.columns and pd.api.types.is_numeric_dtype(reference_df[col])
    ]

    report: dict[str, Any] = {
        "reference_rows": int(len(reference_df)),
        "current_rows": int(len(current_df)),
        "numeric_feature_drift": {},
    }

    for col in numeric_columns:
        report["numeric_feature_drift"][col] = {
            "reference_mean": float(reference_df[col].mean()),
            "current_mean": float(current_df[col].mean()),
            "reference_std": float(reference_df[col].std(ddof=0)) if len(reference_df[col]) > 0 else 0.0,
            "current_std": float(current_df[col].std(ddof=0)) if len(current_df[col]) > 0 else 0.0,
        }

    return report


def save_drift_report(report: dict[str, Any], filename: str = "drift_report.json") -> str:
    output_path = REPORTS_DIR / filename
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    logger.info(f"Drift report saved to {output_path}")
    return str(output_path)