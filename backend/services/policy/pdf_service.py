# ==============================================================================
# PDF TEXT EXTRACTION SERVICE
# ==============================================================================
# Responsible for converting binary PDF files into raw, editable Python strings.
#
# Why is this step needed?
# PDF files are complex binary documents consisting of vector drawing commands,
# fonts, compressed streams, and image assets. Large language models (LLMs) and
# embedding models cannot read binary PDFs directly—they require plain text strings.

import os
from typing import List
from PyPDF2 import PdfReader

def extract_text_from_pdfs(file_paths: List[str]) -> List[str]:
    """
    Extract readable text from a list of PDF file paths.
    
    How it works:
    1. Loops through each file path provided.
    2. Verifies that the file actually exists on the filesystem.
    3. Initializes PyPDF2's PdfReader to parse the document structure.
    4. Iterates over every page in the PDF (`reader.pages`).
    5. Calls `page.extract_text()` to pull the embedded text layer from each page.
    6. Joins all pages together with newline characters ("\n") into one continuous document string.
    7. Uses a try/except block to ensure that if one corrupted PDF fails, it does not
       crash the entire application.
       
    Parameters:
        file_paths (List[str]): List of absolute or relative paths to PDF files on disk.
        
    Returns:
        List[str]: A list of strings, where each entry represents the full extracted text
                   of one corresponding PDF document.
    """
    texts = []
    
    for path in file_paths:
        # Check if the file exists on disk
        if not os.path.exists(path):
            print(f"[PDF Service] Warning: File not found at {path}")
            texts.append("")
            continue
            
        try:
            # PdfReader parses the PDF headers, cross-reference table, and page objects
            reader = PdfReader(path)
            
            # Extract text from every page.
            # `page.extract_text() or ""` ensures that if a page has no text (e.g., blank or image),
            # it returns an empty string instead of None, preventing TypeError during .join().
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            texts.append(text)
            
        except Exception as e:
            # If the PDF is encrypted, corrupted, or malformed, log the error and append empty text
            print(f"[PDF Service] Error extracting text from {path}: {e}")
            texts.append("")
            
    return texts

