import pandas as pd

whoop_file = "/Users/ryanhanson/Documents/health-data/whoop/physiological_cycles.csv"

df = pd.read_csv(whoop_file)

# Rename key columns for easier access
df = df.rename(columns={
    "Recovery score %": "recovery",
    "Heart rate variability (ms)": "hrv",
    "Resting heart rate (bpm)": "resting_hr",
    "Sleep performance %": "sleep_perf",
    "Deep (SWS) duration (min)": "deep_sleep",
    "REM duration (min)": "rem_sleep",
    "Cycle start time": "date"
})

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Instant stats
print("=== Recovery ===")
print(df["recovery"].describe().round(1))

print("\n=== HRV ===")
print(df["hrv"].describe().round(1))

# Your green days only
green_days = df[df["recovery"] >= 80]
print(f"\nGreen days: {len(green_days)}")
print(f"Avg HRV on green days: {green_days['hrv'].mean():.1f} ms")
print(f"Avg HRV on red days:   {df[df['recovery'] < 60]['hrv'].mean():.1f} ms")

# Best 10 recovery days
print("\n=== Your Top 10 Recovery Days ===")
top10 = df.nlargest(10, "recovery")[["date", "recovery", "hrv", "resting_hr"]]
print(top10.to_string(index=False))