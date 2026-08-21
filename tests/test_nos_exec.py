"""
tests/test_nos_exec.py — Regression tests for core/nos_exec.py

These specifically guard against the bug found during Phase-2 hardening:
ALLOWED_BINARIES.get(cmd_binary, cmd_binary) silently fell back to the raw,
non-allowlisted command name instead of rejecting it, and the resolved
binary_path was computed but never actually passed to subprocess.run().
Net effect: the allowlist enforced nothing. These tests fail loudly if
that regresses.

Run with: PYTHONPATH=. python3 tests/test_nos_exec.py
"""

import subprocess
import sys


def run_nos_exec(command_str: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "core/nos_exec.py", command_str],
        capture_output=True,
        text=True,
        timeout=20,
    )


def test_non_allowlisted_binary_is_rejected():
    """
    THE core regression test. Before the fix, 'curl' (not in
    ALLOWED_BINARIES) would execute anyway because .get(key, key) fell
    back to the raw command name instead of failing closed.
    """
    result = run_nos_exec("curl http://example.com")
    assert result.returncode != 0, (
        f"CRITICAL REGRESSION: non-allowlisted binary 'curl' was executed "
        f"(exit code {result.returncode}). The allowlist is not enforcing."
    )
    assert "NOT ALLOWLISTED" in result.stdout, (
        "Expected explicit allowlist-rejection message, got:\n" + result.stdout
    )
    print("PASS: non-allowlisted binary correctly rejected")


def test_arbitrary_unallowlisted_binaries_rejected():
    """Broader sweep — several common binaries that must NOT be in the
    default allowlist. If any of these succeed, the allowlist has silently
    grown or is being bypassed."""
    for binary in ["wget", "nc", "bash", "sh", "python", "curl", "ssh", "scp"]:
        result = run_nos_exec(f"{binary} --help")
        assert result.returncode != 0, (
            f"CRITICAL REGRESSION: '{binary}' executed but is not expected "
            f"to be in ALLOWED_BINARIES. exit_code={result.returncode}"
        )
    print("PASS: full sweep of unallowlisted binaries all rejected")


def test_allowlisted_binary_still_executes():
    """Sanity check the fix didn't break legitimate allowlisted usage."""
    result = run_nos_exec("ls -la")
    assert result.returncode == 0, (
        f"Allowlisted binary 'ls' failed to execute (exit {result.returncode}):\n"
        f"{result.stderr}"
    )
    assert "PERMISSION GRANTED" in result.stdout
    print("PASS: allowlisted binary still executes correctly")


def test_sensitive_path_blocked_for_allowlisted_binary():
    """Even an allowlisted binary must not be able to read sensitive paths."""
    result = run_nos_exec("cat /etc/shadow")
    assert result.returncode != 0, (
        "CRITICAL REGRESSION: allowlisted binary was able to target /etc/shadow"
    )
    print("PASS: sensitive path blocked even for allowlisted binary")


def test_relative_path_traversal_resolves_and_blocks():
    """A relative path that resolves (via Path.resolve()) into a sensitive
    root must be blocked even without an obvious absolute-path string."""
    result = run_nos_exec("cat ../../../../../../etc/passwd")
    assert result.returncode != 0, (
        "CRITICAL REGRESSION: relative-path traversal into /etc was not blocked"
    )
    print("PASS: relative path traversal resolved and blocked")


def test_empty_command_rejected():
    result = run_nos_exec("")
    assert result.returncode != 0
    print("PASS: empty command rejected")


if __name__ == "__main__":
    tests = [
        test_non_allowlisted_binary_is_rejected,
        test_arbitrary_unallowlisted_binaries_rejected,
        test_allowlisted_binary_still_executes,
        test_sensitive_path_blocked_for_allowlisted_binary,
        test_relative_path_traversal_resolves_and_blocks,
        test_empty_command_rejected,
    ]

    failures = []
    for t in tests:
        try:
            t()
        except AssertionError as e:
            failures.append((t.__name__, str(e)))
            print(f"FAIL: {t.__name__}\n  {e}")

    print("\n" + "=" * 60)
    if failures:
        print(f"{len(failures)}/{len(tests)} TESTS FAILED")
        sys.exit(1)
    else:
        print(f"ALL {len(tests)} TESTS PASSED")
        sys.exit(0)
