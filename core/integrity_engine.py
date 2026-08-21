import os
import sys
import json
import hmac
import hashlib
from datetime import datetime

MANIFEST_FILE = "data/INTEGRITY.manifest.json"

TARGET_FILES = [
    "core/sentinel_core.py",
    "core/nomaan_ai.py",
    "core/api.py",
    "core/rag_engine.py",
    "core/nos_exec.py",
    "tests/stress_test.py",
    "tests/redteam_advanced.py"
]


def _get_signing_secret() -> str:
    """
    Load the HMAC secret from the environment ONLY — never hardcode it in
    source. Locally: export NOMAANOS_INTEGRITY_SECRET=<value> in your shell,
    or put it in a .env file that is in .gitignore (never committed).
    In CI: set it as a GitHub Actions encrypted repository secret, scoped
    so fork-originated pull_request workflows cannot read it.
    """
    secret = os.environ.get("NOMAANOS_INTEGRITY_SECRET")
    if not secret:
        print("\033[1;31m⚠️ [CONFIG ERROR] NOMAANOS_INTEGRITY_SECRET env var is not "
              "set. Refusing to sign or verify without a secret.\033[0m")
        sys.exit(2)
    return secret


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
    secret = _get_signing_secret()
    manifest = {"files": {}, "signed_at": datetime.now().isoformat()}
    print("\033[1;34m[INTEGRITY ENGINE]\033[0m Computing SHA-256 & HMAC Signature for core modules...")

    for filename in TARGET_FILES:
        if os.path.exists(filename):
            file_hash = calculate_sha256(filename)
            manifest["files"][filename] = file_hash
            print(f"  ✓ {filename:<25} SHA-256: {file_hash[:16]}...")
        else:
            print(f"  \033[1;33m⚠️  {filename:<25} not found — skipping\033[0m")

    manifest_str = json.dumps(manifest["files"], sort_keys=True)
    manifest["hmac_signature"] = hmac.new(secret.encode(), manifest_str.encode(), hashlib.sha256).hexdigest()

    os.makedirs("data", exist_ok=True)
    with open(MANIFEST_FILE, "w") as f:
        json.dump(manifest, f, indent=4)

    print(f"\033[1;32m✅ Signed Cryptographic Manifest generated -> {MANIFEST_FILE}\033[0m")


def verify_repository() -> bool:
    """
    Loads the EXISTING committed manifest, recomputes live hashes for
    TARGET_FILES right now, and confirms:
      1. The manifest's own HMAC signature is valid (detects manifest tampering)
      2. Live file hashes match what the manifest recorded (detects source tampering)
    This is the check that was MISSING before — the old script only ever
    re-signed whatever was checked out and always exited 0.
    """
    secret = _get_signing_secret()

    if not os.path.exists(MANIFEST_FILE):
        print(f"\033[1;31m🛑 [INTEGRITY FAIL] No manifest at {MANIFEST_FILE}. "
              f"Repository is unsigned — run 'sign' first.\033[0m")
        return False

    with open(MANIFEST_FILE) as f:
        recorded = json.load(f)

    recorded_files = recorded.get("files", {})
    recorded_signature = recorded.get("hmac_signature", "")

    manifest_str = json.dumps(recorded_files, sort_keys=True)
    expected_signature = hmac.new(secret.encode(), manifest_str.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(expected_signature, recorded_signature):
        print("\033[1;31m🛑 [INTEGRITY FAIL] Manifest HMAC signature is INVALID — "
              "manifest was tampered with, or signed with a different secret.\033[0m")
        return False
    print("\033[1;32m✓\033[0m Manifest HMAC signature valid.")

    all_match = True
    for filename in TARGET_FILES:
        live_hash = calculate_sha256(filename)
        recorded_hash = recorded_files.get(filename)
        if recorded_hash is None:
            print(f"\033[1;33m⚠️  {filename:<25} not in signed manifest — skipping\033[0m")
            continue
        if live_hash != recorded_hash:
            all_match = False
            print(f"\033[1;31m🛑 [TAMPER DETECTED] {filename}\033[0m")
            print(f"     Signed: {recorded_hash}")
            print(f"     Live  : {live_hash}")
        else:
            print(f"\033[1;32m✓\033[0m {filename:<25} matches signed manifest")

    if not all_match:
        print("\033[1;31m🛑 [INTEGRITY FAIL] File(s) do not match signed manifest.\033[0m")
        return False

    print("\033[1;32m✅ [INTEGRITY OK] All files match signed manifest.\033[0m")
    return True


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "verify"
    if mode == "sign":
        sign_repository()
    elif mode == "verify":
        sys.exit(0 if verify_repository() else 1)
    else:
        print("Usage: python3 core/integrity_engine.py [sign|verify]")
        sys.exit(2)
