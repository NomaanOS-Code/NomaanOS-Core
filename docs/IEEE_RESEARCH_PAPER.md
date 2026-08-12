# Deterministic Intent-Execution Decoupling in Agentic AI Overlays for Edge Operating Systems

**Author:** Nomaan Khan  
*IHFC - I-Hub Foundation for Cobotics, Indian Institute of Technology (IIT) Delhi*  
*NomaanOS Core Research Group*  
*Email:* nomaank.iitd@gmail.com  

---

## ABSTRACT
As Large Language Models (LLMs) transition from conversational interfaces to autonomous execution agents operating directly within operating system kernels, traditional access control models prove insufficient. Unchecked agentic workflows introduce critical vulnerabilities, including indirect prompt injections, state hijacking, and unpermissioned shell command execution. This paper proposes **NomaanOS Core**, a sovereign agentic framework utilizing a deterministic **Sentinel Proxy** and **Aegis Protocol** to decouple AI decision-making intent from execution threads. Experimental evaluation demonstrates 100% mitigation against 10 primary adversarial injection vectors while maintaining sub-2ms mediation latency.

---

## I. INTRODUCTION
Agentic AI systems rely on function-calling primitives to translate natural language intents into low-level POSIX system calls. However, non-deterministic model outputs expose host environments to security degradation...

## II. SYSTEM ARCHITECTURE
### A. The Aegis Protocol
The Aegis Protocol enforces boundary isolation between the LLM inference engine (AEGIS Brain) and system execution primitives...

### B. Sentinel Proxy & Phoenix Engine
The Sentinel Proxy operates as a hard-coded deterministic logic gate evaluating JSON-formatted intent payloads against active security policy schemas before passing execution tokens to sub-shell processes...

## III. EXPERIMENTAL RESULTS & RED-TEAM BENCHMARKS
Empirical evaluation was conducted across 10 distinct attack vectors...

| Attack Vector ID | Vulnerability Class | Mitigation Status | Mediation Latency |
| :--- | :--- | :--- | :--- |
| ADV-01 | Base64 Obfuscated Payload | BLOCKED | 1.12 ms |
| ADV-02 | Indirect Prompt Injection | BLOCKED | 0.89 ms |
| ADV-03 | Shell Command Escape | BLOCKED | 1.45 ms |
| ADV-04 | Role Spoofing / Jailbreak | BLOCKED | 0.76 ms |

---
*IEEE Style Pre-print Draft — NomaanOS Research Group (2026)*
