# ==============================================================================
# POLICY FILE SERVICE
# ==============================================================================
# Responsible for handling physical file operations:
# - Ensuring the storage folder exists
# - Writing uploaded multipart files from memory/temp space to the local disk

import os
from fastapi import UploadFile
from typing import List

# ------------------------------------------------------------------------------
# Directory Setup
# ------------------------------------------------------------------------------
# os.path.dirname(__file__) returns the directory containing this script.
# '../../../policy_data/uploads' navigates 3 levels up to the project root and then
# into the 'policy_data/uploads' folder.
# os.path.abspath resolves any symlinks or relative references into a clean absolute path.
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../policy_data/uploads'))

# Create the upload directory automatically if it doesn't already exist.
# exist_ok=True prevents Python from throwing a FileExistsError if the folder is already there.
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_files(files: List[UploadFile]) -> List[str]:
    """
    Save uploaded files to the upload directory and return their paths.
    
    How it works:
    1. Loops through each uploaded file received from FastAPI.
    2. Constructs a target destination path: UPLOAD_DIR + original filename.
    3. Reads the binary data from the file stream using file.file.read().
    4. Writes the binary data to disk in write-binary mode ("wb").
    5. Collects and returns the absolute paths of all saved files.
    
    Parameters:
        files (List[UploadFile]): List of uploaded file objects from the client.
        
    Returns:
        List[str]: A list of absolute file paths pointing to where the files were saved.
    """
    saved_files = []
    
    for file in files:
        # Construct the full path where this file will live on the filesystem
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        # Open the file in write-binary mode ("wb") because PDFs are binary files
        with open(file_path, "wb") as f:
            # file.file is the underlying SpooledTemporaryFile provided by Starlette/FastAPI.
            # .read() extracts all bytes from the upload buffer.
            f.write(file.file.read())
            
        saved_files.append(file_path)
        
    return saved_files

