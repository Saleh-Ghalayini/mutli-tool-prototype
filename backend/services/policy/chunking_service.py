# ==============================================================================
# TEXT CHUNKING SERVICE
# ==============================================================================
# In Retrieval-Augmented Generation (RAG), chunking is the process of breaking a
# massive document into smaller, self-contained paragraphs or passages.
#
# Why is chunking necessary?
# 1. Embedding Model Limitations: Embedding models (like MiniLM) can only process
#    a limited number of tokens at once (e.g., 256 or 512 tokens).
# 2. Precision: If you embed an entire 50-page document into a single vector,
#    the specific answer to a question like "How many sick days do I get?" will be
#    diluted and lost. Chunking ensures that each vector represents a focused topic.
# 3. Context Window Efficiency: When feeding retrieved text into an LLM prompt,
#    we only want to pass the exact relevant paragraphs rather than entire chapters.

from typing import List
import re

def chunk_text(text: str, max_length: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into chunks of up to max_length characters, with optional overlap.
    Chunks are split on natural sentence boundaries (., !, ?) whenever possible.

    Parameters:
        text (str): The raw continuous document text extracted from the PDF.
        max_length (int): Target maximum number of characters per chunk (default: 500 chars,
                          which is roughly 75-100 English words).
        overlap (int): Number of characters to carry over from the end of one chunk to the
                       beginning of the next chunk (default: 50 chars).
                       
    Why use Overlap?
        If an important thought or rule spans across the boundary between two chunks,
        without overlap the context could be severed. Overlap ensures that consecutive
        chunks share boundary context so no critical information falls through the cracks.

    Returns:
        List[str]: A list of text chunk strings ready for embedding.
    """
    # --------------------------------------------------------------------------
    # Step 1: Split Text into Individual Sentences
    # --------------------------------------------------------------------------
    # Regular Expression breakdown:
    # (?<=[.!?]) is a "positive lookbehind assertion":
    # It matches a point immediately preceded by a period, exclamation mark, or question mark,
    # followed by one or more spaces (' +').
    # This splits the text into sentences without deleting the punctuation marks!
    sentences = re.split(r'(?<=[.!?]) +', text)
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    # --------------------------------------------------------------------------
    # Step 2: Accumulate Sentences into Chunks
    # --------------------------------------------------------------------------
    for sentence in sentences:
        # Check if adding this next sentence would exceed our maximum chunk length
        if current_length + len(sentence) > max_length and current_chunk:
            # Join the accumulated sentences with spaces to form the finished chunk
            chunk = ' '.join(current_chunk)
            chunks.append(chunk)
            
            # ------------------------------------------------------------------
            # Step 3: Handle Overlap for the Next Chunk
            # ------------------------------------------------------------------
            # If overlap is configured, take the last 'overlap' characters from the
            # previous chunk and seed the new chunk with them.
            if overlap > 0 and len(chunk) > overlap:
                overlap_text = chunk[-overlap:]
                current_chunk = [overlap_text]
                current_length = len(overlap_text)
            else:
                current_chunk = []
                current_length = 0
                
        # Append the current sentence to our active chunk buffer
        current_chunk.append(sentence)
        current_length += len(sentence) + 1  # +1 accounts for the space when joining
        
    # --------------------------------------------------------------------------
    # Step 4: Flush Remaining Sentences
    # --------------------------------------------------------------------------
    # Don't forget any leftover sentences still in current_chunk at the end of the text
    if current_chunk:
        chunks.append(' '.join(current_chunk))
        
    return chunks

