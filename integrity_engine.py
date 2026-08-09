import hashlib, json, datetime, os

MANIFEST_FILE = "INTEGRITY.manifest.json"

def calculate_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def sign_repository():
    manifest = {}
    if os.path.exists(MANIFEST_FILE):
        with open(MANIFEST_FILE, 'r') as f: manifest = json.load(f)

    timestamp = datetime.datetime.now().isoformat()
    files_to_sign = ['api.py', 'stress_test.py', 'redteam_benchmark.json']
    
    for f in files_to_sign:
        if os.path.exists(f):
            h = calculate_sha256(f)
            manifest[f] = {"hash": h, "last_signed": timestamp}
    
    with open(MANIFEST_FILE, 'w') as f:
        json.dump(manifest, f, indent=4)
    print(f"✅ Repository signed at {timestamp}. Manifest updated.")

if __name__ == "__main__":
    sign_repository()
