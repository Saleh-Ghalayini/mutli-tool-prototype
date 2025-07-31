
from typing import List
from sentence_transformers import SentenceTransformer

# Load the model once at module import
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks: List[str]) -> List[List[float]]:
    """
    Convert a list of text chunks into embeddings using a real model.
    """
    return model.encode(chunks, convert_to_numpy=True).tolist()
