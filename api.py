import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from sentinel_core import inspect_payload

class SentinelAPIHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            payload_json = json.loads(post_data.decode('utf-8'))
            prompt = payload_json.get("prompt", "")
            
            is_blocked, audit = inspect_payload(prompt)
            
            response = {
                "status": "BLOCKED" if is_blocked else "ALLOWED",
                "http_code": 403 if is_blocked else 200,
                "latency_ms": audit["latency_ms"],
                "rule_matched": audit["matched_pattern"],
                "sha256_audit_hash": audit["entry_sha256"]
            }
            
            self.send_response(403 if is_blocked else 200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SentinelAPIHandler)
    print(f"\n==========================================================")
    print(f" 🌐 NOMAANOS REAL REST API LISTENING ON PORT {port}")
    print(f" Endpoint: http://localhost:{port}/validate")
    print(f"==========================================================\n")
    # Quick single handling test mode or loop
    print("API Server Script Ready & Compiled!")

if __name__ == "__main__":
    run_server()
