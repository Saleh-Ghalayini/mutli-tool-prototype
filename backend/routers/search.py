# ==============================================================================
# POLICY SEARCH & REAL-TIME RAG QUERY ROUTER
# ==============================================================================
# This file represents the SECOND HALF of the RAG pipeline:
#
#   User Query: "How many vacation days do I get?"
#         │
#         ▼  (1) Embed query into 384-dim vector (embedding_service)
#   [0.045, -0.012, 0.098, ...]
#         │
#         ▼  (2) Load stored document chunks from JSONL (vector_store_service)
#         │
#         ▼  (3) Calculate Cosine Similarity with every stored chunk (NumPy)
#   Chunk A: score 0.89 (Vacation Policy)  <-- Top Match!
#   Chunk B: score 0.82 (Paid Time Off)    <-- Top Match!
#   Chunk C: score 0.31 (Dress Code)       <-- Discarded
#         │
#         ▼  (4) Pick Top K chunks (top_k=3)
#         │
#         ▼  (5) Combine Chunks + Query into Grounded Prompt (prompt_service)
#         │
#         ▼  (6) Local LLM Inference with Phi-3 Mini (llm_service)
#         │
#         ▼  (7) Stream tokens back to client (FastAPI StreamingResponse)
# ==============================================================================

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
import numpy as np

# Import domain services for embeddings, vector storage, prompt formatting, and LLM inference
from services.policy.vector_store_service import load_embeddings
from services.policy.embedding_service import embed_chunks
from services.policy.prompt_service import build_rag_prompt
from services.policy.llm_service import run_llm

router = APIRouter()

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """
    Calculate the Cosine Similarity between two numerical vectors.
    
    Formula:
        Cosine Similarity = (a · b) / (||a|| * ||b||)
        where:
        - (a · b) is the dot product (sum of pairwise multiplications)
        - ||a|| is the Euclidean length (L2 norm) of vector a: sqrt(sum(x^2))
        - ||b|| is the Euclidean length (L2 norm) of vector b: sqrt(sum(y^2))
        
    Intuition:
        Cosine similarity measures the angle between two multi-dimensional arrows,
        ignoring their magnitude.
        - 1.0 means the vectors point in exactly the same direction (identical semantic meaning).
        - 0.0 means the vectors are perpendicular (completely unrelated).
        - -1.0 means they point in opposite directions.
        
    Parameters:
        a (List[float]): Vector 1 (e.g., query embedding)
        b (List[float]): Vector 2 (e.g., document chunk embedding)
        
    Returns:
        float: Similarity score between 0.0 and 1.0.
    """
    a = np.array(a)
    b = np.array(b)
    
    # Check for zero vectors to prevent division-by-zero errors (NaN)
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
        
    # np.dot(a, b) computes the scalar dot product
    # np.linalg.norm(x) computes the magnitude/length of the vector
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

@router.get("/policy/search", tags=["Policy"])
def search_policy(query: str = Query(..., description="Search query"), top_k: int = 3):
    """
    Search for relevant policy chunks using vector similarity and stream LLM output.
    
    Parameters:
        query (str): The question asked by the user (passed as a URL query parameter,
                     e.g., /policy/search?query=What+is+leave+policy).
        top_k (int): How many top-matching document excerpts to retrieve as context (default: 3).
        
    Returns:
        StreamingResponse: An HTTP chunked transfer response streaming generated tokens
                           in real-time as the local AI model produces them.
    """
    client_id = "default_client"
    
    # --------------------------------------------------------------------------
    # Step 1: Load Stored Embeddings from Disk
    # --------------------------------------------------------------------------
    # Reads all previously processed chunks and their 384-dimensional vectors from
    # policy_data/vector_store/default_client_embeddings.jsonl.
    records = load_embeddings(client_id)
    if not records:
        raise HTTPException(status_code=404, detail="No policy data found. Please upload documents first.")

    # --------------------------------------------------------------------------
    # Step 2: Convert User Query into an Embedding Vector
    # --------------------------------------------------------------------------
    # embed_chunks expects a list of strings and returns a list of vectors.
    # [0] grabs the single embedding vector corresponding to this query.
    query_embedding = embed_chunks([query])[0]

    # --------------------------------------------------------------------------
    # Step 3: Compute Semantic Similarity Against Every Stored Chunk
    # --------------------------------------------------------------------------
    # We compare the query vector against each stored chunk's vector coordinate.
    for rec in records:
        rec["similarity"] = cosine_similarity(query_embedding, rec["embedding"])

    # --------------------------------------------------------------------------
    # Step 4: Rank and Select the Top-K Most Relevant Chunks
    # --------------------------------------------------------------------------
    # Sort records by similarity descending (highest score first) and slice the top_k.
    results = sorted(records, key=lambda r: r["similarity"], reverse=True)[:top_k]

    # --------------------------------------------------------------------------
    # Step 5: Build Grounded RAG Prompt
    # --------------------------------------------------------------------------
    # Extract just the raw text of the winning chunks and inject them into our
    # anti-hallucination prompt template.
    context_chunks = [r["chunk"] for r in results]
    rag_prompt = build_rag_prompt(context_chunks, query)

    # --------------------------------------------------------------------------
    # Step 6: Generate and Stream LLM Tokens
    # --------------------------------------------------------------------------
    # run_llm returns a Python Generator that yields text chunks/tokens one by one.
    llm_stream = run_llm(rag_prompt)
    
    # StreamingResponse sends tokens over the open HTTP connection as they become available.
    # This enables the frontend chat interface to display words in real time (typing animation)
    # instead of waiting 5-10 seconds for the entire answer to finish generating.
    return StreamingResponse(llm_stream, media_type="text/plain")

