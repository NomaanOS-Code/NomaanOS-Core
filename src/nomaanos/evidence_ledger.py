"""
NomaanOS Core - Cryptographic Forensic Audit Ledger (evidence_ledger.py)
Classification: Layer 4 Tamper-Evident Evidence Logging
Author: Nomaan Khan (Scholar @ IHFC - IIT Delhi)
"""

import time
import json
import hashlib
from typing import List, Dict, Any
from pathlib import Path

class ForensicAuditLedger:
    def __init__(self, ledger_file_path: str = "data/forensic_ledger.json"):
        self.ledger_path = Path(ledger_file_path)
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self.chain: List[Dict[str, Any]] = self._load_ledger()

    def _calculate_hash(self, index: int, timestamp: float, payload_hash: str, previous_hash: str) -> str:
        """Computes SHA-256 hash for append-only log node (Merkle Chain)."""
        block_string = f"{index}:{timestamp}:{payload_hash}:{previous_hash}"
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

    def _load_ledger(self) -> List[Dict[str, Any]]:
        """Loads existing ledger or initializes Genesis node."""
        if self.ledger_path.exists():
            try:
                with open(self.ledger_path, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Create Genesis Node
        genesis_hash = hashlib.sha256(b"NOMAANOS_GENESIS_ROOT_V6.0").hexdigest()
        genesis_node = {
            "index": 0,
            "timestamp": time.time(),
            "event": "GENESIS_NODE_INITIALIZED",
            "payload_sha256": genesis_hash,
            "previous_hash": "0" * 64,
            "node_hash": genesis_hash
        }
        return [genesis_node]

    def log_execution_event(self, event_type: str, payload_hash: str) -> Dict[str, Any]:
        """Appends a cryptographically chained execution entry to the ledger."""
        previous_node = self.chain[-1]
        new_index = len(self.chain)
        timestamp = time.time()
        node_hash = self._calculate_hash(new_index, timestamp, payload_hash, previous_node["node_hash"])

        ledger_entry = {
            "index": new_index,
            "timestamp": timestamp,
            "event": event_type,
            "payload_sha256": payload_hash,
            "previous_hash": previous_node["node_hash"],
            "node_hash": node_hash
        }

        self.chain.append(ledger_entry)
        self._persist()
        return ledger_entry

    def _persist(self) -> None:
        """Writes audit chain atomically to filesystem."""
        with open(self.ledger_path, "w") as f:
            json.dump(self.chain, f, indent=2)

    def verify_integrity(self) -> bool:
        """Validates hash integrity across the complete chain."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current["previous_hash"] != previous["node_hash"]:
                return False

            recalculated = self._calculate_hash(
                current["index"],
                current["timestamp"],
                current["payload_sha256"],
                current["previous_hash"]
            )
            if recalculated != current["node_hash"]:
                return False

        return True

if __name__ == "__main__":
    ledger = ForensicAuditLedger()
    # Test Entry Integration
    entry = ledger.log_execution_event("SANDBOX_EXECUTION_LS", "e8fe008ca11c031f5520e97fe0d12a5e9f8283b71935a7d8c481304dbed2f053")
    print(f"[FORENSIC LEDGER ENTRY ADDED] Index: {entry['index']} | Node Hash: {entry['node_hash'][:20]}...")
    print(f"[CHAIN INTEGRITY STATUS]: {ledger.verify_integrity()}")
