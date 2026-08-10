#!/usr/bin/env bash
# NomaanOS Systemd Daemon Configuration
# Author: Nomaan Khan (IHFC - IIT Delhi)

set -e

echo "============================================================"
echo "    CREATING NOMAANOS SYSTEMD BACKGROUND SERVICES          "
echo "============================================================"

# 1. CREATE REST API DAEMON SERVICE
sudo bash -c 'cat << SERVICE_EOF > /etc/systemd/system/nomaanos-api.service
[Unit]
Description=NomaanOS Core REST API Gateway Daemon
After=network.target ollama.service

[Service]
Type=simple
User='$USER'
WorkingDirectory='$HOME'/workspace/NomaanOS-Core_recovery_final
ExecStart='$HOME'/workspace/NomaanOS-Core_recovery_final/venv/bin/python3 '$HOME'/workspace/NomaanOS-Core_recovery_final/api.py
Restart=always
RestartSec=3
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
SERVICE_EOF'

echo "[+] Systemd service file created at /etc/systemd/system/nomaanos-api.service"

# 2. RELOAD & ENABLE SERVICE
sudo systemctl daemon-reload
sudo systemctl enable nomaanos-api.service
sudo systemctl restart nomaanos-api.service

echo "============================================================"
echo "    [SUCCESS] NOMAANOS REST API DAEMON IS LIVE ON BOOT!    "
echo "============================================================"
