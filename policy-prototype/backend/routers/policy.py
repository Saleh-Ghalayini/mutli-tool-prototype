from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

from services.policy.file_service import save_uploaded_files
from services.policy.pdf_service import extract_text_from_pdfs
from services.policy.chunking_service import chunk_text
from services.policy.embedding_service import embed_chunks
from services.policy.vector_store_service import save_embeddings

router = APIRouter()

@router.post("/policy/upload", tags=["Policy"])
async def upload_policy(files: List[UploadFile] = File(...)):
    """Endpoint to upload one or more policy documents (PDFs), extract their text, chunk it, and return the results."""
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")
    saved_paths = save_uploaded_files(files)
    extracted_texts = extract_text_from_pdfs(saved_paths)
    chunked_texts = [chunk_text(text) for text in extracted_texts]
    embeddings = [embed_chunks(chunks) for chunks in chunked_texts]
    # For now, use a dummy client_id; in production, get from auth/session
    client_id = "default_client"
    vector_store_paths = []
    for chunks, emb in zip(chunked_texts, embeddings):
        path = save_embeddings(client_id, chunks, emb)
        vector_store_paths.append(path)
    return {
        "saved_files": saved_paths,
        "extracted_texts": extracted_texts,
        "chunked_texts": chunked_texts,
        "embeddings": embeddings,
        "vector_store_paths": vector_store_paths,
        "message": "Files uploaded, text extracted, chunked, embedded, and stored successfully."
    }
