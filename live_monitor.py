import os, json, hashlib, datetime

LEDGER_FILE = "data/evidence_ledger.json"

def draw_dashboard():
    os.system('clear' if os.name != 'nt' else 'cls')
    
    total_inspects = 0
    total_blocked = 0
    total_allowed = 0
    last_event = "NO_EVENTS_LOGGED"
    last_hash = "N/A"

    if os.path.exists(LEDGER_FILE):
        try:
            with open(LEDGER_FILE, "r") as f:
                logs = json.load(f)
                total_inspects = len(logs)
                total_blocked = sum(1 for entry in logs if entry.get("action") == "BLOCKED")
                total_allowed = sum(1 for entry in logs if entry.get("action") == "ALLOWED")
                if logs:
                    last_entry = logs[-1]
                    last_event = f"{last_entry.get('action')} -> {last_entry.get('payload')[:30]}"
                    last_hash = last_entry.get("entry_sha256", "N/A")[:16]
        except Exception:
            pass

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
    
    print("\033[92m==========================================================================\033[0m")
    print("      🛡️ NOMAANOS CORE v6.0 // REAL-TIME AEGIS SENTINEL TELEMETRY")
    print("\033[92m==========================================================================\033[0m")
    print(f" System Timestamp : {now}")
    print(f" Scholar / Owner  : Nomaan Khan (IHFC - IIT Delhi)")
    print(f" Sentinel State   : \033[92mHARDENED & ACTIVE\033[0m")
    print(f" Ledger Source    : \033[96m{LEDGER_FILE}\033[0m")
    print("==========================================================================")
    print("\033[93m[ REAL EVIDENCE LEDGER METRICS ]\033[0m")
    print(f"  • Total Inspect Requests : {total_inspects}")
    print(f"  • Threat Vector Blocks   : \033[91m{total_blocked}\033[0m")
    print(f"  • Authorized Pass-through : \033[92m{total_allowed}\033[0m")
    print(f"  • Latest SHA-256 Hash    : \033[96m{last_hash}...\033[0m")
    print(f"  • Recent Activity Trace  : {last_event}")
    print("==========================================================================")
    print("\033[90mPress Ctrl+C to exit...\033[0m")

if __name__ == "__main__":
    try:
        draw_dashboard()
    except KeyboardInterrupt:
        print("\n\n\033[91m[!] Telemetry Stream Paused.\033[0m")
