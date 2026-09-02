import numpy as np
import pandas as pd

from src.common.constants import HIGH_AMOUNT_THRESHOLD
from src.common.logger import logger


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["transaction_hour"] = df["timestamp"].dt.hour
    df["transaction_dayofweek"] = df["timestamp"].dt.dayofweek
    df["is_weekend"] = df["transaction_dayofweek"].isin([5, 6]).astype(int)
    df["is_night"] = df["transaction_hour"].isin([0, 1, 2, 3, 4, 5]).astype(int)

    return df


def add_customer_velocity_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().sort_values("timestamp").reset_index(drop=True)

    windows = {
        "1d": "1D",
        "7d": "7D",
        "30d": "30D",
    }

    result_frames = []

    for customer_id, group in df.groupby("customer_id", sort=False):
        group = group.sort_values("timestamp").copy()
        group = group.set_index("timestamp")

        for label, window in windows.items():
            shifted_amount = group["amount"].shift(1)
            shifted_count = shifted_amount.notna().astype(int)

            group[f"customer_txn_count_{label}"] = shifted_count.rolling(window).sum().fillna(0)
            group[f"customer_amount_sum_{label}"] = shifted_amount.rolling(window).sum().fillna(0)

        group = group.reset_index()
        result_frames.append(group)

    df = pd.concat(result_frames, axis=0).sort_values("timestamp").reset_index(drop=True)
    return df


def add_customer_behavior_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().sort_values(["customer_id", "timestamp"]).reset_index(drop=True)

    grouped = df.groupby("customer_id", sort=False)

    df["customer_prev_txn_count"] = grouped.cumcount()

    prev_mean = grouped["amount"].expanding().mean().shift(1)
    prev_std = grouped["amount"].expanding().std().shift(1)

    df["customer_prev_amount_mean"] = prev_mean.reset_index(level=0, drop=True)
    df["customer_prev_amount_std"] = prev_std.reset_index(level=0, drop=True)

    df["customer_prev_amount_mean"] = df["customer_prev_amount_mean"].fillna(0)
    df["customer_prev_amount_std"] = df["customer_prev_amount_std"].fillna(0)

    df["customer_amount_deviation"] = df["amount"] - df["customer_prev_amount_mean"]

    df["customer_amount_zscore"] = np.where(
        df["customer_prev_amount_std"] > 0,
        (df["amount"] - df["customer_prev_amount_mean"]) / df["customer_prev_amount_std"],
        0,
    )

    prev_timestamps = grouped["timestamp"].shift(1)
    df["customer_minutes_since_prev_txn"] = (
        (df["timestamp"] - prev_timestamps).dt.total_seconds() / 60.0
    ).fillna(-1)

    return df


def add_merchant_risk_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().sort_values(["merchant_id", "timestamp"]).reset_index(drop=True)

    grouped = df.groupby("merchant_id", sort=False)

    df["merchant_prev_txn_count"] = grouped.cumcount()
    df["merchant_prev_fraud_count"] = grouped["is_fraud"].cumsum().shift(1).fillna(0)

    df["merchant_prev_fraud_rate"] = np.where(
        df["merchant_prev_txn_count"] > 0,
        df["merchant_prev_fraud_count"] / df["merchant_prev_txn_count"],
        0,
    )

    prev_amount_mean = grouped["amount"].expanding().mean().shift(1)
    df["merchant_prev_amount_mean"] = prev_amount_mean.reset_index(level=0, drop=True).fillna(0)

    return df


def add_geo_device_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().sort_values(["customer_id", "timestamp"]).reset_index(drop=True)

    customer_home_country = (
        df.groupby("customer_id")["country"]
        .transform(lambda s: s.mode().iloc[0] if not s.mode().empty else s.iloc[0])
    )

    df["is_foreign_transaction"] = (df["country"] != customer_home_country).astype(int)
    df["is_high_amount"] = (df["amount"] >= HIGH_AMOUNT_THRESHOLD).astype(int)

    seen_devices = {}
    is_new_device = []

    for _, row in df.iterrows():
        customer_id = row["customer_id"]
        device_type = row["device_type"]

        if customer_id not in seen_devices:
            seen_devices[customer_id] = set()

        is_new = int(device_type not in seen_devices[customer_id])
        is_new_device.append(is_new)

        seen_devices[customer_id].add(device_type)

    df["is_new_device_for_customer"] = is_new_device
    return df


def build_batch_features(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Starting batch feature engineering")

    df = add_time_features(df)
    df = add_customer_velocity_features(df)
    df = add_customer_behavior_features(df)
    df = add_merchant_risk_features(df)
    df = add_geo_device_features(df)

    numeric_cols = [
        "customer_txn_count_1d",
        "customer_txn_count_7d",
        "customer_txn_count_30d",
        "customer_amount_sum_1d",
        "customer_amount_sum_7d",
        "customer_amount_sum_30d",
        "customer_prev_txn_count",
        "customer_prev_amount_mean",
        "customer_prev_amount_std",
        "customer_amount_deviation",
        "customer_amount_zscore",
        "customer_minutes_since_prev_txn",
        "merchant_prev_txn_count",
        "merchant_prev_fraud_count",
        "merchant_prev_fraud_rate",
        "merchant_prev_amount_mean",
        "is_foreign_transaction",
        "is_high_amount",
        "is_new_device_for_customer",
        "transaction_hour",
        "transaction_dayofweek",
        "is_weekend",
        "is_night",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = df[col].replace([np.inf, -np.inf], 0).fillna(0)

    logger.info(f"Batch feature engineering completed with shape: {df.shape}")
    return df