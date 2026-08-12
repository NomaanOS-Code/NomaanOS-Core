import subprocess
import requests
import json
import sys

def get_rag_context(query):
    try:
        res = subprocess.run(["python3", "rag_engine.py", query], capture_output=True, text=True)
        return res.stdout
    except Exception as e:
        return f"RAG Error: {str(e)}"

def query_ollama(prompt, context):
    url = "http://localhost:11434/api/generate"
    system_prompt = f"You are NomaanOS Local Sentinel Intelligence. Answer the query strictly based on the provided local RAG context.\n\nCONTEXT:\n{context}\n\nUSER QUERY: {prompt}"
    
    payload = {
        "model": "llama3:8b",
        "prompt": system_prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "No response text found.")
        else:
            return f"Ollama HTTP Error: {response.status_code}"
    except Exception as e:
        return f"Ollama Daemon Connection Failed: {str(e)}"

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "Explain Aegis Security Protocol and Sentinel Core"
    print(f"\n[OFFLINE RAG + OLLAMA] Processing Query: '{query}'")
    context = get_rag_context(query)
    print("\n[+] Local Document Context Retrieved.")
    print("[+] Querying Llama3 8B GPU Engine...\n")
    answer = query_ollama(query, context)
    print("============================================================")
    print(answer)
    print("============================================================")
