import requests
import json

# Load token from file
token_file = "/Users/ryanhanson/Documents/health-data/oura_token.txt"
with open(token_file, "r") as f:
    token = f.read().strip()

# Set up headers
headers = {"Authorization": f"Bearer {token}"}

# Pull last 7 days of readiness data
url = "https://api.ouraring.com/v2/usercollection/daily_readiness"
params = {"start_date": "2026-05-28", "end_date": "2026-06-04"}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    print("=== Oura Readiness Data ===")
    for day in data["data"]:
        print(f"Date: {day['day']}  |  Readiness: {day['score']}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

# Pull sleep data
sleep_url = "https://api.ouraring.com/v2/usercollection/daily_sleep"
sleep_response = requests.get(sleep_url, headers=headers, params=params)

if sleep_response.status_code == 200:
    sleep_data = sleep_response.json()
    print("\n=== Oura Sleep Data ===")
    for day in sleep_data["data"]:
        print(f"Date: {day['day']}  |  Sleep Score: {day['score']}")

# Pull HRV - comes from sleep details
hrv_url = "https://api.ouraring.com/v2/usercollection/sleep"
hrv_response = requests.get(hrv_url, headers=headers, params=params)

if hrv_response.status_code == 200:
    hrv_data = hrv_response.json()
    print("\n=== Oura HRV + Resting HR ===")
    for day in hrv_data["data"]:
        print(f"Date: {day['day']}  |  HRV: {day.get('average_hrv')}  |  RHR: {day.get('lowest_heart_rate')}")