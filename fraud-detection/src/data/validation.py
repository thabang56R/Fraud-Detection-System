import pandas as pd

from src.common.constants import REQUIRED_TRANSACTION_COLUMNS
from src.common.logger import logger


def validate_dataframe(df: pd.DataFrame) -> dict:
    report = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "missing_columns": [],
        "null_counts": {},
        "duplicate_transaction_ids": 0,
        "invalid_amount_rows": 0,
        "invalid_target_rows": 0,
        "status": "success",
    }

    missing_columns = [col for col in REQUIRED_TRANSACTION_COLUMNS if col not in df.columns]
    report["missing_columns"] = missing_columns

    if missing_columns:
        report["status"] = "failed"
        return report

    report["null_counts"] = df[REQUIRED_TRANSACTION_COLUMNS].isnull().sum().to_dict()
    report["duplicate_transaction_ids"] = int(df["transaction_id"].duplicated().sum())
    report["invalid_amount_rows"] = int((df["amount"] < 0).sum())
    report["invalid_target_rows"] = int((~df["is_fraud"].isin([0, 1])).sum())

    has_nulls = any(v > 0 for v in report["null_counts"].values())
    has_issues = (
        has_nulls
        or report["duplicate_transaction_ids"] > 0
        or report["invalid_amount_rows"] > 0
        or report["invalid_target_rows"] > 0
    )

    if has_issues:
        report["status"] = "failed"

    logger.info(f"Validation report: {report}")
    return report