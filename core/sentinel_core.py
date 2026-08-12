import re
import json
import time
import hashlib
import urllib.parse
import unicodedata

# 1. MULTI-STAGE UNICODE & OBFUSCATION NORMALIZER
class SentinelNormalizer:
    ZERO_WIDTH = re.compile(r'[\u200B\u200C\u200D\uFEFF\u00AD\u2060\u180E]')
    
    HOMOGLYPH_MAP = {
        '\u0430': 'a', '\u0410': 'A', '\u0435': 'e', '\u0415': 'E',
        '\u0456': 'i', '\u0406': 'I', '\u043e': 'o', '\u041e': 'O',
        '\u0440': 'r', '\u0420': 'P', '\u0441': 'c', '\u0421': 'C',
        '\u0445': 'x', '\u0425': 'X', '\u0443': 'y', '\u0423': 'Y',
    }

    LEET_MAP = {'0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's', '7': 't', '$': 's', '!': 'i'}

    def normalize(self, text: str) -> list[str]:
        variants = [text]
        
        # Double URL decode
        decoded = text
        for _ in range(2):
            new_dec = urllib.parse.unquote(decoded)
            if new_dec == decoded: break
            decoded = new_dec
        variants.append(decoded)

        # Strip zero-width chars
        stripped = self.ZERO_WIDTH.sub('', decoded)
        
        # NFKC Unicode Normalization
        nfkc = unicodedata.normalize('NFKC', stripped)
        variants.append(nfkc)

        # Homoglyph translation
        homo = ''.join(self.HOMOGLYPH_MAP.get(c, c) for c in nfkc)
        variants.append(homo)

        # Leetspeak translation
        leet = ''.join(self.LEET_MAP.get(c, c) for c in homo.lower())
        variants.append(leet)

        return list(set(variants))

# 2. DETERMINISTIC SECURITY RULES
PATTERNS = [
    r'ignore\s+all\s+previous',
    r'ignore\s+all',
    r'override\s+sentinel',
    r'rm\s+-rf',
    r'/etc/passwd',
    r'dump\s+contents',
    r'system_exec',
    r'eval\(',
    r'base64',
    r'chmod\s+777',
]

normalizer = SentinelNormalizer()

def inspect_payload(payload: str):
    start_time = time.time()
    
    # Generate canonical variants
    normalized_variants = normalizer.normalize(payload)
    
    matched_rule = None
    is_blocked = False

    for variant in normalized_variants:
        for pattern in PATTERNS:
            if re.search(pattern, variant, re.IGNORECASE):
                is_blocked = True
                matched_rule = pattern
                break
        if is_blocked:
            break

    entry_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    latency = round((time.time() - start_time) * 1000, 3)

    audit_entry = {
        "timestamp": time.time(),
        "entry_sha256": entry_hash,
        "status": "BLOCKED" if is_blocked else "ALLOWED",
        "matched_pattern": matched_rule,
        "latency_ms": latency
    }

    return is_blocked, audit_entry
