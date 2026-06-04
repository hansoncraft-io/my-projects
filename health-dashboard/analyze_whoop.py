import csv

whoop_file = "/Users/ryanhanson/Documents/health-data/whoop/physiological_cycles.csv"

rows = []
with open(whoop_file, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

# Collect valid numeric values
recovery_scores = []
hrv_values = []
resting_hr_values = []

for row in rows:
    try:
        recovery_scores.append(float(row["Recovery score %"]))
        hrv_values.append(float(row["Heart rate variability (ms)"]))
        resting_hr_values.append(float(row["Resting heart rate (bpm)"]))
    except ValueError:
        pass  # Skip rows with missing data

# Calculate averages
avg_recovery = sum(recovery_scores) / len(recovery_scores)
avg_hrv = sum(hrv_values) / len(hrv_values)
avg_rhr = sum(resting_hr_values) / len(resting_hr_values)

print("=== Your Whoop Averages ===")
print(f"Average Recovery:    {avg_recovery:.1f}%")
print(f"Average HRV:         {avg_hrv:.1f} ms")
print(f"Average Resting HR:  {avg_rhr:.1f} bpm")

# Find best and worst recovery days
best_day = max(rows, key=lambda r: float(r["Recovery score %"]) if r["Recovery score %"] else 0)
worst_day = min(rows, key=lambda r: float(r["Recovery score %"]) if r["Recovery score %"] else 100)

print("\n=== Best and Worst Days ===")
print(f"Best recovery:  {best_day['Recovery score %']}% on {best_day['Cycle start time'][:10]}")
print(f"Worst recovery: {worst_day['Recovery score %']}% on {worst_day['Cycle start time'][:10]}")

# Find your highest HRV day
best_hrv = max(rows, key=lambda r: float(r["Heart rate variability (ms)"]) if r["Heart rate variability (ms)"] else 0)
print(f"Best HRV:       {best_hrv['Heart rate variability (ms)']} ms on {best_hrv['Cycle start time'][:10]}")

# Count green, yellow, red days
green = sum(1 for s in recovery_scores if s >= 80)
yellow = sum(1 for s in recovery_scores if 60 <= s < 80)
red = sum(1 for s in recovery_scores if s < 60)
total = len(recovery_scores)

print("\n=== Recovery Distribution ===")
print(f"Green days (80+):     {green} ({green/total*100:.1f}%)")
print(f"Yellow days (60-79):  {yellow} ({yellow/total*100:.1f}%)")
print(f"Red days (<60):       {red} ({red/total*100:.1f}%)")

# === Correlation Analysis ===
import csv
from datetime import datetime, timedelta

journal_file = "/Users/ryanhanson/Documents/health-data/whoop/journal_entries.csv"

# Build journal answer lookups by date
alcohol_days = set()
late_food_days = set()
caffeine_days = set()
poor_sleep_screen_days = set()

with open(journal_file, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        question = row["Question text"]
        answered_yes = row["Answered yes"].strip().lower() == "true"
        date = row["Cycle start time"][:10]

        if "alcoholic" in question and answered_yes:
            alcohol_days.add(date)
        if "close to bedtime" in question and answered_yes:
            late_food_days.add(date)
        if "caffeine" in question.lower() and answered_yes:
            caffeine_days.add(date)
        if "non-screened" in question and answered_yes:
            poor_sleep_screen_days.add(date)

def correlate(label, flagged_days, rows):
    flagged = []
    unflagged = []
    for row in rows:
        try:
            date = row["Cycle start time"][:10]
            score = float(row["Recovery score %"])
            if date in flagged_days:
                flagged.append(score)
            else:
                unflagged.append(score)
        except ValueError:
            pass
    if flagged:
        avg_yes = sum(flagged) / len(flagged)
        avg_no = sum(unflagged) / len(unflagged)
        diff = avg_yes - avg_no
        direction = "▼ worse" if diff < 0 else "▲ better"
        print(f"{label}")
        print(f"  Yes: {avg_yes:.1f}%  ({len(flagged)} days)  |  No: {avg_no:.1f}%  ({len(unflagged)} days)  |  {diff:+.1f} pts {direction}")
    else:
        print(f"{label} — no data found")

print("\n=== Lifestyle Correlations vs Recovery ===")
correlate("Alcohol",              alcohol_days,          rows)
correlate("Ate close to bedtime", late_food_days,        rows)
correlate("Caffeine",             caffeine_days,         rows)
correlate("Screen before bed",    poor_sleep_screen_days, rows)