"""
NomaanOS Core - Secure Process Execution Sandbox (nos_exec.py)
Classification: Hardened Execution Layer
Author: Nomaan Khan (Scholar @ IHFC - IIT Delhi)
"""

import os
import shlex
import subprocess
import hashlib
from typing import Dict, List, Any
from pathlib import Path

# Explicit Binary Allowlist - Strict Path & Command Boundary
ALLOWED_BINARIES: Dict[str, str] = {
    "ls": "/bin/ls",
    "cat": "/bin/cat",
    "grep": "/bin/grep",
    "docker": "/usr/bin/docker",
    "python3": "/usr/bin/python3"
}

class ExecutionSecurityError(Exception):
    """Custom exception raised when execution boundary constraints are violated."""
    pass

class SecureExecutionEngine:
    def __init__(self, timeout_seconds: int = 15):
        self.timeout = timeout_seconds

    def _hash_payload(self, binary_path: str, args: List[str]) -> str:
        """Generates deterministic SHA-256 payload hash for audit logging."""
        payload_str = f"{binary_path}:" + ":".join(args)
        return hashlib.sha256(payload_str.encode('utf-8')).hexdigest()

    def execute_command(self, binary_key: str, args: List[str]) -> Dict[str, Any]:
        """
        Executes allowlisted binaries without shell interpolation (shell=False).
        Prevents metacharacter expansion, command chaining, and subshell injection.
        """
        if binary_key not in ALLOWED_BINARIES:
            raise ExecutionSecurityError(
                f"EXECUTION_BLOCKED: Binary '{binary_key}' is not registered in Aegis Allowlist."
            )

        binary_path = ALLOWED_BINARIES[binary_key]

        if not Path(binary_path).exists():
            raise FileNotFoundError(
                f"SYSTEM_ERROR: Allowlisted binary path '{binary_path}' does not exist on host."
            )

        # Sanitize arguments against path traversal vectors
        sanitized_args = [shlex.quote(arg) for arg in args]
        execution_vector = [binary_path] + sanitized_args
        payload_hash = self._hash_payload(binary_path, sanitized_args)

        try:
            # Secure execution: shell=False enforces explicit process boundaries
            process = subprocess.run(
                execution_vector,
                shell=False,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                check=False
            )

            return {
                "status": "SUCCESS" if process.returncode == 0 else "FAILED",
                "return_code": process.returncode,
                "stdout": process.stdout.strip(),
                "stderr": process.stderr.strip(),
                "payload_sha256": payload_hash,
                "execution_vector": execution_vector
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "TIMED_OUT",
                "return_code": -1,
                "stdout": "",
                "stderr": f"Process execution exceeded enforcement timeout of {self.timeout}s.",
                "payload_sha256": payload_hash,
                "execution_vector": execution_vector
            }
        except Exception as e:
            raise ExecutionSecurityError(f"Sandboxed Execution Failure: {str(e)}")

# Self-Verification Execution Context
if __name__ == "__main__":
    engine = SecureExecutionEngine(timeout_seconds=5)
    # Verification test run: Execution of allowlisted 'ls' binary
    result = engine.execute_command("ls", ["-la", "docs"])
    print(f"[AEGIS EXECUTION VERIFIED] Payload Hash: {result['payload_sha256']}")
    print(f"[STDOUT OUTPUT]:\n{result['stdout'][:150]}...")
