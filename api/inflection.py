from __future__ import annotations

import json
import time
from http.server import BaseHTTPRequestHandler
from pathlib import Path


SNAPSHOT = Path(__file__).resolve().with_name("inflection_snapshot.json")
INFLECTION_PROFILE = {"max_names": 12, "max_weight": 0.11, "cash": 0.04, "min_score": 2.15}


def snapshot_payload() -> dict:
    report = json.loads(SNAPSHOT.read_text())
    ranked = report["top"]
    selected = [item for item in ranked if item["score"] >= INFLECTION_PROFILE["min_score"]][: INFLECTION_PROFILE["max_names"]]
    investable = round((1 - INFLECTION_PROFILE["cash"]) * 100)
    total_score = sum(max(item["score"], 0.01) for item in selected) or 1
    allocations = []
    used = 0
    for item in selected:
        weight = min(
            round(INFLECTION_PROFILE["max_weight"] * 100),
            round(investable * max(item["score"], 0.01) / total_score),
        )
        if weight <= 0:
            continue
        allocations.append(
            {
                "symbol": item["symbol"],
                "weight": weight,
                "industry": item.get("industry", "Unknown"),
                "score": round(item["score"], 2),
            }
        )
        used += weight
    if investable - used > 0:
        allocations.append({"symbol": "QQQ", "weight": investable - used, "industry": "Core sleeve", "score": None})
    plan = [
        {"symbol": item["symbol"], "action": "Buy / add to target", "tone": "buy"}
        for item in allocations
        if item["symbol"] != "QQQ"
    ]
    return {
        "allocations": allocations,
        "cash": round(INFLECTION_PROFILE["cash"] * 100),
        "candidates": ranked,
        "date": report["date"],
        "engine": "Inflection Balanced + Trend Guard",
        "industryBreadth": report.get("industry_breadth", {}),
        "mode": "inflection-balanced",
        "plan": plan,
        "ranked": ranked,
        "signals": {"spy63": None, "spy126": None, "qqq63": None, "qqq126": None},
        "source": "research-snapshot",
        "state": "Inflection",
        "stateDetail": "Public snapshot mode is active. The local app can run live Alpaca scans; this deployment shows the latest approved research scan.",
        "timestamp": int(time.time()),
        "trendGuard": False,
        "universeCount": report["universe_size"],
    }


class handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        payload = snapshot_payload()
        data = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "s-maxage=300, stale-while-revalidate=3600")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
