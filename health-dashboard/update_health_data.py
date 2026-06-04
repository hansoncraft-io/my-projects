import subprocess
import sys
from datetime import datetime

log_file = "/Users/ryanhanson/Documents/health-data/update_log.txt"

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(log_file, "a") as f:
        f.write(f"{timestamp} — {message}\n")
    print(message)

try:
    log("Starting daily health data update...")

    # Step 1 — Pull fresh Oura data
    import requests
    import pandas as pd
    from datetime import datetime, timedelta

    token_file = "/Users/ryanhanson/Documents/health-data/oura_token.txt"
    with open(token_file, "r") as f:
        token = f.read().strip()

    headers = {"Authorization": f"Bearer {token}"}
    start_date = "2024-01-01"
    end_date = datetime.today().strftime("%Y-%m-%d")
    params = {"start_date": start_date, "end_date": end_date}

    readiness = requests.get("https://api.ouraring.com/v2/usercollection/daily_readiness", headers=headers, params=params).json()
    sleep = requests.get("https://api.ouraring.com/v2/usercollection/daily_sleep", headers=headers, params=params).json()
    sleep_detail = requests.get("https://api.ouraring.com/v2/usercollection/sleep", headers=headers, params=params).json()

    df_readiness = pd.DataFrame([{"date": d["day"], "readiness_score": d["score"]} for d in readiness["data"]])
    df_sleep = pd.DataFrame([{"date": d["day"], "sleep_score": d["score"]} for d in sleep["data"]])
    df_hrv = pd.DataFrame([{
        "date": d["day"],
        "hrv": d.get("average_hrv"),
        "resting_hr": d.get("lowest_heart_rate"),
        "deep_sleep_min": round(d.get("deep_sleep_duration", 0) / 60, 1),
        "rem_sleep_min": round(d.get("rem_sleep_duration", 0) / 60, 1),
        "sleep_efficiency": d.get("efficiency"),
        "respiratory_rate": d.get("average_breath")
    } for d in sleep_detail["data"]])

    df_oura = df_readiness.merge(df_sleep, on="date", how="outer")
    df_oura = df_oura.merge(df_hrv, on="date", how="outer")
    df_oura["source"] = "oura"
    df_oura["date"] = pd.to_datetime(df_oura["date"]).dt.date
    df_oura.to_csv("/Users/ryanhanson/Documents/health-data/oura/oura_clean.csv", index=False)
    log(f"Oura data updated — {len(df_oura)} days pulled")

    # Step 2 — Rebuild unified timeline
    df_whoop = pd.read_csv("/Users/ryanhanson/Documents/health-data/whoop/whoop_clean.csv")
    df_whoop["date"] = pd.to_datetime(df_whoop["date"]).dt.date

    overlap_cols = ["date", "source", "hrv", "resting_hr", "sleep_efficiency",
                    "deep_sleep_min", "rem_sleep_min", "respiratory_rate"]
    oura_cols = overlap_cols + ["readiness_score", "sleep_score"]

    df_whoop_slim = df_whoop[overlap_cols].copy()
    df_oura_slim = df_oura[[c for c in oura_cols if c in df_oura.columns]].copy()

    df_unified = pd.concat([df_whoop_slim, df_oura_slim], ignore_index=True)
    df_unified = df_unified.sort_values("date").reset_index(drop=True)
    df_unified = df_unified.drop_duplicates(subset="date", keep="last")
    df_unified.to_csv("/Users/ryanhanson/Documents/health-data/unified_health.csv", index=False)
    log(f"Unified timeline rebuilt — {len(df_unified)} total days")
    log("Update complete ✓")

except Exception as e:
    log(f"ERROR: {str(e)}")