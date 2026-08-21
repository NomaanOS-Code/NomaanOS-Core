import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from core.sentinel_core import inspect_payload

MAX_PAYLOAD_SIZE = 10 * 1024 * 1024  # 10 MB Max Body Payload Limit

class SentinelAPIHandler(BaseHTTPRequestHandler):
    
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))

        # DoS Prevention Guard
        if content_length > MAX_PAYLOAD_SIZE:
            self.send_response(413)
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Payload Too Large. Max size is 10MB."}).encode('utf-8'))
            return

        post_data = self.rfile.read(content_length)

        try:
            payload_json = json.loads(post_data.decode('utf-8'))
            prompt = payload_json.get("prompt", "")

            if not prompt:
                self.send_response(400)
                self._send_cors_headers()
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Missing 'prompt' field in JSON request."}).encode('utf-8'))
                return

            # SENTINEL SECURITY GATE INTERCEPTION
            is_blocked, audit = inspect_payload(prompt)

            response = {
                "status": "BLOCKED" if is_blocked else "ALLOWED",
                "http_code": 403 if is_blocked else 200,
                "latency_ms": audit["latency_ms"],
                "rule_matched": audit["matched_pattern"],
                "sha256_audit_hash": audit["entry_sha256"]
            }

            self.send_response(403 if is_blocked else 200)
            self._send_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))

        except json.JSONDecodeError:
            self.send_response(400)
            self._send_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON Payload Body."}).encode('utf-8'))

        except Exception as e:
            self.send_response(500)
            self._send_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Internal Server Error: {str(e)}"}).encode('utf-8'))

    def log_message(self, format, *args):
        return  # Mute default HTTP noise

def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SentinelAPIHandler)
    print(f"\033[1;32m🌐 NOMAANOS SECURE REST API GATEWAY LISTENING ON PORT {port}\033[0m")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\033[1;36m⚡ REST API Gateway shutting down cleanly.\033[0m")

if __name__ == "__main__":
    run_server()
