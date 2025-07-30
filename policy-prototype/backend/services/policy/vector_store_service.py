from typing import List, Dict
import os
import json

VECTOR_STORE_DIR = os.path.join(os.path.dirname(__file__), '../../../policy_data/vector_store')
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

def save_embeddings(client_id: str, chunks: List[str], embeddings: List[List[float]]):
    """Save chunks and their embeddings to a JSONL file for the given client."""
    file_path = os.path.join(VECTOR_STORE_DIR, f'{client_id}_embeddings.jsonl')
    with open(file_path, 'w', encoding='utf-8') as f:
        for chunk, embedding in zip(chunks, embeddings):
            record = {"chunk": chunk, "embedding": embedding}
            f.write(json.dumps(record) + '\n')
    return file_path

def load_embeddings(client_id: str) -> List[Dict]:
    """Load all chunk-embedding pairs for a client from the vector store."""
    file_path = os.path.join(VECTOR_STORE_DIR, f'{client_id}_embeddings.jsonl')
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]
