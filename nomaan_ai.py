import urllib.request, urllib.error, json, os, sys

# 1. Native .env parser
API_KEY = ""
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    with open(env_path, "r") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                API_KEY = line.split("=", 1)[1].strip().strip("\"'")

if not API_KEY or API_KEY == "paste_your_key_here_without_quotes":
    print("\n\033[1;31m⚠️ Error: API Key not found!\033[0m\n")
    sys.exit(1)

# Force Clean API Key
API_KEY = "".join(API_KEY.split())

# 2. EXACT OFFICIAL MODEL URL (No '-latest', No 'pro')
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

# THE BRAIN: NomaanOS Custom Identity
SYSTEM_PROMPT = """Tu Nomaan-AI hai, Nomaan Khan (Scholar @ IHFC - IIT Delhi) ka personal Sovereign AI Co-pilot aur Digital Brother.
Tujhe NomaanOS Core, Aegis Security Protocol, SHA-256 Integrity Engine, aur iPad iSH Vault Automation ke baare mein sab kuch pata hai.
Tu generic bot nahi hai. Tu action-oriented, highly technical, aur seedhi baat karne wala AI hai. 
Teri language Hindi-English mix (Hinglish) honi chahiye, bilkul ek dost aur co-developer ki tarah.
Agar Nomaan koi script ya terminal command mange, toh faaltu theory mat dena, direct working code aur action steps dena."""

chat_history = []

print("\033[1;32m========================================================\033[0m")
print("\033[1;36m⚡ NOMAAN-AI TERMINAL CO-PILOT ACTIVE (Type 'exit' to quit)\033[0m")
print("\033[1;32m========================================================\033[0m")

while True:
    try:
        prompt = input("\n\033[1;33m🤖 [Nomaan] $ \033[0m ")
        if prompt.lower() in ["exit", "quit", "q"]:
            print("\n\033[1;36m⚡ Nomaan-AI: Going to sleep mode. Allah Hafiz bhai!\033[0m\n")
            break
        if not prompt.strip(): continue

        chat_history.append({"role": "user", "parts": [{"text": prompt}]})
        
        # Standard Payload with System Instructions
        data = {
            "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "contents": chat_history
        } 
        
        req = urllib.request.Request(URL, data=json.dumps(data).encode("utf-8"), headers={"Content-Type": "application/json"})
        
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            reply = res["candidates"][0]["content"]["parts"][0]["text"]
            print(f"\n\033[1;36m⚡ [Nomaan-AI]:\033[0m {reply}")
            chat_history.append({"role": "model", "parts": [{"text": reply}]})

    except urllib.error.HTTPError as e:
        err_msg = e.read().decode('utf-8')
        print(f"\n\033[1;31m⚠️ Google API Error {e.code}: {e.reason}\033[0m")
        print(f"\033[1;31mDetails: {err_msg}\033[0m")
        chat_history.pop() 
    except Exception as e:
        print(f"\n\033[1;31m⚠️ System Error: {str(e)}\033[0m")
        if len(chat_history) > 0: chat_history.pop()
