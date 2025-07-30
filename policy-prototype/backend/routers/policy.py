from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

from services.policy.file_service import save_uploaded_files
from services.policy.pdf_service import extract_text_from_pdfs

router = APIRouter()

@router.post("/policy/upload", tags=["Policy"])
async def upload_policy(files: List[UploadFile] = File(...)):
    """Endpoint to upload one or more policy documents (PDFs), extract their text, and return it."""
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")
    saved_paths = save_uploaded_files(files)
    extracted_texts = extract_text_from_pdfs(saved_paths)
    return {
        "saved_files": saved_paths,
        "extracted_texts": extracted_texts,
        "message": "Files uploaded and text extracted successfully."
    }
