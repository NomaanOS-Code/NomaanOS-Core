import os, shutil, glob

VAULT_BASE = os.path.expanduser("~/iSH/00_NOMAANOS_OFFICIAL_VAULT")
DOCS_DIR = os.path.join(VAULT_BASE, "01_HUMAN_READABLE_DOCS")
os.makedirs(DOCS_DIR, exist_ok=True)

patterns = ["*.md", "*.txt", "*.pdf"]
for p in patterns:
    for filepath in glob.glob(p):
        if os.path.isfile(filepath):
            shutil.copy2(filepath, DOCS_DIR)

print("✅ Vault Organised & Synced Successfully!")
