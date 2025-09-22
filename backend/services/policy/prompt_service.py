from typing import List

def build_rag_prompt(context_chunks: List[str], user_query: str) -> str:
    """
    Build a RAG prompt for the LLM using the retrieved context chunks and user query.
    """
    context = '\n---\n'.join(context_chunks)
    prompt = (
        "You are an AI assistant designed to answer questions strictly based on the provided company policy documents.\n"
        "If the answer to the question cannot be found in the provided context, state that you do not have enough information to answer the question, or that the question is outside the scope of the provided policies. Do not invent information.\n"
        "\nCompany Policy Context:\n---\n"
        f"{context}\n---\n"
        f"User Question: {user_query}\n\nAnswer:"
    )
    return prompt
