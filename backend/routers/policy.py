# ==============================================================================
# POLICY DOCUMENT INGESTION ROUTER
# ==============================================================================
# This router represents the FIRST HALF of the RAG (Retrieval-Augmented Generation) pipeline:
#
#   [Uploaded PDF]
#         │
#         ▼  (1) Save PDF to local disk (file_service)
#   [policy_data/uploads/...]
#         │
#         ▼  (2) Extract raw text from pages (pdf_service)
#   "Company Policy: Employees are entitled to 20 days..."
#         │
#         ▼  (3) Split into 500-character chunks with overlap (chunking_service)
#   ["Chunk 1...", "Chunk 2...", "Chunk 3..."]
#         │
#         ▼  (4) Compute 384-dimensional vector embeddings (embedding_service)
#   [[0.012, -0.045, ...], [0.089, 0.003, ...], ...]
#         │
#         ▼  (5) Save chunks & vectors into JSONL vector store (vector_store_service)
#   [default_client_embeddings.jsonl]
# ==============================================================================

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

# Import domain-specific services responsible for each step of the pipeline
from services.policy.file_service import save_uploaded_files
from services.policy.pdf_service import extract_text_from_pdfs
from services.policy.chunking_service import chunk_text
from services.policy.embedding_service import embed_chunks
from services.policy.vector_store_service import save_embeddings

router = APIRouter()

@router.post("/policy/upload", tags=["Policy"])
async def upload_policy(files: List[UploadFile] = File(...)):
    """
    Endpoint to upload one or more policy documents (PDFs), extract their text,
    split into manageable chunks, generate vector embeddings, and store them locally.

    Parameters:
        files (List[UploadFile]): A list of files sent via multipart/form-data.
                                  FastAPI's UploadFile provides an async file-like
                                  interface that does not immediately load the entire
                                  file into RAM unless read.

    Returns:
        JSON response summarizing the saved paths, extracted texts, chunks,
        embeddings, and vector store file destinations.
    """
    # --------------------------------------------------------------------------
    # Step 0: Input Validation
    # --------------------------------------------------------------------------
    # Ensure at least one file was provided in the request payload
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    # --------------------------------------------------------------------------
    # Step 1: Save Uploaded Files to Disk
    # --------------------------------------------------------------------------
    # Writes the incoming files to the server's policy_data/uploads/ directory
    # so we retain the original source files for auditing and re-processing.
    saved_paths = save_uploaded_files(files)

    # --------------------------------------------------------------------------
    # Step 2: Extract Raw Text from PDFs
    # --------------------------------------------------------------------------
    # Uses PyPDF2 to read each PDF page-by-page and concatenate text into a single
    # continuous string per document.
    extracted_texts = extract_text_from_pdfs(saved_paths)

    # --------------------------------------------------------------------------
    # Step 3: Text Chunking
    # --------------------------------------------------------------------------
    # An entire 50-page PDF cannot be embedded as a single vector (embedding models
    # have maximum token limits, typically 256-512 tokens).
    # We break each document's text into small passages (~500 chars) with 50-char overlap
    # to preserve semantic context across sentence boundaries.
    chunked_texts = [chunk_text(text) for text in extracted_texts]

    # --------------------------------------------------------------------------
    # Step 4: Vector Embedding Generation
    # --------------------------------------------------------------------------
    # Pass each list of chunks to the Sentence-Transformers model ('all-MiniLM-L6-v2').
    # This transforms each text chunk into a 384-dimensional numerical coordinate vector.
    embeddings = [embed_chunks(chunks) for chunks in chunked_texts]

    # --------------------------------------------------------------------------
    # Step 5: Save Embeddings to Vector Store
    # --------------------------------------------------------------------------
    # For now, use a dummy client_id ("default_client"); in a multi-tenant production app,
    # this would come from an authentication token or user session ID.
    client_id = "default_client"
    vector_store_paths = []
    
    # Iterate through each document's chunks and corresponding embedding vectors,
    # saving them to a JSON Lines (.jsonl) file on disk.
    for chunks, emb in zip(chunked_texts, embeddings):
        path = save_embeddings(client_id, chunks, emb)
        vector_store_paths.append(path)

    # --------------------------------------------------------------------------
    # Step 6: Return Response
    # --------------------------------------------------------------------------
    return {
        "saved_files": saved_paths,
        "extracted_texts": extracted_texts,
        "chunked_texts": chunked_texts,
        "embeddings": embeddings,
        "vector_store_paths": vector_store_paths,
        "message": "Files uploaded, text extracted, chunked, embedded, and stored successfully."
    }

