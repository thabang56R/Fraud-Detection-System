from __future__ import annotations

import json

from src.common.logger import logger
from src.common.paths import MODEL_ARTIFACTS_DIR


def run_evaluation_pipeline() -> dict:
    logger.info("Evaluation pipeline started")

    metadata_path = MODEL_ARTIFACTS_DIR / "model_metadata.json"
    if not metadata_path.exists():
        raise FileNotFoundError(
            f"Model metadata not found at {metadata_path}. Run training_pipeline first."
        )

    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    logger.info("Evaluation pipeline completed")
    return metadata


if __name__ == "__main__":
    result = run_evaluation_pipeline()
    print(json.dumps(result, indent=2))