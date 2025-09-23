# ==============================================================================
# LOCAL LLM INFERENCE SERVICE (LLAMA.CPP & GGUF)
# ==============================================================================
# This service is the "brain" of the application. It runs a local Large Language
# Model directly on the computer's CPU—without internet and without sending any
# sensitive company data to external cloud providers.
#
# Key Technologies:
# 1. GGUF (GPT-Generated Unified Format):
#    A binary file format designed by Georgi Gerganov (author of llama.cpp).
#    It stores neural network weights that have been "quantized" (compressed,
#    e.g. from 16-bit floats down to 4-bit integers).
# 2. Microsoft Phi-3 Mini:
#    A state-of-the-art 3.8-billion parameter small language model trained by Microsoft.
#    Despite its small footprint (~2.4 GB in 4-bit quantization), it rivals much larger
#    models on reasoning and reading comprehension benchmarks.
# 3. llama-cpp-python:
#    Python bindings for llama.cpp, executing high-speed C/C++ matrix multiplication
#    optimized for CPU instruction sets (AVX2/AVX-512).

import os
import subprocess
import llama_cpp
from typing import Generator

# ------------------------------------------------------------------------------
# Model & Binary File Paths
# ------------------------------------------------------------------------------
# Absolute path to the quantized GGUF weights file on disk
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../models/phi3-mini.gguf'))

# Path to the standalone llama-cli executable (retained from early CLI testing)
LLAMA_CPP_PATH = os.path.join(os.path.dirname(__file__), '../../../llama.cpp/llama-cli.exe')

# ------------------------------------------------------------------------------
# Global Model Reference (Singleton Pattern)
# ------------------------------------------------------------------------------
# In machine learning, loading model weights from disk into RAM is expensive:
# Reading a 2.4 GB file into memory takes 3-10 seconds.
# By keeping a global variable `_llama_model` initialized to None, we can ensure
# the model is loaded into memory only ONCE on the first query and kept resident.
_llama_model = None

def get_llama_model():
    """
    Model loader function implementing the Singleton Pattern.
    
    If the model is already in RAM, it returns the existing instance immediately.
    If it has not been loaded yet, it instantiates llama_cpp.Llama and caches it.
    
    Parameters configured:
    - model_path: Absolute path to the phi3-mini.gguf file.
    - n_ctx=2048: Context window size (maximum total tokens for prompt + response).
    - n_threads=8: Number of CPU threads dedicated to parallel matrix multiplication.
    """
    global _llama_model
    if _llama_model is None:
        print("[llama-cpp-python] Loading model into memory...")
        _llama_model = llama_cpp.Llama(
            model_path=MODEL_PATH,
            n_ctx=2048,  # Context window size in tokens
            n_threads=8, # Number of CPU threads to utilize
        )
        print("[llama-cpp-python] Model loaded successfully.")
    return _llama_model

def run_llm(prompt: str, n_predict: int = 256) -> Generator[str, None, None]:
    """
    Run local quantized inference on the prompt and stream the answer token-by-token.
    
    Why use a Generator (`yield`)?
    Traditional functions compute the entire 100-word answer, wait 5-10 seconds,
    and return the whole string at once.
    A Python Generator uses the `yield` keyword to emit each word/token the millisecond
    it is generated. This creates the classic real-time "typing" effect in the UI.

    Parameters:
        prompt (str): The full context-grounded prompt constructed by prompt_service.
        n_predict (int): Default token limit parameter.

    Yields:
        str: Individual text tokens/words as they are produced by the neural network.
    """
    print("\n========== LLM PROMPT SENT TO LLAMA.CPP ==========")
    print(prompt)
    print("========== END OF PROMPT ==========")
    
    # Sequence that signals the LLM to stop generating text
    stop_sequence = "\n== End ==\n"
    
    try:
        model = get_llama_model()
        
        # Invoke the model for text generation:
        # - max_tokens=384: Maximum number of new tokens the model is allowed to generate
        # - temperature=0.7: Controls randomness (0.0 = deterministic/rigid, 1.0 = creative)
        # - stream=True: Instructs llama.cpp to yield tokens incrementally instead of blocking
        # - stop=[stop_sequence]: Halts generation if this exact string is produced
        output_stream = model(
            prompt=prompt + stop_sequence,  # Stop token marker
            max_tokens=384,
            temperature=0.7,
            stream=True,
            stop=[stop_sequence]
        )
        
        # Iterate over the stream of generated token chunks
        for chunk in output_stream:
            # Each chunk is a dictionary like:
            # {'id': ..., 'choices': [{'text': ' word', 'index': 0, 'finish_reason': None}]}
            if 'choices' in chunk and len(chunk['choices']) > 0:
                # Yield the newly produced token string directly to FastAPI's StreamingResponse
                yield chunk['choices'][0]['text']
                
    except Exception as e:
        # If an error occurs (e.g. out of memory or corrupted file), yield the error description
        yield f"[llama-cpp-python exception: {e}]"

