import os, glob, re, json, hashlib
from sentinel_core import inspect_payload

VAULT_DOCS_DIR = os.path.expanduser("~/iSH/00_NOMAANOS_OFFICIAL_VAULT/01_HUMAN_READABLE_DOCS")
LOCAL_DOCS = [f for f in glob.glob("*.md") + glob.glob("*.txt")]

def load_and_chunk_documents():
    """Reads all local Markdown & Text research files and creates a lightweight search index."""
    chunks = []
    
    # Scan local workspace + Vault docs
    sources = LOCAL_DOCS
    if os.path.exists(VAULT_DOCS_DIR):
        sources += [os.path.join(VAULT_DOCS_DIR, f) for f in os.listdir(VAULT_DOCS_DIR) if f.endswith(('.md', '.txt'))]

    for filepath in set(sources):
        if not os.path.isfile(filepath):
            continue
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                # Split by sections or double newlines
                paragraphs = re.split(r'\n\s*\n', content)
                for idx, p in enumerate(paragraphs):
                    p_clean = p.strip()
                    if len(p_clean) > 30: # Ignore tiny lines
                        chunks.append({
                            "source": os.path.basename(filepath),
                            "chunk_id": f"{os.path.basename(filepath)}#p{idx}",
                            "text": p_clean
                        })
        except Exception:
            pass
    return chunks

def vector_keyword_search(query, chunks, top_k=2):
    """Real deterministic keyword-based semantic scorer for local RAG retrieval."""
    keywords = re.findall(r'\w+', query.lower())
    scored_chunks = []

    for chunk in chunks:
        text_lower = chunk["text"].lower()
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scored_chunks.append((score, chunk))

    # Sort by relevance score descending
    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    return [c[1] for c in scored_chunks[:top_k]]

def query_rag_pipeline(user_query):
    print(f"\n\033[94m[RAG ENGINE]\033[0m Processing Query: '{user_query}'")
    
    # Step 1: Pass through Sentinel Security Interceptor first
    is_blocked, audit = inspect_payload(user_query)
    if is_blocked:
        print(f"\033[91m[403 SECURITY BLOCK]\033[0m Sentinel intercepted unsafe RAG query!")
        return None

    # Step 2: Retrieve local context
    chunks = load_and_chunk_documents()
    matches = vector_keyword_search(user_query, chunks)

    print(f"\033[92m[200 OK]\033[0m Scanned {len(chunks)} local document chunks. Found {len(matches)} relevant context match(es):\n")
    
    for idx, match in enumerate(matches, 1):
        print(f"--- \033[96mMatch {idx} [{match['source']}]\033[0m ---")
        print(f"{match['text'][:250]}...")
        print("-" * 50)

if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Aegis Protocol security"
    query_rag_pipeline(query)
