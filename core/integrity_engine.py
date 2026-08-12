import os
import sys
import json
import hashlib
from datetime import datetime

MANIFEST_FILE = "INTEGRITY.manifest.json"

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
    manifest = {}
    print("\033[1;34m[INTEGRITY ENGINE]\033[0m Computing cryptographic manifest for core modules...")
    
    for filename in TARGET_FILES:
        if os.path.exists(filename):
            file_hash = calculate_sha256(filename)
            manifest[filename] = {
                "hash": file_hash,
                "last_signed": datetime.now().isoformat()
            }
            print(f"  ✓ {filename:<20} SHA-256: {file_hash[:16]}...")

    with open(MANIFEST_FILE, "w") as f:
        json.dump(manifest, f, indent=4)
        
    print(f"\033[1;32m✅ Repository manifest updated -> {MANIFEST_FILE}\033[0m")

if __name__ == "__main__":
    sign_repository()
