from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    roc_auc_score,
)


def evaluate_classifier(
    model,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    threshold: float = 0.5,
) -> dict[str, Any]:
    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= threshold).astype(int)

    has_both_classes = len(np.unique(y_test)) > 1

    metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(precision_score(y_test, predictions, zero_division=0)),
        "recall": float(recall_score(y_test, predictions, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, probabilities)) if has_both_classes else 0.0,
        "pr_auc": float(average_precision_score(y_test, probabilities)) if has_both_classes else 0.0,
        "confusion_matrix": confusion_matrix(y_test, predictions, labels=[0, 1]).tolist(),
        "classification_report": classification_report(
            y_test,
            predictions,
            labels=[0, 1],
            zero_division=0,
            output_dict=True,
        ),
        "threshold": float(threshold),
        "support": int(len(y_test)),
        "positive_rate_actual": float(pd.Series(y_test).mean()) if len(y_test) > 0 else 0.0,
        "positive_rate_predicted": float(pd.Series(predictions).mean()) if len(predictions) > 0 else 0.0,
    }

    return metrics