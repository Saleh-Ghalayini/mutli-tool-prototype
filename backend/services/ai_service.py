"""
AI Service - Handles AI model inference and text processing
"""

from typing import Optional
from llama_cpp import Llama
from pathlib import Path

class AIService:
    """Service for AI model management and inference"""
    
    def __init__(self, model_path: str):
        self.model_path = Path(model_path)
        self.model: Optional[Llama] = None
    
    def load_model(self) -> None:
        """Load the AI model"""
        if not self.model_path.exists():
            raise RuntimeError(f"Model file not found: {self.model_path}")
        
        try:
            self.model = Llama(
                model_path=str(self.model_path),
                n_ctx=2048,          # Context window
                n_batch=512,         # Batch size for prompt processing  
                n_threads=None,      # Use all available CPU threads
                verbose=False,       # Reduce console spam
                seed=-1,             # Random seed for variety
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None
    
    def generate_text(
        self, 
        prompt: str, 
        max_tokens: int = 300,
        temperature: float = 0.7,
        top_p: float = 0.9,
        stop_sequences: list = None
    ) -> str:
        """Generate text using the loaded model"""
        if not self.model:
            raise RuntimeError("Model not loaded")
        
        if stop_sequences is None:
            stop_sequences = []
        
        try:
            response = self.model(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                echo=False,
                stop=stop_sequences,
                repeat_penalty=1.1,
            )
            
            return response['choices'][0]['text'].strip()
        except Exception as e:
            raise RuntimeError(f"Text generation failed: {e}")
    
    def unload_model(self) -> None:
        """Unload the model to free memory"""
        self.model = None
