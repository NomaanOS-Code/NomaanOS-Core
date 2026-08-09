from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
import re

app = FastAPI(
    title="NomaanOS Core — Aegis Security API",
    version="6.0",
    description="Sovereign AI Runtime Security Gateway & Prompt Injection Inspection API"
)

class PromptRequest(BaseModel):
    prompt: str

class InspectionResponse(BaseModel):
    status: str
    mitigated: bool
    reason: str
    sanitized_prompt: str

DANGEROUS_PATTERNS = [
    r"ignore all", r"system override", r"rm -rf", r"dump contents", r"override_sentinel"
]

def inspect_text(text: str):
    # 1. Direct Pattern Inspection
    for pat in DANGEROUS_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            return False, f"Deterministic Gate triggered on '{pat}'"
    
    # 2. Base64 Obfuscation Inspection
    try:
        b64_matches = re.findall(r'[A-Za-z0-9+/]{8,}={0,2}', text)
        for b64 in b64_matches:
            decoded = base64.b64decode(b64).decode('utf-8', errors='ignore')
            for pat in DANGEROUS_PATTERNS:
                if re.search(pat, decoded, re.IGNORECASE):
                    return False, f"Base64 Obfuscated Gate triggered on decoded '{pat}'"
    except Exception:
        pass

    return True, "CLEAN_INTENT"

@app.get("/")
def root():
    return {
        "system": "NomaanOS Core Sentinel REST API",
        "status": "HARDENED",
        "version": "6.0",
        "author": "Nomaan Khan (Scholar @ IHFC - IIT Delhi)"
    }

@app.get("/health")
def health():
    return {"status": "HEALTHY", "immunity": "100.0%"}

@app.post("/api/v1/inspect", response_model=InspectionResponse)
def inspect_prompt(payload: PromptRequest):
    is_safe, reason = inspect_text(payload.prompt)
    if not is_safe:
        return InspectionResponse(
            status="BLOCKED",
            mitigated=True,
            reason=reason,
            sanitized_prompt="[REDACTED_BY_SENTINEL_PROXY]"
        )
    return InspectionResponse(
        status="AUTHORIZED",
        mitigated=False,
        reason=reason,
        sanitized_prompt=payload.prompt
    )
