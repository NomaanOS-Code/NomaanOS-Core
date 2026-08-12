import sys
import subprocess
from core.sentinel_core import inspect_payload

def execute_safely(command_str):
    print(f"\033[1;34m[SENTINEL INTERCEPTOR]\033[0m Analyzing command execution intent: '{command_str}'")

    # 1. DETERMINISTIC SECURITY GATE CHECK
    is_blocked, audit = inspect_payload(command_str)

    if is_blocked:
        print(f"\033[1;31m🛑 [403 ACCESS DENIED] Unsafe Command Intercepted!")
        print(f"   Matched Policy Rule : {audit['matched_pattern']}")
        print(f"   Audit Cryptographic Hash : {audit['entry_sha256'][:16]}...\033[0m")
        sys.exit(1)

    # 2. SAFE CONTROLLED SUBPROCESS EXECUTION
    print("\033[1;32m[200 PERMISSION GRANTED]\033[0m Security policies passed. Executing process...\n")
    try:
        result = subprocess.run(
            command_str,
            shell=True,
            text=True,
            capture_output=True,
            timeout=15
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"\033[1;33m[STDERR]: {result.stderr}\033[0m")
            
        sys.exit(result.returncode)

    except subprocess.TimeoutExpired:
        print("\033[1;31m⚠️ [EXECUTION TIMEOUT] Command execution exceeded 15 seconds limit.\033[0m")
        sys.exit(124)
    except Exception as e:
        print(f"\033[1;31m⚠️ [SYSTEM EXEC ERROR] {str(e)}\033[0m")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 nos_exec.py \"<command>\"")
        sys.exit(1)

    cmd = " ".join(sys.argv[1:])
    execute_safely(cmd)
