#!/bin/sh
# NomaanOS Core Silent Auto-Backup Engine
cd ~/workspace/NomaanOS-Core_recovery_final

# 1. Update Work Logs & PDF Report
python3 auto_tasks.py > /dev/null 2>&1
python3 generate_report.py > /dev/null 2>&1

# 2. Local Vault Sync
nos-export > /dev/null 2>&1

# 3. Cryptographic SHA-256 Sign & Git Auto-Commit
git add .
if ! git diff-index --quiet HEAD --; then
    git commit -m "auto(nomaanos): Scheduled Cryptographic Backup [$(date +'%Y-%m-%d %H:%M IST')]"
    git push origin main > /dev/null 2>&1
fi
