# NomaanOS-Core

## Sovereign AI Operating Environment

NomaanOS-Core is a security-focused AI operating environment built around deterministic policy enforcement, command execution controls, evidence logging, and Sentinel-based security inspection.

### Core Components

- **Sentinel Core** — deterministic payload inspection and security policy enforcement.
- **NOS Exec** — restricted command execution with an explicit binary allowlist, resolved-path checks, and `shell=False` subprocess execution.
- **Evidence Ledger** — security/audit evidence recording with cryptographic integrity metadata.
- **Phoenix Engine** — recovery and resilience-oriented project components.
- **Neural Lock** — additional protection mechanisms within the NomaanOS security architecture.

## Security

NOS Exec uses a fail-closed execution model:

1. Commands are inspected by the Sentinel security gate.
2. Shell parsing is performed without shell execution.
3. Only explicitly allowlisted binaries can execute.
4. Executable targets are resolved and verified before execution.
5. Sensitive filesystem roots are blocked.
6. Subprocess execution uses `shell=False`.
7. Execution is bounded by a timeout.

### Validation

The current security test suite includes:

```text
6/6 direct NOS Exec security tests passed
10/10 advanced red-team vectors blocked
100% red-team immunity score

python3 -m py_compile core/*.py src/nomaanos/*.py tests/*.py

PYTHONPATH=. python3 tests/test_nos_exec.py
PYTHONPATH=. python3 tests/redteam_advanced.py

Repository Structure
NomaanOS-Core/
├── core/                  # Core NomaanOS components
├── src/nomaanos/          # Restored NomaanOS security source
├── tests/                 # Security and validation tests
├── data/                  # Project data
├── docs/                  # Documentation
├── scripts/               # Utility and operational scripts
├── web/                   # Web-facing components
├── dist/                  # Distribution / landing-page assets
├── Dockerfile
├── docker-compose.yml
├── SECURITY.md
└── README.md

Setup
Clone the repository:git clone https://github.com/NomaanOS-Code/NomaanOS-Core.git
cd NomaanOS-Core
Install project dependencies as required by the deployment environment, then run the validation commands above.
Development
Before committing changes:

python3 -m py_compile core/*.py src/nomaanos/*.py tests/*.py
PYTHONPATH=. python3 tests/test_nos_exec.py
PYTHONPATH=. python3 tests/redteam_advanced.py
git diff --check

Generated Python caches should not be committed.
Security Reporting
Please review SECURITY.md for information about reporting security vulnerabilities.
License
MIT License © 2026 Nomaan Khan
