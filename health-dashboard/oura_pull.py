import requests
import pandas as pd
from datetime import datetime, timedelta

# Load token
token_file = "/Users/ryanhanson/Documents/health-data/oura_token.txt"
with open(token_file, "r") as f:
    token = f.read().strip()

headers = {"Authorization": f"Bearer {token}"}

# Pull from Oura start date to today
start_date = "2024-01-01"
end_date = datetime.today().strftime("%Y-%m-%d")
params = {"start_date": start_date, "end_date": end_date}

# Pull readiness
readiness = requests.get(
    "https://api.ouraring.com/v2/usercollection/daily_readiness",
    headers=headers, params=params
).json()

# Pull sleep
sleep = requests.get(
    "https://api.ouraring.com/v2/usercollection/daily_sleep",
    headers=headers, params=params
).json()

# Pull HRV + RHR from sleep details
sleep_detail = requests.get(
    "https://api.ouraring.com/v2/usercollection/sleep",
    headers=headers, params=params
).json()

# Build readiness DataFrame
df_readiness = pd.DataFrame([{
    "date": d["day"],
    "readiness_score": d["score"]
} for d in readiness["data"]])

# Build sleep DataFrame
df_sleep = pd.DataFrame([{
    "date": d["day"],
    "sleep_score": d["score"]
} for d in sleep["data"]])

# Build HRV + RHR DataFrame
df_hrv = pd.DataFrame([{
    "date": d["day"],
    "hrv": d.get("average_hrv"),
    "resting_hr": d.get("lowest_heart_rate"),
    "deep_sleep_min": round(d.get("deep_sleep_duration", 0) / 60, 1),
    "rem_sleep_min": round(d.get("rem_sleep_duration", 0) / 60, 1),
    "sleep_efficiency": d.get("efficiency"),
    "respiratory_rate": d.get("average_breath")
} for d in sleep_detail["data"]])

# Merge all Oura data on date
df_oura = df_readiness.merge(df_sleep, on="date", how="outer")
df_oura = df_oura.merge(df_hrv, on="date", how="outer")
df_oura["source"] = "oura"
df_oura["date"] = pd.to_datetime(df_oura["date"]).dt.date

# Save
oura_output = "/Users/ryanhanson/Documents/health-data/oura/oura_clean.csv"
df_oura.to_csv(oura_output, index=False)

print(f"=== Oura Data Saved ===")
print(f"Rows: {len(df_oura)}")
print(f"Date range: {df_oura['date'].min()} to {df_oura['date'].max()}")
print(f"Columns: {df_oura.columns.tolist()}")
print(f"Saved to: {oura_output}")
