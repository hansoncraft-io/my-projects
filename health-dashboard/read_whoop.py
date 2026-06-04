import csv

whoop_file = "/Users/ryanhanson/Documents/health-data/whoop/physiological_cycles.csv"

rows = []
with open(whoop_file, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

print("Total days of Whoop data:", len(rows))
print("First recorded day:", rows[0]["Cycle start time"])
print("Last recorded day:", rows[-1]["Cycle start time"])