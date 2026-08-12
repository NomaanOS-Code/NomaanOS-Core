🎓 Academic Alignment & Research Context

Developed as part of research coursework and practical implementation in Generative AI, Security Engineering, and Agentic Automation (IHFC - I-Hub Foundation for Cobotics, IIT Delhi).

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
