def get_recovery_status(score):
    if score >= 80:
        return "Green - train hard"
    elif score >= 60:
        return "Yellow - train moderately"
    else:
        return "Red - rest"


def summarize_day(day):
    status = get_recovery_status(day["recovery"])
    print("Date:", day["date"])
    print("Recovery:", day["recovery"], "%")
    print("HRV:", day["hrv"], "ms")
    print("Resting HR:", day["resting_hr"], "bpm")
    print("Status:", status)
    print("---")


# Simulated days using real Whoop metric names
days = [
    {"date": "2024-01-01", "recovery": 82, "hrv": 68, "resting_hr": 52},
    {"date": "2024-01-02", "recovery": 65, "hrv": 55, "resting_hr": 58},
    {"date": "2024-01-03", "recovery": 45, "hrv": 42, "resting_hr": 63},
]

for day in days:
    summarize_day(day)