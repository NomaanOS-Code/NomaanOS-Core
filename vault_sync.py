import os, shutil, glob

VAULT_BASE = os.path.expanduser("~/iSH/00_NOMAANOS_OFFICIAL_VAULT")
if not os.path.exists(VAULT_BASE):
    os.makedirs(VAULT_BASE, exist_ok=True)

# Define Dedicated Directories
DOCS_DIR = os.path.join(VAULT_BASE, "01_HUMAN_READABLE_DOCS")
LOGS_DIR = os.path.join(VAULT_BASE, "02_DAILY_WORK_LOGS")
SIGS_DIR = os.path.join(VAULT_BASE, "03_DIGITAL_SIGNATURES")

for d in [DOCS_DIR, LOGS_DIR, SIGS_DIR]:
    os.makedirs(d, exist_ok=True)

# 1. Sync Human Readable Documents (.pdf, .md, LINKEDIN txt, WHITEPAPER)
doc_patterns = ["*.pdf", "*.md", "LINKEDIN_SHOWCASE_POST.txt", "NomaanOS_*.txt"]
for pattern in doc_patterns:
    for filepath in glob.glob(pattern):
        if os.path.isfile(filepath):
            shutil.copy2(filepath, DOCS_DIR)

# 2. Sync Work Logs
if os.path.exists("work_hours.json"):
    shutil.copy2("work_hours.json", LOGS_DIR)

# 3. Sync Signatures & Manifest
if os.path.exists("INTEGRITY.manifest.json"):
    shutil.copy2("INTEGRITY.manifest.json", SIGS_DIR)

print("✅ Vault Organised & Synced Successfully!")
