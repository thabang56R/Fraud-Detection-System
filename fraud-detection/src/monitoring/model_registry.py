from __future__ import annotations

import json
from typing import Any

from src.common.paths import MODEL_ARTIFACTS_DIR


def load_model_metadata() -> dict[str, Any]:
    metadata_path = MODEL_ARTIFACTS_DIR / "model_metadata.json"
    if not metadata_path.exists():
        return {}

    with open(metadata_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_anomaly_metadata() -> dict[str, Any]:
    metadata_path = MODEL_ARTIFACTS_DIR / "anomaly_metadata.json"
    if not metadata_path.exists():
        return {}

    with open(metadata_path, "r", encoding="utf-8") as f:
        return json.load(f)