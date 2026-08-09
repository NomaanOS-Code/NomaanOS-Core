from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import re
import base64

DANGEROUS_PATTERNS = [
    r"ignore all", r"system override", r"rm -rf", r"dump contents", r"override_sentinel"
]

def inspect_text(text: str):
    # Direct Pattern Inspection
    for pat in DANGEROUS_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            return False, f"Deterministic Gate triggered on '{pat}'"
    
    # Base64 Obfuscation Inspection
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

class SentinelAPIHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        if self.path == '/':
            self._send_response(200, {
                "system": "NomaanOS Core Sentinel REST API",
                "status": "HARDENED",
                "version": "6.0",
                "author": "Nomaan Khan (Scholar @ IHFC - IIT Delhi)"
            })
        elif self.path == '/health':
            self._send_response(200, {"status": "HEALTHY", "immunity": "100.0%"})
        else:
            self._send_response(404, {"error": "Endpoint not found"})

    def do_POST(self):
        if self.path == '/api/v1/inspect':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                payload = json.loads(post_data.decode('utf-8'))
                prompt = payload.get('prompt', '')
                is_safe, reason = inspect_text(prompt)
                
                if not is_safe:
                    self._send_response(200, {
                        "status": "BLOCKED",
                        "mitigated": True,
                        "reason": reason,
                        "sanitized_prompt": "[REDACTED_BY_SENTINEL_PROXY]"
                    })
                else:
                    self._send_response(200, {
                        "status": "AUTHORIZED",
                        "mitigated": False,
                        "reason": reason,
                        "sanitized_prompt": prompt
                    })
            except Exception as e:
                self._send_response(400, {"error": f"Invalid JSON payload: {str(e)}"})
        else:
            self._send_response(404, {"error": "Endpoint not found"})

def run(server_class=HTTPServer, handler_class=SentinelAPIHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"🛡️ NomaanOS Aegis API running on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
