import urllib.request, json, sys

def test_api(payload):
    url = 'http://localhost:8080/validate'
    data = json.dumps({"prompt": payload}).encode('utf-8')
    
    print(f"\033[94m[API TESTER]\033[0m Requesting: {payload[:40]}...")
    
    try:
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            status = res_data.get("status")
            print(f"\033[92m[200 OK]\033[0m Server Response: {status} | Latency: {res_data.get('latency_ms')} ms")
            print(f"Audit Hash: {res_data.get('sha256_audit_hash')[:16]}...")
    except Exception as e:
        print(f"\033[91m[API CONNECTION ERROR]\033[0m Ensure API server is running on port 8080! {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        test_api("ls -la") # Safe test
    else:
        test_api(" ".join(sys.argv[1:]))
