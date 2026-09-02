from __future__ import annotations

import pandas as pd

from features.batch_features import build_batch_features
from src.common.logger import logger
from src.common.paths import RAW_DATA_DIR
from src.data.ingestion import basic_cleaning, read_csv_data
from src.monitoring.drift import generate_simple_drift_report, save_drift_report


def run_monitoring() -> dict:
    logger.info("Monitoring service started")

    df = read_csv_data(str(RAW_DATA_DIR / "transactions_sample.csv"))
    df = basic_cleaning(df)
    features_df = build_batch_features(df)

    midpoint = max(1, len(features_df) // 2)
    reference_df = features_df.iloc[:midpoint].copy()
    current_df = features_df.iloc[midpoint:].copy()

    report = generate_simple_drift_report(reference_df=reference_df, current_df=current_df)
    report_path = save_drift_report(report)

    result = {
        "message": "Monitoring report generated successfully",
        "report_path": report_path,
        "report": report,
    }

    logger.info(result)
    return result


if __name__ == "__main__":
    print(run_monitoring())