from typing import Any

import numpy as np
import pandas as pd

from src.common.constants import HIGH_AMOUNT_THRESHOLD


def _safe_std(values: pd.Series) -> float:
    std = float(values.std()) if len(values) > 1 else 0.0
    if np.isnan(std):
        return 0.0
    return std


def build_realtime_features(
    payload: dict[str, Any],
    customer_history: pd.DataFrame | None = None,
    merchant_history: pd.DataFrame | None = None,
) -> dict[str, Any]:
    transaction_time = pd.to_datetime(payload.get("timestamp"), errors="coerce")
    amount = float(payload.get("amount", 0))
    country = str(payload.get("country", "")).upper()
    device_type = str(payload.get("device_type", "")).lower()
    customer_id = str(payload.get("customer_id", ""))
    merchant_id = str(payload.get("merchant_id", ""))

    features = {
        "transaction_id": payload.get("transaction_id"),
        "customer_id": customer_id,
        "merchant_id": merchant_id,
        "amount": amount,
        "currency": str(payload.get("currency", "")).upper(),
        "country": country,
        "device_type": device_type,
        "ip_address": payload.get("ip_address"),
        "timestamp": payload.get("timestamp"),
        "transaction_hour": transaction_time.hour if pd.notna(transaction_time) else -1,
        "transaction_dayofweek": transaction_time.dayofweek if pd.notna(transaction_time) else -1,
        "is_weekend": int(transaction_time.dayofweek in [5, 6]) if pd.notna(transaction_time) else 0,
        "is_night": int(transaction_time.hour in [0, 1, 2, 3, 4, 5]) if pd.notna(transaction_time) else 0,
        "customer_txn_count_1d": 0,
        "customer_txn_count_7d": 0,
        "customer_txn_count_30d": 0,
        "customer_amount_sum_1d": 0.0,
        "customer_amount_sum_7d": 0.0,
        "customer_amount_sum_30d": 0.0,
        "customer_prev_txn_count": 0,
        "customer_prev_amount_mean": 0.0,
        "customer_prev_amount_std": 0.0,
        "customer_amount_deviation": 0.0,
        "customer_amount_zscore": 0.0,
        "customer_minutes_since_prev_txn": -1.0,
        "merchant_prev_txn_count": 0,
        "merchant_prev_fraud_count": 0.0,
        "merchant_prev_fraud_rate": 0.0,
        "merchant_prev_amount_mean": 0.0,
        "is_foreign_transaction": 0,
        "is_high_amount": int(amount >= HIGH_AMOUNT_THRESHOLD),
        "is_new_device_for_customer": 1,
    }

    if customer_history is not None and not customer_history.empty:
        customer_history = customer_history.copy()
        customer_history["timestamp"] = pd.to_datetime(customer_history["timestamp"], errors="coerce")
        customer_history = customer_history.sort_values("timestamp")

        customer_rows = customer_history[customer_history["customer_id"] == customer_id].copy()

        if not customer_rows.empty:
            features["customer_prev_txn_count"] = int(len(customer_rows))

            amount_mean = float(customer_rows["amount"].mean())
            amount_std = _safe_std(customer_rows["amount"])

            features["customer_prev_amount_mean"] = amount_mean
            features["customer_prev_amount_std"] = amount_std
            features["customer_amount_deviation"] = amount - amount_mean
            features["customer_amount_zscore"] = (
                (amount - amount_mean) / amount_std if amount_std > 0 else 0.0
            )

            last_txn_time = customer_rows["timestamp"].max()
            if pd.notna(transaction_time) and pd.notna(last_txn_time):
                minutes_since = (transaction_time - last_txn_time).total_seconds() / 60.0
                features["customer_minutes_since_prev_txn"] = float(minutes_since)

            if pd.notna(transaction_time):
                features["customer_txn_count_1d"] = int(
                    (customer_rows["timestamp"] >= transaction_time - pd.Timedelta(days=1)).sum()
                )
                features["customer_txn_count_7d"] = int(
                    (customer_rows["timestamp"] >= transaction_time - pd.Timedelta(days=7)).sum()
                )
                features["customer_txn_count_30d"] = int(
                    (customer_rows["timestamp"] >= transaction_time - pd.Timedelta(days=30)).sum()
                )

                features["customer_amount_sum_1d"] = float(
                    customer_rows.loc[
                        customer_rows["timestamp"] >= transaction_time - pd.Timedelta(days=1), "amount"
                    ].sum()
                )
                features["customer_amount_sum_7d"] = float(
                    customer_rows.loc[
                        customer_rows["timestamp"] >= transaction_time - pd.Timedelta(days=7), "amount"
                    ].sum()
                )
                features["customer_amount_sum_30d"] = float(
                    customer_rows.loc[
                        customer_rows["timestamp"] >= transaction_time - pd.Timedelta(days=30), "amount"
                    ].sum()
                )

            home_country_mode = customer_rows["country"].mode()
            if not home_country_mode.empty:
                home_country = str(home_country_mode.iloc[0]).upper()
                features["is_foreign_transaction"] = int(country != home_country)

            seen_devices = set(customer_rows["device_type"].astype(str).str.lower())
            features["is_new_device_for_customer"] = int(device_type not in seen_devices)

    if merchant_history is not None and not merchant_history.empty:
        merchant_rows = merchant_history[merchant_history["merchant_id"] == merchant_id].copy()

        if not merchant_rows.empty:
            features["merchant_prev_txn_count"] = int(len(merchant_rows))
            features["merchant_prev_fraud_count"] = float(merchant_rows["is_fraud"].sum())
            features["merchant_prev_fraud_rate"] = float(merchant_rows["is_fraud"].mean())
            features["merchant_prev_amount_mean"] = float(merchant_rows["amount"].mean())

    return features