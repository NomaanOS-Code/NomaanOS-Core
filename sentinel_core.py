import re, sys, os, json, hashlib, datetime

# Real Security Audit Log Directory
LOG_DIR = "data"
os.makedirs(LOG_DIR, exist_ok=True)
LEDGER_FILE = os.path.join(LOG_DIR, "evidence_ledger.json")

# Dangerous Execution Patterns (Real Filtering Schema)
BLACKLIST_PATTERNS = [
    r"rm\s+-rf",                        # Destructive command
    r"/etc/passwd",                     # Sensitive file read
    r"aWdub3Jl",                        # Base64 encoded 'ignore'
    r"curl\s+http",                     # Outbound data exfiltration
    r"IGNORE\s+ALL\s+INSTRUCTIONS",     # Direct Prompt Injection
    r";\s*import\s+os",                 # Python Shell Escape
    r"PROMPT\s+OVERRIDE"                # Role Hijacking
]

def inspect_payload(payload_text):
    """Real Deterministic Security Logic Gate"""
    start_time = datetime.datetime.now()
    
    is_threat = False
    matched_rule = None

    for pattern in BLACKLIST_PATTERNS:
        if re.search(pattern, payload_text, re.IGNORECASE):
            is_threat = True
            matched_rule = pattern
            break
            
    latency_ms = (datetime.datetime.now() - start_time).total_seconds() * 1000

    # Log to Real Evidence Ledger
    log_entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S IST"),
        "payload": payload_text,
        "action": "BLOCKED" if is_threat else "ALLOWED",
        "matched_pattern": matched_rule,
        "latency_ms": round(latency_ms, 3)
    }

    # Hash the entry (Real SHA-256)
    entry_bytes = json.dumps(log_entry).encode('utf-8')
    log_entry["entry_sha256"] = hashlib.sha256(entry_bytes).hexdigest()

    # Append to Ledger
    ledger = []
    if os.path.exists(LEDGER_FILE):
        try:
            with open(LEDGER_FILE, "r") as f:
                ledger = json.load(f)
        except Exception:
            ledger = []
    
    ledger.append(log_entry)
    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=4)

    return is_threat, log_entry

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 sentinel_core.py \"<command_or_prompt>\"")
        sys.exit(1)

    input_text = " ".join(sys.argv[1:])
    is_blocked, audit = inspect_payload(input_text)

    if is_blocked:
        print(f"\n\033[91m[403 FORBIDDEN - AEGIS SENTINEL BLOCK]\033[0m")
        print(f"Rule Matched : {audit['matched_pattern']}")
        print(f"Latency      : {audit['latency_ms']} ms")
        print(f"Audit SHA256 : {audit['entry_sha256'][:16]}...")
        sys.exit(1)
    else:
        print(f"\n\033[92m[200 OK - PASSED INTEGRITY GATE]\033[0m")
        print(f"Latency      : {audit['latency_ms']} ms")
        sys.exit(0)
