import xml.etree.ElementTree as ET
from datetime import datetime
import csv
import json
import os

TCX_FILE = "../data/Match3.tcx"
CSV_FILE = "../output/heart_rate_data.csv"
JSON_FILE = "../output/heart_rate_data.json"

NS = {
    "tcx": "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"
}

def parse_time(t):
    return datetime.fromisoformat(t.replace("Z", "+00:00"))

# 🔥 format temps lisible
def format_time(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h > 0:
        return f"{h}h {m:02d}m {s:02d}s"
    return f"{m:02d}m {s:02d}s"

def main():
    if not os.path.exists(TCX_FILE):
        print(f"Erreur : fichier introuvable -> {TCX_FILE}")
        return

    os.makedirs("../output", exist_ok=True)

    tree = ET.parse(TCX_FILE)
    root = tree.getroot()

    trackpoints = root.findall(".//tcx:Trackpoint", NS)

    data = []
    start_time = None

    for tp in trackpoints:
        time_el = tp.find("tcx:Time", NS)
        hr_el = tp.find("tcx:HeartRateBpm/tcx:Value", NS)

        if time_el is None or hr_el is None:
            continue

        try:
            current_time = parse_time(time_el.text)
            heart_rate = int(hr_el.text)
        except Exception:
            continue

        if start_time is None:
            start_time = current_time

        elapsed_seconds = int((current_time - start_time).total_seconds())

        data.append({
            "t": elapsed_seconds,
            "bpm": heart_rate
        })

    if not data:
        print("Aucune donnée fréquence cardiaque trouvée dans le fichier.")
        return

    # 🔥 durée totale du match
    duration = data[-1]["t"]

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["t", "bpm"])
        writer.writeheader()
        writer.writerows(data)

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Extraction terminée : {len(data)} points")
    print(f"⏱ Durée du match : {format_time(duration)}")
    print(f"CSV créé : {CSV_FILE}")
    print(f"JSON créé : {JSON_FILE}")

if __name__ == "__main__":
    main()