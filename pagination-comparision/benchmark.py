import base64
import csv
import statistics
import time
from typing import Dict, List

import requests

BASE_URL = "http://127.0.0.1:5000"
LIMIT = 20
OFFSETS = [0, 1000, 10000, 100000, 500000, 900000]
RUNS_PER_CASE = 5


def call_offset(offset: int) -> float:
    t0 = time.perf_counter()
    r = requests.get(
        f"{BASE_URL}/books/offset-limit",
        params={"offset": offset, "limit": LIMIT},
        timeout=60
    )
    r.raise_for_status()
    return round((time.perf_counter() - t0) * 1000, 2)


def get_anchor_for_offset(offset: int) -> Dict[str, str]:
    r = requests.get(
        f"{BASE_URL}/books/offset-limit",
        params={"offset": offset, "limit": 1},
        timeout=60
    )
    r.raise_for_status()
    data = r.json()["data"]
    if not data:
        raise ValueError(f"No document found at offset={offset}")
    return data[0]


def build_cursor_token(created_at: str, oid: str) -> str:
    raw = f"{created_at}|{oid}"
    return base64.urlsafe_b64encode(raw.encode()).decode()


def call_cursor_from_anchor(cursor_token: str) -> float:
    t0 = time.perf_counter()
    r = requests.get(
        f"{BASE_URL}/books/cursor",
        params={"cursor": cursor_token, "limit": LIMIT},
        timeout=60
    )
    r.raise_for_status()
    return round((time.perf_counter() - t0) * 1000, 2)


def summarize(values: List[float]) -> Dict[str, float]:
    return {
        "min_ms": round(min(values), 2),
        "avg_ms": round(statistics.mean(values), 2),
        "max_ms": round(max(values), 2),
    }


def main() -> None:
    rows = []
    print("Running benchmark...")

    for offset in OFFSETS:
        offset_times = [call_offset(offset) for _ in range(RUNS_PER_CASE)]

        anchor = get_anchor_for_offset(offset)
        cursor_token = build_cursor_token(anchor["created_at"], anchor["id"])
        cursor_times = [call_cursor_from_anchor(cursor_token) for _ in range(RUNS_PER_CASE)]

        offset_summary = summarize(offset_times)
        cursor_summary = summarize(cursor_times)

        row = {
            "offset": offset,
            "offset_avg_ms": offset_summary["avg_ms"],
            "offset_min_ms": offset_summary["min_ms"],
            "offset_max_ms": offset_summary["max_ms"],
            "cursor_avg_ms": cursor_summary["avg_ms"],
            "cursor_min_ms": cursor_summary["min_ms"],
            "cursor_max_ms": cursor_summary["max_ms"],
            "speedup_x": round(offset_summary["avg_ms"] / cursor_summary["avg_ms"], 2)
            if cursor_summary["avg_ms"] else None,
        }
        rows.append(row)
        print(row)

    with open("benchmark_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print("Saved benchmark_results.csv")


if __name__ == "__main__":
    main()