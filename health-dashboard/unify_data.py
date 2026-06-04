import pandas as pd

# Load both datasets
whoop_file = "/Users/ryanhanson/Documents/health-data/whoop/whoop_clean.csv"
oura_file = "/Users/ryanhanson/Documents/health-data/oura/oura_clean.csv"

df_whoop = pd.read_csv(whoop_file)
df_oura = pd.read_csv(oura_file)

# Ensure dates are the same type
df_whoop["date"] = pd.to_datetime(df_whoop["date"]).dt.date
df_oura["date"] = pd.to_datetime(df_oura["date"]).dt.date

# Shared overlap columns only
overlap_cols = ["date", "source", "hrv", "resting_hr",
                "sleep_efficiency", "deep_sleep_min",
                "rem_sleep_min", "respiratory_rate"]

# Keep only overlap columns from Whoop
df_whoop_slim = df_whoop[overlap_cols].copy()

# Keep overlap + Oura-only columns
oura_cols = overlap_cols + ["readiness_score", "sleep_score"]
df_oura_slim = df_oura[[c for c in oura_cols if c in df_oura.columns]].copy()

# Stack them — Whoop history on bottom, Oura on top
df_unified = pd.concat([df_whoop_slim, df_oura_slim], ignore_index=True)
df_unified = df_unified.sort_values("date").reset_index(drop=True)

# Remove any date overlap — prefer Oura where both exist
df_unified = df_unified.drop_duplicates(subset="date", keep="last")

# Save
output_file = "/Users/ryanhanson/Documents/health-data/unified_health.csv"
df_unified.to_csv(output_file, index=False)

print("=== Unified Health Timeline ===")
print(f"Total days: {len(df_unified)}")
print(f"Date range: {df_unified['date'].min()} to {df_unified['date'].max()}")
print(f"\nWhoop days: {len(df_unified[df_unified['source'] == 'whoop'])}")
print(f"Oura days:  {len(df_unified[df_unified['source'] == 'oura'])}")
print(f"\nColumns: {df_unified.columns.tolist()}")
print(f"\nSaved to: {output_file}")

# Spot check — show first and last 3 rows
print("\n=== First 3 rows (Whoop history) ===")
print(df_unified.head(3).to_string(index=False))

print("\n=== Last 3 rows (Oura live) ===")
print(df_unified.tail(3).to_string(index=False))