"""
PDF Service - Handles PDF text extraction and processing
"""

import PyPDF2
from io import BytesIO
from pathlib import Path
from fastapi import HTTPException

class PDFService:
    """Service for PDF text extraction and processing"""
    
    @staticmethod
    def extract_text_from_bytes(pdf_bytes: bytes) -> str:
        """Extract text from PDF bytes"""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to extract PDF text: {e}")
    
    @staticmethod
    def extract_text_from_file(file_path: str) -> str:
        """Extract text from PDF file path"""
        try:
            pdf_path = Path(file_path)
            if not pdf_path.exists():
                raise HTTPException(status_code=404, detail="PDF file not found")
            
            with open(pdf_path, 'rb') as file:
                return PDFService.extract_text_from_bytes(file.read())
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=f"Failed to process PDF file: {e}")
