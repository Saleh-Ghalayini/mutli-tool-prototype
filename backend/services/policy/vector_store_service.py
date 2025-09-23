# ==============================================================================
# LOCAL VECTOR STORE SERVICE (JSON LINES FORMAT)
# ==============================================================================
# In production RAG systems, developers often use dedicated vector databases
# like Pinecone, ChromaDB, Milvus, or Qdrant.
#
# Why does this prototype use JSONL (.jsonl) files instead?
# 1. Zero External Dependencies: It requires no database server (Docker, PostgreSQL, etc.)
#    to be installed, running, or maintained on the user's local machine.
# 2. Complete Portability: The entire knowledge base is saved as a plain text file
#    inside the policy_data/vector_store/ folder.
# 3. What is JSONL?
#    "JSON Lines" is a format where every line in the text file is a complete, valid JSON object.
#    Line 1: {"chunk": "Text A...", "embedding": [0.01, -0.02, ...]}
#    Line 2: {"chunk": "Text B...", "embedding": [0.05, 0.08, ...]}
#    This makes reading and writing line-by-line simple and streamable.

from typing import List, Dict
import os
import json

# Define the directory where client embedding files are persisted
VECTOR_STORE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../policy_data/vector_store'))
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

def save_embeddings(client_id: str, chunks: List[str], embeddings: List[List[float]]) -> str:
    """
    Save text chunks and their corresponding embedding vectors to a JSONL file.

    Parameters:
        client_id (str): Identifier for the client or organization (e.g. "default_client").
                         This allows isolation between different users' documents.
        chunks (List[str]): List of text chunk strings.
        embeddings (List[List[float]]): List of 384-dimensional vector coordinate lists.

    Returns:
        str: The file path where the embeddings were saved.
    """
    file_path = os.path.join(VECTOR_STORE_DIR, f'{client_id}_embeddings.jsonl')
    
    # Open the file for writing (UTF-8 encoding ensures special characters and accents are preserved).
    # NOTE FOR INTERVIEWS: Mode 'w' overwrites the file. In an incremental indexing system,
    # append mode ('a') or an upsert database logic would be used to keep prior documents.
    with open(file_path, 'w', encoding='utf-8') as f:
        # Pair each chunk string with its corresponding vector embedding using zip()
        for chunk, embedding in zip(chunks, embeddings):
            record = {"chunk": chunk, "embedding": embedding}
            # json.dumps converts the Python dictionary into a JSON string.
            # We append '\n' so each record occupies exactly one line in the file.
            f.write(json.dumps(record) + '\n')
            
    return file_path

def load_embeddings(client_id: str) -> List[Dict]:
    """
    Load all chunk-embedding records for a client from the vector store into memory.

    Parameters:
        client_id (str): The client identifier whose embeddings should be loaded.

    Returns:
        List[Dict]: A list of dictionary objects, each containing:
                    - "chunk": The original text passage (str)
                    - "embedding": The 384-dimensional vector (List[float])
                    Returns an empty list [] if no vector file exists yet.
    """
    file_path = os.path.join(VECTOR_STORE_DIR, f'{client_id}_embeddings.jsonl')
    
    # If the file does not exist (e.g., no documents uploaded yet), return an empty list safely
    if not os.path.exists(file_path):
        return []
        
    # Read the file line-by-line and deserialize each JSON line back into a Python dictionary
    with open(file_path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]

