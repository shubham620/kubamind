"""Simple RAG wrapper: fetch top-k docs from Qdrant and call Ollama LLM for answer generation."""
import os
import logging
from typing import List

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("rag")
logging.basicConfig(level=logging.INFO)

try:
    from qdrant_client import QdrantClient
except Exception as e:
    logger.warning("qdrant-client not installed: %s", e)

import requests


def fetch_context(query: str, collection: str = "logs", top_k: int = 3) -> List[str]:
    host = os.getenv("QDRANT_HOST", "localhost")
    port = int(os.getenv("QDRANT_PORT", 6333))
    api_key = os.getenv("QDRANT_API_KEY", None)

    client = QdrantClient(url=f"http://{host}:{port}", api_key=api_key)
    hits = client.search(collection_name=collection, query_vector=None, query_filter=None, limit=top_k)

    contexts = []
    for h in hits:
        payload = getattr(h, "payload", {})
        # payload may not contain text; include source metadata
        src = payload.get("source") or payload.get("doc_id") or ""
        contexts.append(f"Source: {src}")
    return contexts


def generate_answer(query: str, contexts: List[str]) -> str:
    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
    model = os.getenv("LLM_MODEL", "llama2")

    prompt = """
You are an infrastructure reasoning assistant. Use the following context from system logs and metrics to answer the user's question.

Context:
{context}

Question: {question}

Answer concisely and include root cause and suggested remediation.
""".format(context="\n".join(contexts), question=query)

    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": 512
    }

    try:
        resp = requests.post(f"{ollama_url}/api/generate", json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        # Ollama responses vary; attempt to extract text
        if isinstance(data, dict) and "output" in data:
            return data.get("output")
        if isinstance(data, dict) and "response" in data:
            return data.get("response")
        return str(data)
    except Exception as e:
        logger.exception("LLM request failed: %s", e)
        return "(LLM generation failed)"


def answer_rag(query: str) -> str:
    contexts = fetch_context(query)
    return generate_answer(query, contexts)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--q", "-q", required=True, help="Question to ask the system")
    args = parser.parse_args()
    out = answer_rag(args.q)
    print(out)
