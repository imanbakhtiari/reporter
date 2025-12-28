from flask import Flask, request, jsonify
import csv
import re
from collections import defaultdict
from datetime import datetime

CSV_FILE = "Provider_ascii_1.csv"

app = Flask(__name__)

rows = []

DATA_REGEX = re.compile(
    r"Symbol:\s*(\w+)\s+Seqno:\s*(\d+)\s+Price:\s*(\d+)"
)

def human(ts):
    return datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


with open(CSV_FILE, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        match = DATA_REGEX.search(row.get("data", ""))
        if not match:
            continue

        symbol, seqno, price = match.groups()

        rows.append({
            "symbol": symbol,
            "seqno": int(seqno),
            "provider": row["ip.src"].strip(),
            "timestamp": float(row["frame.time_epoch"])
        })


@app.route("/sorting")
def sorting():
    seqno = request.args.get("seqno", type=int)
    if seqno is None:
        return jsonify({"error": "seqno is required"}), 400

    data = [r for r in rows if r["seqno"] == seqno]
    if not data:
        return jsonify({"error": "seqno not found"}), 404

    data.sort(key=lambda x: x["timestamp"])

    fastest = data[0]
    slowest = data[-1]
    avg_ts = sum(d["timestamp"] for d in data) / len(data)

    return jsonify({
        "seqno": seqno,
        "symbol": fastest["symbol"],
        "fastest_provider": fastest["provider"],
        "fastest_timestamp": human(fastest["timestamp"]),
        "slowest_provider": slowest["provider"],
        "slowest_timestamp": human(slowest["timestamp"]),
        "average_timestamp": human(avg_ts),
        "sorted_by_arrival": [
            {
                "provider": d["provider"],
                "timestamp": human(d["timestamp"])
            }
            for d in data
        ]
    })


@app.route("/ranking")
def ranking():
    by_seqno = defaultdict(list)
    for r in rows:
        by_seqno[r["seqno"]].append(r)

    win = defaultdict(int)
    total_time = defaultdict(float)
    count = defaultdict(int)

    for packets in by_seqno.values():
        packets.sort(key=lambda x: x["timestamp"])
        win[packets[0]["provider"]] += 1
        for p in packets:
            total_time[p["provider"]] += p["timestamp"]
            count[p["provider"]] += 1

    ranking = []
    for provider in count:
        avg_ts = total_time[provider] / count[provider]
        ranking.append({
            "provider": provider,
            "fastest_count": win.get(provider, 0),
            "average_timestamp": human(avg_ts)
        })

    ranking.sort(key=lambda x: -x["fastest_count"])

    return jsonify({
        "best_providers_to_keep": [
            ranking[0]["provider"],
            ranking[1]["provider"]
        ],
        "ranking": ranking
    })


if __name__ == "__main__":
    app.run(debug=True)

