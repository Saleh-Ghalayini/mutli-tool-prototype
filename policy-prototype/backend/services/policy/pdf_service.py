import os
from typing import List
from PyPDF2 import PdfReader


def extract_text_from_pdfs(file_paths: List[str]) -> List[str]:
    """Extract text from a list of PDF file paths. Returns a list of extracted texts (one per file)."""
    texts = []
    for path in file_paths:
        if not os.path.exists(path):
            texts.append("")
            continue
        try:
            reader = PdfReader(path)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            texts.append(text)
        except Exception as e:
            texts.append("")
    return texts
