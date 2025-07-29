"""
File Service - Handles file upload and management
"""

import shutil
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
import tempfile

class FileService:
    """Service for file upload and management operations"""
    
    def __init__(self):
        self.temp_dir = Path(tempfile.gettempdir()) / "multi-tool-ai"
        self.temp_dir.mkdir(exist_ok=True)
    
    def save_uploaded_file(self, file: UploadFile) -> dict:
        """Save uploaded file to temporary directory"""
        try:
            # Generate unique filename
            file_id = str(uuid.uuid4())
            file_extension = Path(file.filename).suffix
            temp_filename = f"{file_id}_{file.filename}"
            temp_path = self.temp_dir / temp_filename
            
            # Save file
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            return {
                "success": True,
                "file_path": str(temp_path),
                "filename": file.filename,
                "size": temp_path.stat().st_size
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File upload failed: {e}")
    
    def cleanup_file(self, file_path: str) -> None:
        """Clean up temporary file"""
        try:
            Path(file_path).unlink(missing_ok=True)
        except Exception:
            # Ignore cleanup errors
            pass
