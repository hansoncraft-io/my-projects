import pandas as pd

whoop_file = "/Users/ryanhanson/Documents/health-data/whoop/physiological_cycles.csv"

df = pd.read_csv(whoop_file)

# Rename only the columns we actually care about
# Using Oura-friendly names so they align when we merge later
df = df.rename(columns={
    "Cycle start time": "date",
    "Heart rate variability (ms)": "hrv",
    "Resting heart rate (bpm)": "resting_hr",
    "Sleep performance %": "sleep_efficiency",
    "Deep (SWS) duration (min)": "deep_sleep_min",
    "REM duration (min)": "rem_sleep_min",
    "Respiratory rate (rpm)": "respiratory_rate",
})

# Keep only the 6 overlap metrics + date
core_columns = ["date", "hrv", "resting_hr", "sleep_efficiency",
                "deep_sleep_min", "rem_sleep_min", "respiratory_rate"]

df_clean = df[core_columns].copy()

# Clean date format
df_clean["date"] = pd.to_datetime(df_clean["date"]).dt.date

# Tag the source
df_clean["source"] = "whoop"

# Fill missing values with column median
for col in ["hrv", "resting_hr", "sleep_efficiency",
            "deep_sleep_min", "rem_sleep_min", "respiratory_rate"]:
    df_clean[col] = df_clean[col].fillna(df_clean[col].median())

# Save
output_file = "/Users/ryanhanson/Documents/health-data/whoop/whoop_clean.csv"
df_clean.to_csv(output_file, index=False)

print("=== Whoop Clean Dataset ===")
print(f"Rows: {len(df_clean)}")
print(f"Columns: {df_clean.columns.tolist()}")
print(f"Date range: {df_clean['date'].min()} to {df_clean['date'].max()}")
print(f"Missing values: {df_clean.isnull().sum().sum()}")
print(f"\nSaved to: {output_file}")