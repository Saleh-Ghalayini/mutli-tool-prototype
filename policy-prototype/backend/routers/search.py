from fastapi import APIRouter, Query, HTTPException
from services.policy.vector_store_service import load_embeddings
from services.policy.embedding_service import embed_chunks

from typing import List
import numpy as np

from services.policy.prompt_service import build_rag_prompt
from services.policy.llm_service import run_llm

router = APIRouter()

def cosine_similarity(a: List[float], b: List[float]) -> float:
    a = np.array(a)
    b = np.array(b)
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

@router.get("/policy/search", tags=["Policy"])
def search_policy(query: str = Query(..., description="Search query"), top_k: int = 5):
    """Search for relevant policy chunks using vector similarity."""
    client_id = "default_client"
    records = load_embeddings(client_id)
    if not records:
        raise HTTPException(status_code=404, detail="No policy data found.")
    # Embed the query (returns a list of one embedding)
    query_embedding = embed_chunks([query])[0]
    # Compute similarity for each chunk
    for rec in records:
        rec["similarity"] = cosine_similarity(query_embedding, rec["embedding"])
    # Sort by similarity, descending
    results = sorted(records, key=lambda r: r["similarity"], reverse=True)[:top_k]
    # Build the RAG prompt using the top chunks
    context_chunks = [r["chunk"] for r in results]
    rag_prompt = build_rag_prompt(context_chunks, query)
    llm_answer = run_llm(rag_prompt)
    return {
        "results": results,
        "rag_prompt": rag_prompt,
        "llm_answer": llm_answer,
        "message": f"Top {top_k} most similar chunks returned, RAG prompt built, and LLM answer generated."
    }
