"""
NomaanOS Core - Sentinel Proxy Gatekeeper (sentinel_core.py)
Classification: Layer 2 & 3 Input Interceptor & Orchestrator
Author: Nomaan Khan (Scholar @ IHFC - IIT Delhi)
"""

import re
import base64
from typing import Dict, Any, List
from nos_exec import SecureExecutionEngine, ExecutionSecurityError
from evidence_ledger import ForensicAuditLedger

class SentinelProxy:
    def __init__(self):
        self.executor = SecureExecutionEngine(timeout_seconds=10)
        self.ledger = ForensicAuditLedger()
        # Threat detection regex for command chaining & injection attempts
        self.forbidden_patterns = [
            r";", r"&&", r"\|", r"`", r"\$\(.*\)", r"\.\./", r"rm\s+-rf"
        ]

    def _scan_threats(self, raw_input: str) -> bool:
        """Inspects raw payload against threat patterns and Base64-encoded bypass vectors."""
        # 1. Direct Pattern Inspection
        for pattern in self.forbidden_patterns:
            if re.search(pattern, raw_input):
                return False

        # 2. Base64 Evasion Inspection
        try:
            decoded = base64.b64decode(raw_input, validate=True).decode('utf-8', errors='ignore')
            for pattern in self.forbidden_patterns:
                if re.search(pattern, decoded):
                    return False
        except Exception:
            pass # Payload is not base64 encoded

        return True

    def process_and_execute(self, binary_key: str, args: List[str]) -> Dict[str, Any]:
        """Orchestrates input security scanning, sandboxed execution, and forensic logging."""
        raw_payload = f"{binary_key} " + " ".join(args)

        # Step 1: Pre-execution Threat Scanning
        if not self._scan_threats(raw_payload):
            block_log = self.ledger.log_execution_event("SENTINEL_BLOCKED_INJECTION", "BLOCKED_PAYLOAD_HASH")
            return {
                "status": "BLOCKED",
                "reason": "AEGIS_POLICY_VIOLATION: Injection vector detected in payload.",
                "ledger_node": block_log["node_hash"]
            }

        # Step 2: Sandboxed Execution
        try:
            exec_result = self.executor.execute_command(binary_key, args)
            
            # Step 3: Cryptographic Audit Logging
            ledger_entry = self.ledger.log_execution_event(
                f"EXECUTION_{binary_key.upper()}",
                exec_result["payload_sha256"]
            )
            
            exec_result["forensic_ledger_index"] = ledger_entry["index"]
            exec_result["forensic_node_hash"] = ledger_entry["node_hash"]
            return exec_result

        except ExecutionSecurityError as e:
            block_log = self.ledger.log_execution_event("SENTINEL_EXEC_SECURITY_ERROR", "ERROR_PAYLOAD_HASH")
            return {
                "status": "SECURITY_ERROR",
                "reason": str(e),
                "ledger_node": block_log["node_hash"]
            }

if __name__ == "__main__":
    proxy = SentinelProxy()
    
    # Test Case 1: Valid Execution
    res1 = proxy.process_and_execute("ls", ["-la", "src"])
    print(f"[SENTINEL VALID EXECUTION]: Status={res1['status']} | Logged Index={res1.get('forensic_ledger_index')}")

    # Test Case 2: Injection Attack Attempt
    res2 = proxy.process_and_execute("ls", ["-la", "; cat /etc/passwd"])
    print(f"[SENTINEL INJECTION TEST]: Status={res2['status']} | Reason={res2['reason']}")
