from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DATA_DIR = Path("data")
CSV_PATH = DATA_DIR / "chatbot_runs.csv"
JSONL_PATH = DATA_DIR / "chatbot_runs.jsonl"

FIELDNAMES = [
    "timestamp_utc",
    "session_id",
    "run_type",
    "prompt_id",
    "category",
    "bot_key",
    "blind_label",
    "provider",
    "model",
    "temperature",
    "max_output_tokens",
    "latency_seconds",
    "input_tokens",
    "output_tokens",
    "total_tokens",
    "finish_reason",
    "prompt",
    "response",
    "error",
]

def log_run(record: dict[str, Any]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    row = {field: record.get(field, "") for field in FIELDNAMES}
    row["timestamp_utc"] = row["timestamp_utc"] or datetime.now(timezone.utc).isoformat()

    new_file = not CSV_PATH.exists()
    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if new_file:
            writer.writeheader()
        writer.writerow(row)

    with JSONL_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
