from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from src.common.config import get_base_config
from src.common.logger import logger
from src.common.paths import LOGS_DIR


def write_audit_event(event_type: str, payload: dict[str, Any]) -> None:
    base_config = get_base_config()
    monitoring_cfg = base_config.get("monitoring", {})
    audit_log_file = monitoring_cfg.get("audit_log_file", str(LOGS_DIR / "prediction_audit.jsonl"))

    event = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "payload": payload,
    }

    with open(audit_log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

    logger.info(f"Audit event written: {event_type}")