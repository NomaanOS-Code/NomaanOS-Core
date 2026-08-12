import json, datetime, os

LOG_FILE = "work_hours.json"
today = datetime.datetime.now().strftime("%Y-%m-%d")

# Master Daily Recurring Tasks Checklist
DAILY_MASTER_TASKS = [
    "[CRITICAL] Run NomaanOS Integrity Audit & SHA-256 Sign",
    "[CORE] Sync Vault to iPad Files App (nos-export)",
    "[RESEARCH] Scholar Work Log @ IHFC IIT Delhi",
    "[SECURITY] Check Red-Team Benchmark & Gateway Telemetry"
]

data = {}
if os.path.exists(LOG_FILE):
    try:
        with open(LOG_FILE, "r") as f: data = json.load(f)
    except: pass

if today not in data:
    data[today] = {
        "date": today,
        "hours_logged": "0.0 Hours (In Progress)",
        "status": "PENDING",
        "tasks": DAILY_MASTER_TASKS,
        "last_updated": datetime.datetime.now().strftime("%I:%M %p IST")
    }
    with open(LOG_FILE, "w") as f: json.dump(data, f, indent=4)
    print(f"✅ Daily Auto-Tasks Generated for {today}!")
else:
    print(f"ℹ️ Today's Task Sheet Active: {data[today]['status']}")
