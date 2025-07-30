import os
from fastapi import UploadFile
from typing import List

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '../../../policy_data/uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_files(files: List[UploadFile]) -> List[str]:
    """Save uploaded files to the upload directory and return their paths."""
    saved_files = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        saved_files.append(file_path)
    return saved_files
