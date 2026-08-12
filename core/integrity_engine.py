import os
import sys
import json
import hmac
import hashlib
from datetime import datetime

MANIFEST_FILE = "data/INTEGRITY.manifest.json"
SIGNING_SECRET = "NOMAANOS_SOVEREIGN_SECRET_KEY_2026"

TARGET_FILES = [
    "core/sentinel_core.py",
    "core/nomaan_ai.py",
    "core/api.py",
    "core/rag_engine.py",
    "core/nos_exec.py",
    "tests/stress_test.py",
    "tests/redteam_advanced.py"
]

def calculate_sha256(filepath):
    if not os.path.exists(filepath):
        return None
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"⚠️ Error hashing {filepath}: {e}")
        return None

def sign_repository():
    manifest = {"files": {}, "signed_at": datetime.now().isoformat()}
    print("\033[1;34m[INTEGRITY ENGINE]\033[0m Computing SHA-256 & HMAC Signature for core modules...")
    
    for filename in TARGET_FILES:
        if os.path.exists(filename):
            file_hash = calculate_sha256(filename)
            manifest["files"][filename] = file_hash
            print(f"  ✓ {filename:<25} SHA-256: {file_hash[:16]}...")

    # HMAC Signing
    manifest_str = json.dumps(manifest["files"], sort_keys=True)
    signature = hmac.new(SIGNING_SECRET.encode(), manifest_str.encode(), hashlib.sha256).hexdigest()
    manifest["hmac_signature"] = signature

    os.makedirs("data", exist_ok=True)
    with open(MANIFEST_FILE, "w") as f:
        json.dump(manifest, f, indent=4)
        
    print(f"\033[1;32m✅ Signed Cryptographic Manifest generated -> {MANIFEST_FILE}\033[0m")

if __name__ == "__main__":
    sign_repository()
