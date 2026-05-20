"""Lightweight log ingestion into Qdrant for RAG demos.

Usage:
    python -m backend.app.ingest.qdrant_ingest --source simulations --collection logs
"""
import os
import glob
import argparse
import logging
from typing import List

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("qdrant_ingest")
logging.basicConfig(level=logging.INFO)

try:
    from sentence_transformers import SentenceTransformer
    from qdrant_client import QdrantClient
    from qdrant_client.models import VectorParams, PointStruct
except Exception as e:
    logger.warning("Optional ingestion dependencies not installed: %s", e)


def _gather_documents(source_dir: str) -> List[dict]:
    docs = []
    patterns = ["**/*.log", "**/*.txt", "**/*.json"]
    for p in patterns:
        for path in glob.glob(os.path.join(source_dir, p), recursive=True):
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    text = fh.read().strip()
                    if not text:
                        continue
                    docs.append({"id": os.path.relpath(path), "text": text, "source": path})
            except Exception:
                logger.exception("Failed reading %s", path)
    return docs


def ingest_to_qdrant(
    docs: List[dict],
    collection_name: str = "logs",
    embedding_model: str = None,
    host: str = None,
    port: int = None,
    api_key: str = None,
):
    if not docs:
        logger.info("No documents to ingest")
        return

    embedding_model = embedding_model or os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    host = host or os.getenv("QDRANT_HOST", "localhost")
    port = port or int(os.getenv("QDRANT_PORT", 6333))
    api_key = api_key or os.getenv("QDRANT_API_KEY", None)

    logger.info("Connecting to Qdrant %s:%s", host, port)
    client = QdrantClient(url=f"http://{host}:{port}", api_key=api_key) if host else QdrantClient()

    model = SentenceTransformer(embedding_model)
    texts = [d["text"] for d in docs]
    vectors = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    # create collection if not exists
    try:
        client.recreate_collection(collection_name, vectors_config=VectorParams(size=vectors.shape[1], distance="Cosine"))
    except Exception:
        # fallback: create only if missing
        try:
            client.create_collection(collection_name, vectors_config=VectorParams(size=vectors.shape[1], distance="Cosine"))
        except Exception:
            pass

    points = []
    for i, d in enumerate(docs):
        pid = f"doc-{i}-{os.path.basename(d['id'])}"
        payload = {"source": d.get("source"), "doc_id": d.get("id")}
        points.append(PointStruct(id=pid, vector=vectors[i].tolist(), payload=payload))

    logger.info("Upserting %d documents into Qdrant collection '%s'", len(points), collection_name)
    client.upsert(collection_name=collection_name, points=points)
    logger.info("Ingestion complete")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", "-s", default="simulations", help="Source directory to scan for logs")
    parser.add_argument("--collection", "-c", default="logs", help="Qdrant collection name")
    parser.add_argument("--model", "-m", default=None, help="Embedding model")
    args = parser.parse_args()

    src = args.source
    if not os.path.isdir(src):
        logger.error("Source directory not found: %s", src)
        return

    docs = _gather_documents(src)
    ingest_to_qdrant(docs, collection_name=args.collection, embedding_model=args.model)


if __name__ == "__main__":
    main()
