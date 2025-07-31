import os
import subprocess

# Prepare for llama-cpp-python integration
import llama_cpp

# Path to the quantized LLM model
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../models/phi3-mini.gguf'))
# Path to llama.cpp binary (llama-cli.exe)
LLAMA_CPP_PATH = os.path.join(os.path.dirname(__file__), '../../../llama.cpp/llama-cli.exe')

from typing import Generator

# Global model object for persistent in-memory loading
_llama_model = None

# Model loader function (singleton pattern)
def get_llama_model():
    global _llama_model
    if _llama_model is None:
        print("[llama-cpp-python] Loading model into memory...")
        _llama_model = llama_cpp.Llama(
            model_path=MODEL_PATH,
            n_ctx=2048,  # You can adjust context size as needed
            n_threads=8, # Adjust for your CPU
        )
        print("[llama-cpp-python] Model loaded.")
    return _llama_model

def run_llm(prompt: str, n_predict: int = 256) -> Generator[str, None, None]:
    """
    Run the local quantized LLM (phi3-mini.gguf) on the given prompt and stream the answer using llama.cpp.
    Yields output lines as they are produced.
    """
    print("\n========== LLM PROMPT SENT TO LLAMA.CPP ==========")
    print(prompt)
    print("========== END OF PROMPT ==========")
    # Use a higher n_predict and a stop sequence for more complete answers
    stop_sequence = "\n== End ==\n"
    try:
        model = get_llama_model()
        output_stream = model(
            prompt=prompt + stop_sequence,  # Encourage model to end with stop
            max_tokens=384,
            temperature=0.7,
            stream=True,
            stop=[stop_sequence]
        )
        for chunk in output_stream:
            if 'choices' in chunk and len(chunk['choices']) > 0:
                yield chunk['choices'][0]['text']
    except Exception as e:
        yield f"[llama-cpp-python exception: {e}]"
