import os
import sys
import re
from core.sentinel_core import inspect_payload

def load_and_chunk_documents(target_dir="."):
    chunks = []
    supported_extensions = ('.md', '.txt')
    
    for root, _, files in os.walk(target_dir):
        # Skip virtual environment and hidden folders
        if "venv" in root or ".git" in root or "data" in root:
            continue
            
        for file in files:
            if file.endswith(supported_extensions):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        paragraphs = re.split(r'\n\s*\n', content)
                        for idx, p in enumerate(paragraphs):
                            p_clean = p.strip()
                            if len(p_clean) > 30:  # Noise filtering
                                chunks.append({
                                    "source": os.path.relpath(filepath, target_dir),
                                    "chunk_id": f"{os.path.basename(filepath)}#p{idx}",
                                    "text": p_clean
                                })
                except Exception as e:
                    print(f"⚠️ [RAG SCAN ERROR] Could not read {filepath}: {e}")

    return chunks

def vector_keyword_search(query, chunks, top_k=3):
    keywords = re.findall(r'\w+', query.lower())
    if not keywords:
        return []

    scored_chunks = []
    for chunk in chunks:
        text_lower = chunk["text"].lower()
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return [c[1] for c in scored_chunks[:top_k]]

def query_rag_pipeline(user_query):
    print(f"\n\033[94m[RAG ENGINE]\033[0m Scanning Knowledge Base for: '{user_query}'")

    # 1. SENTINEL SECURITY GATE INTERCEPTION
    is_blocked, audit = inspect_payload(user_query)
    if is_blocked:
        print(f"\033[91m🛑 [SENTINEL BLOCK 403]\033[0m Intercepted malicious RAG query!")
        print(f"   Matched Rule: {audit['matched_pattern']}")
        return None

    # 2. DOCUMENT SCAN & KEYWORD RETRIEVAL
    chunks = load_and_chunk_documents()
    matches = vector_keyword_search(user_query, chunks)

    if not matches:
        print("\033[93m⚠️ [RAG] No matching local context found.\033[0m\n")
        return []

    print(f"\033[92m[200 OK]\033[0m Indexed {len(chunks)} local chunks. Found {len(matches)} relevant match(es):\n")
    for idx, match in enumerate(matches, 1):
        print(f"--- \033[96mMatch {idx} [{match['source']}]\033[0m ---")
        preview = match['text'][:200].replace('\n', ' ')
        print(f"{preview}...")
        print("-" * 50)

    return matches

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "Aegis Protocol security"
    query_rag_pipeline(query)
