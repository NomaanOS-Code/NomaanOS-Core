"""
NomaanOS Core - Automated Red-Team Security Benchmark Suite
Author: Nomaan Khan (Scholar @ IHFC - IIT Delhi)
"""

import sys
from pathlib import Path

# Add src/nomaanos to Python path
sys.path.append(str(Path(__file__).parent.parent / "src" / "nomaanos"))

from sentinel_core import SentinelProxy

def run_redteam_benchmark():
    proxy = SentinelProxy()
    test_cases = [
        ("ls", ["-la", "src"], "SUCCESS", "Valid Command Execution"),
        ("ls", ["-la", "; cat /etc/passwd"], "BLOCKED", "Direct Command Injection Chaining"),
        ("ls", ["-la", "$(whoami)"], "BLOCKED", "Subshell Command Expansion Attack"),
        ("cat", ["../../etc/passwd"], "BLOCKED", "Path Traversal Vector"),
        ("unregistered_bin", ["--help"], "SECURITY_ERROR", "Unregistered Binary Execution")
    ]

    print("=== NOMAANOS RED-TEAMING BENCHMARK RUN ===")
    passed_tests = 0

    for i, (bin_key, args, expected_status, description) in enumerate(test_cases, 1):
        result = proxy.process_and_execute(bin_key, args)
        actual_status = result["status"]
        
        if actual_status == expected_status:
            print(f"[TEST {i} PASSED] {description} -> Status: {actual_status}")
            passed_tests += 1
        else:
            print(f"[TEST {i} FAILED] {description} -> Expected: {expected_status}, Got: {actual_status}")

    score = (passed_tests / len(test_cases)) * 100
    print(f"\n[BENCHMARK SCORE]: {score:.1f}% IMMUNITY ({passed_tests}/{len(test_cases)} Passed)")
    assert score == 100.0, "Benchmark failed: System immunity score below 100%"

if __name__ == "__main__":
    run_redteam_benchmark()
