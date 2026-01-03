import json
import os
from datetime import datetime, timedelta, timezone
from config import OUTPUT_JSON

def _parse_iso(ts: str) -> datetime:
    if ts.endswith("Z"):
        ts = ts[:-1]
    return datetime.fromisoformat(ts).replace(tzinfo=timezone.utc)

def load_records():
    if not os.path.exists(OUTPUT_JSON):
        return []
    try:
        with open(OUTPUT_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []

def save_record(record: dict):
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)

    records = load_records()
    records.append(record)

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=24)

    filtered = []
    for r in records:
        ts = r.get("timestamp_utc")
        if not ts:
            continue
        try:
            dt = _parse_iso(ts)
            if dt >= cutoff:
                filtered.append(r)
        except Exception:
            continue

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)

    return len(filtered)
