import sys, os, subprocess
from sentinel_core import inspect_payload

def execute_safely(command_str):
    print(f"\n\033[94m[SENTINEL INTERCEPTOR]\033[0m Analyzing command: '{command_str}'")
    is_blocked, audit = inspect_payload(command_str)
    
    if is_blocked:
        print(f"\033[91m[403 ACCESS DENIED]\033[0m Blocked Rule: {audit['matched_pattern']}")
        print(f"Cryptographic Hash Logged: {audit['entry_sha256'][:16]}...")
        sys.exit(1)
        
    print(f"\033[92m[200 PERMISSION GRANTED]\033[0m Executing shell process...\n")
    subprocess.run(command_str, shell=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 nos_exec.py \"<shell_command>\"")
        sys.exit(1)
        
    cmd = " ".join(sys.argv[1:])
    execute_safely(cmd)
