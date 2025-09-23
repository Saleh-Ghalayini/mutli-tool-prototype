# ==============================================================================
# PROMPT ENGINEERING & RAG CONTEXT ASSEMBLY SERVICE
# ==============================================================================
# In Retrieval-Augmented Generation (RAG), the Large Language Model does not
# search documents directly. Instead, we manually construct a prompt containing:
# 1. System Guardrails: Explicit instructions defining persona and constraints.
# 2. Retrieved Context: The top document excerpts found by cosine similarity.
# 3. User Question: The question asked by the user.
#
# The goal is "Grounding": forcing the AI to act like an open-book test taker who
# can only cite the provided text and is forbidden from guessing or making things up.

from typing import List

def build_rag_prompt(context_chunks: List[str], user_query: str) -> str:
    """
    Build a structured RAG prompt for the LLM by combining retrieved context and the user query.

    Parameters:
        context_chunks (List[str]): The top-scoring text passages retrieved from the vector search.
        user_query (str): The raw question typed by the user in the chat interface.

    Returns:
        str: The complete formatted prompt string sent to the LLM for inference.
    """
    # Join multiple retrieved chunks with distinct visual separators ('\n---\n')
    # so the model clearly perceives where one excerpt ends and the next begins.
    context = '\n---\n'.join(context_chunks)
    
    # Construct the grounded prompt:
    # Notice the strict negative constraints:
    # - "strictly based on the provided company policy documents"
    # - "If the answer cannot be found... state that you do not have enough information"
    # - "Do not invent information"
    # These instructions drastically reduce "hallucinations" (the AI inventing false rules).
    prompt = (
        "You are an AI assistant designed to answer questions strictly based on the provided company policy documents.\n"
        "If the answer to the question cannot be found in the provided context, state that you do not have enough information to answer the question, or that the question is outside the scope of the provided policies. Do not invent information.\n"
        "\nCompany Policy Context:\n---\n"
        f"{context}\n---\n"
        f"User Question: {user_query}\n\nAnswer:"
    )
    return prompt

