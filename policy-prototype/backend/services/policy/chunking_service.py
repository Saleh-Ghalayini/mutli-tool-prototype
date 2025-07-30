from typing import List
import re

def chunk_text(text: str, max_length: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into chunks of up to max_length characters, with optional overlap.
    Chunks are split on sentence boundaries if possible.
    """
    # Split into sentences
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = []
    current_length = 0
    for sentence in sentences:
        if current_length + len(sentence) > max_length and current_chunk:
            chunk = ' '.join(current_chunk)
            chunks.append(chunk)
            # Overlap: keep last N characters
            if overlap > 0 and len(chunk) > overlap:
                overlap_text = chunk[-overlap:]
                current_chunk = [overlap_text]
                current_length = len(overlap_text)
            else:
                current_chunk = []
                current_length = 0
        current_chunk.append(sentence)
        current_length += len(sentence) + 1
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    return chunks
