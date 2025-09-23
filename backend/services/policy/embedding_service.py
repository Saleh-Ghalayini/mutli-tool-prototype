
# ==============================================================================
# VECTOR EMBEDDING SERVICE
# ==============================================================================
# Embeddings are the bridge between human language and mathematical search.
#
# What is a Text Embedding?
# An embedding is a list of floating-point numbers (a high-dimensional vector)
# that represents the semantic "meaning" of a text string.
#
# Why "all-MiniLM-L6-v2"?
# 1. Compact: It is an 80MB model based on the BERT transformer architecture.
# 2. Fast: Extremely fast inference on ordinary CPUs without needing an Nvidia GPU.
# 3. 384 Dimensions: It outputs a 384-element vector for any input text.
# 4. Semantic Matching: Sentences with synonymous meanings have vectors pointing
#    in nearly the same mathematical direction.
#    Example: "Company holidays" and "Paid vacation days" will have high cosine similarity,
#    even though they share zero identical words!

from typing import List
from sentence_transformers import SentenceTransformer

# ------------------------------------------------------------------------------
# Load the Model Once (Module-Level Caching)
# ------------------------------------------------------------------------------
# Loading a transformer model into memory takes several hundred megabytes of RAM
# and 1-2 seconds of startup time.
# By loading it once at module import, all subsequent requests can use the existing
# in-memory model instantly without reloading.
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks: List[str]) -> List[List[float]]:
    """
    Convert a list of text strings (chunks or search queries) into vector embeddings.

    Parameters:
        chunks (List[str]): A list of text passages or user queries, e.g.:
                            ["Employees receive 15 days of PTO.", "Health insurance benefits..."]

    Returns:
        List[List[float]]: A 2D list of floating point numbers.
                           Each inner list has exactly 384 floats representing that chunk's vector coordinate.
                           Example shape: [len(chunks), 384]
    """
    # model.encode() runs the transformer forward pass:
    # 1. Tokenizes the text into subword token IDs.
    # 2. Passes tokens through 6 self-attention transformer layers.
    # 3. Performs mean pooling over token embeddings to produce a single 384-dim vector.
    # convert_to_numpy=True returns a NumPy array.
    # .tolist() converts the NumPy array into native Python lists of floats for easy JSON serialization.
    return model.encode(chunks, convert_to_numpy=True).tolist()

