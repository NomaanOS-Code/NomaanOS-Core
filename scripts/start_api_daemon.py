import subprocess, time, os, urllib.request

def is_port_open():
    try:
        with urllib.request.urlopen("http://localhost:8080/validate", timeout=1) as response:
            return True
    except Exception:
        return False

# Start background process if not already running
if not is_port_open():
    print("\033[94m[NOMAANOS DAEMON]\033[0m Starting Real REST API Server on Port 8080...")
    subprocess.Popen(["python3", "api.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.5)
    print("\033[92m[ACTIVE]\033[0m API Background Server is up and listening!")
else:
    print("\033[92m[ACTIVE]\033[0m API Server is already running on Port 8080!")
