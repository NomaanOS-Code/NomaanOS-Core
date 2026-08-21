import sys
import shlex
import subprocess
from pathlib import Path
from core.sentinel_core import inspect_payload

ALLOWED_BINARIES = {
    "ls": "/usr/bin/ls",
    "cat": "/usr/bin/cat",
    "grep": "/usr/bin/grep",
    "echo": "/usr/bin/echo",
    "python3": "/usr/bin/python3",
    "git": "/usr/bin/git",
    "pwd": "/usr/bin/pwd"
}

def execute_safely(command_str):
    print(f"\033[1;34m[SENTINEL INTERCEPTOR]\033[0m Analyzing command execution intent: '{command_str}'")

    # 1. DETERMINISTIC SECURITY GATE CHECK
    is_blocked, audit = inspect_payload(command_str)
    if is_blocked:
        print(f"\033[1;31m🛑 [403 ACCESS DENIED] Unsafe Command Intercepted!")
        print(f"   Matched Policy Rule : {audit['matched_pattern']}")
        print(f"   Audit Cryptographic Hash : {audit['entry_sha256'][:16]}...\033[0m")
        sys.exit(1)

    # 2. SAFE ARGUMENT PARSING (NO SHELL INTERPRETATION)
    try:
        args = shlex.split(command_str)
    except Exception as e:
        print(f"\033[1;31m⚠️ [SHELL PARSE ERROR] Malformed shell command input: {e}\033[0m")
        sys.exit(1)

    if not args:
        print("\033[1;31m⚠️ [EMPTY COMMAND] No command provided.\033[0m")
        sys.exit(1)

    cmd_binary = args[0]

    # 3. ALLOWLIST ENFORCEMENT (fail closed — no fallback to raw command name)
    if cmd_binary not in ALLOWED_BINARIES:
        print(f"\033[1;31m🛑 [403 NOT ALLOWLISTED] Binary '{cmd_binary}' is not in ALLOWED_BINARIES.\033[0m")
        sys.exit(1)

    binary_path = Path(ALLOWED_BINARIES[cmd_binary]).resolve()
    if not binary_path.is_file():
        print(f"\033[1;31m⚠️ [BINARY MISSING] Allowlisted binary not found on disk: {binary_path}\033[0m")
        sys.exit(1)

    # 4. PATH TRAVERSAL GUARD IN ARGUMENTS (resolved-path based, not substring-based)
    SENSITIVE_ROOTS = ["/etc", "/proc", "/root", "/sys", "/boot", "/home"]
    for arg in args[1:]:
        if arg.startswith("-"):
            continue  # flags like -la, --version are not paths
        candidate = Path(arg)
        if not candidate.is_absolute():
            candidate = Path.cwd() / candidate
        try:
            resolved = candidate.resolve()
        except (OSError, RuntimeError):
            print(f"\033[1;31m🛑 [PATH RESOLUTION ERROR] Could not resolve argument: {arg}\033[0m")
            sys.exit(1)
        if any(str(resolved) == root or str(resolved).startswith(root + "/") for root in SENSITIVE_ROOTS):
            print(f"\033[1;31m🛑 [PATH TRAVERSAL BLOCKED] Resolved path hits sensitive root: {resolved}\033[0m")
            sys.exit(1)

    # 5. HARDENED SUBPROCESS EXECUTION (shell=False, resolved absolute binary path)
    print("\033[1;32m[200 PERMISSION GRANTED]\033[0m Security policies passed. Executing binary via execve()...\n")
    try:
        exec_args = [str(binary_path)] + args[1:]  # use the RESOLVED absolute path, not the raw name
        result = subprocess.run(
            exec_args,         # List form -> direct execve(), NO /bin/sh invocation!
            shell=False,       # CRITICAL FAANG MANDATE: NEVER SHELL=TRUE
            text=True,
            capture_output=True,
            timeout=15,
            env={"PATH": "/usr/bin:/bin"}
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
        print("Usage: python3 core/nos_exec.py \"<command>\"")
        sys.exit(1)

    cmd = " ".join(sys.argv[1:])
    execute_safely(cmd)
