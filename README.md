# 🛡️ NomaanOS Core: Sovereign AI Operating Environment (v6.0)

[![Security Benchmark](https://github.com/NomaanOS-Code/NomaanOS-Core/actions/workflows/security_benchmark.yml/badge.svg)](https://github.com/NomaanOS-Code/NomaanOS-Core/actions)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![AI Engine: Local Ollama](https://img.shields.io/badge/AI%20Engine-Ollama%20%28Phi--3%2FLlama--3%29-orange.svg)](https://ollama.ai/)

> **Research & Architecture Prototype**: NomaanOS Core is an agentic security overlay designed for Linux kernels. It decouples AI Intent from OS System Execution through a deterministic, multi-stage Sentinel Interceptor and local Small Language Models (SLMs).

---

## 🏛️ Core Architecture (The Aegis Protocol)

| Subsystem | Security Role | Implementation Detail |
| :--- | :--- | :--- |
| **AEGIS Brain** | Local Offline Intelligence | Ollama (Phi-3 / Llama-3) 100% Sovereign Inference |
| **Sentinel Proxy** | Deterministic Interceptor | Multi-Stage Normalizer + Regex Logic Gate |
| **System Executor** | Isolated Subprocess Exec | Non-shell (`shell=False`) argument vector execution |
| **Integrity Engine** | Cryptographic Verification | SHA-256 Hashes with HMAC Signature Manifests |
| **Forensic Ledger** | Audit Logging | Local JSON evidence ledgers with cryptographic hashes |

---

## 🔒 Security Scope & Threat Model

NomaanOS Core treats AI intent as inherently untrusted. The security enforcement layer operates on a **Defense-in-Depth** model:

1. **Multi-Stage Normalization**: Resolves URL double-encoding, Cyrillic homoglyph substitution, leetspeak, zero-width spaces, and NFKC Unicode canonicalization before pattern inspection.
2. **Deterministic Interception**: Pre-execution blocklist preventing standard prompt injections and dangerous system operations.
3. **Safe Process Isolation**: Command execution via `execve()` system calls (`shell=False`), preventing shell metacharacter expansion (`;`, `&&`, `|`).
4. **HMAC Cryptographic Verification**: Signed manifest ensuring codebase integrity against unauthorized local file tampering.

---

## 🧪 Security Benchmarks & Red-Teaming

To run local stress tests and verify system immunity:

```bash
# 1. Verify Cryptographic Signature of Core Modules
PYTHONPATH=. python3 core/integrity_engine.py

# 2. Execute Red-Team Adversarial Test Suites
PYTHONPATH=. python3 tests/stress_test.py
PYTHONPATH=. python3 tests/redteam_advanced.py
---

### 2. `SECURITY.md` File Ensure Karo

Ye file auditors ke liye bohot badi indicator hoti hai ki project security standards follow karta hai:

```bash
cat << 'EOF' > SECURITY.md
# Security Policy & Threat Disclosure

## Supported Versions

| Version | Supported | Notes |
| ------- | --------- | ----- |
| 6.x     | :white_check_mark: | Active Hardened Architecture |
| < 6.0   | :x: | Legacy / Prototype Models |

## Threat Model & Security Boundaries

NomaanOS Core is a **deterministic security gate research prototype**. It is designed to mitigate:
- Direct Command Injections (`rm -rf`, system overrides)
- Common Prompt Injections & Base64 Obfuscated Payloads
- Shell Metacharacter Escapes

### Out-of-Scope / Known Non-Goals
- Zero-day OS-level kernel exploits (handled by host OS DAC/MAC policies).
- Semantic-only prompt drift without explicit command execution.

## Reporting a Vulnerability

If you discover a security vulnerability within NomaanOS Core, please report it directly via email:
`nikki108@duck.com`
