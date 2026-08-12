import re
import sys
import os
import json
import hashlib
import datetime
import fcntl

LEDGER_FILE = os.path.join(os.path.dirname(__file__), "data", "evidence_ledger.json")

# Pre-compiled Blacklist Patterns for High Performance
RAW_PATTERNS = [
    r"rm\s+-rf",                        # Destructive filesystem operations
    r"/etc/passwd",                     # Sensitive Linux file access
    r"aWdub3Jl",                        # Base64 'ignore' (obfuscation evasion)
    r"curl\s+http",                     # Data exfiltration attempts
    r"IGNORE\s+ALL\s+INSTRUCTIONS",     # Direct prompt injection
    r";\s*import\s+os",                 # Python shell escape
    r"PROMPT\s+OVERRIDE"                # Role hijacking
]

COMPILED_PATTERNS = [re.compile(pattern, re.IGNORECASE) for pattern in RAW_PATTERNS]

def inspect_payload(payload_text):
    start_time = datetime.datetime.now()
    is_threat = False
    matched_rule = None

    for idx, compiled_re in enumerate(COMPILED_PATTERNS):
        if compiled_re.search(payload_text):
            is_threat = True
            matched_rule = RAW_PATTERNS[idx]
            break

    latency_ms = (datetime.datetime.now() - start_time).total_seconds() * 1000

    log_entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S IST"),
        "payload": payload_text,
        "action": "BLOCKED" if is_threat else "ALLOWED",
        "matched_pattern": matched_rule,
        "latency_ms": round(latency_ms, 3)
    }

    entry_bytes = json.dumps(log_entry, sort_keys=True).encode('utf-8')
    log_entry["entry_sha256"] = hashlib.sha256(entry_bytes).hexdigest()

    # Ensure target directory exists
    os.makedirs(os.path.dirname(LEDGER_FILE), exist_ok=True)

    # Thread-Safe File Locking Write Execution
    try:
        with open(LEDGER_FILE, "a+") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.seek(0)
            content = f.read().strip()
            if content:
                try:
                    ledger = json.loads(content)
                except Exception:
                    ledger = []
            else:
                ledger = []
            
            ledger.append(log_entry)
            
            f.seek(0)
            f.truncate()
            json.dump(ledger, f, indent=4)
            f.flush()
            fcntl.flock(f, fcntl.LOCK_UN)
    except Exception as e:
        print(f"⚠️ [SENTINEL LEDGER ERROR] Could not log entry: {e}")

    return is_threat, log_entry

if __name__ == "__main__":
    test_payload = sys.argv[1] if len(sys.argv) > 1 else "ls -la"
    blocked, audit = inspect_payload(test_payload)
    print(f"Payload: {test_payload} | Blocked: {blocked} | Hash: {audit['entry_sha256'][:16]}...")
