import pandas as pd

whoop_file = "/Users/ryanhanson/Documents/health-data/whoop/physiological_cycles.csv"

df = pd.read_csv(whoop_file)

# Rename key columns
df = df.rename(columns={
    "Recovery score %": "recovery",
    "Heart rate variability (ms)": "hrv",
    "Resting heart rate (bpm)": "resting_hr",
    "Sleep performance %": "sleep_perf",
    "Deep (SWS) duration (min)": "deep_sleep",
    "REM duration (min)": "rem_sleep",
    "Cycle start time": "date"
})

# Check for missing values
print("=== Missing Values Per Column ===")
print(df.isnull().sum())
print(f"\nTotal rows: {len(df)}")

# Convert date to proper datetime and extract just the date
df["date"] = pd.to_datetime(df["date"]).dt.date

# Add a source column — important for when we merge with Oura
df["source"] = "whoop"

print("\n=== Date Range ===")
print("First day:", df["date"].min())
print("Last day: ", df["date"].max())
print("Total days:", len(df))

# Keep only the columns that matter for the dashboard
core_columns = ["date", "source", "recovery", "hrv", "resting_hr",
                "sleep_perf", "deep_sleep", "rem_sleep"]

df_clean = df[core_columns].copy()

# Fill missing numeric values with column median
# Median is better than mean for health data — less affected by outlier days
for col in ["recovery", "hrv", "resting_hr", "sleep_perf", "deep_sleep", "rem_sleep"]:
    median_val = df_clean[col].median()
    missing_count = df_clean[col].isnull().sum()
    if missing_count > 0:
        print(f"Filling {missing_count} missing values in {col} with median: {median_val:.1f}")
    df_clean[col] = df_clean[col].fillna(median_val)

print("\n=== Clean Dataset ===")
print(f"Rows: {len(df_clean)}")
print(f"Columns: {df_clean.columns.tolist()}")
print(f"Missing values remaining: {df_clean.isnull().sum().sum()}")

# Save cleaned Whoop data to a new file
output_file = "/Users/ryanhanson/Documents/health-data/whoop/physiological_cycles_clean.csv"
df_clean.to_csv(output_file, index=False)

print(f"\nClean file saved to: {output_file}")
print("Ready to merge with Oura data.")