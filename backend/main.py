#!/usr/bin/env python3
"""
Multi-Tool AI Platform - Backend
Fast, reliable LLM inference with GGUF support using llama-cpp-python
"""

from pathlib import Path
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import services
from services.ai_service import AIService
from services.file_service import FileService
from services.summarization_service import SummarizationService

# Configuration
MODEL_PATH = Path("models/phi3-mini.gguf")

# Global services
ai_service = AIService(str(MODEL_PATH))
file_service = FileService()
summarization_service = SummarizationService(ai_service, file_service)

class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 256
    temperature: Optional[float] = 0.7

class GenerateResponse(BaseModel):
    response: str
    success: bool
    error: Optional[str] = None

class SummarizeResponse(BaseModel):
    summary: str
    success: bool
    error: Optional[str] = None
    original_length: Optional[int] = None
    summary_length: Optional[int] = None
    compression_ratio: Optional[float] = None
    strategy_used: Optional[str] = None
    processing_type: Optional[str] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model on startup, clean up on shutdown"""
    
    print("🚀 Loading Phi-3 model...")
    if not MODEL_PATH.exists():
        print(f"❌ Model file not found: {MODEL_PATH}")
        print("Please ensure phi3-mini.gguf is in the parent directory")
        raise RuntimeError(f"Model file not found: {MODEL_PATH}")
    
    try:
        ai_service.load_model()
        print("✅ Model loaded successfully!")
        
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        raise RuntimeError(f"Failed to load model: {e}")
    
    yield
    
    # Cleanup
    print("🔄 Shutting down...")
    ai_service.unload_model()

# Create FastAPI app
app = FastAPI(
    title="Multi-Tool AI Platform",
    description="Backend for LLM inference with GGUF support",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware for Tauri frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://tauri.localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Multi-Tool AI Platform Backend",
        "status": "ready",
        "model_loaded": ai_service.is_model_loaded()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy" if ai_service.is_model_loaded() else "model_not_loaded",
        "model_path": str(MODEL_PATH),
        "model_exists": MODEL_PATH.exists(),
        "model_loaded": ai_service.is_model_loaded(),
        "temp_dir": str(file_service.temp_dir)
    }

@app.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """Generate text using the loaded LLM"""
    if not ai_service.is_model_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        generated_text = ai_service.generate_text(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            stop_sequences=["\n\n", "Human:", "User:"]
        )
        
        return GenerateResponse(
            response=generated_text,
            success=True
        )
        
    except Exception as e:
        return GenerateResponse(
            response="",
            success=False,
            error=str(e)
        )

@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    """Upload and save file for processing"""
    return file_service.save_uploaded_file(file)

@app.post("/summarize_pdf", response_model=SummarizeResponse)
async def summarize_pdf(request: dict):
    """Summarize a PDF file"""
    if not ai_service.is_model_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    result = summarization_service.summarize_pdf(request)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return SummarizeResponse(**result)

@app.post("/chat")
async def chat_completion(request: GenerateRequest):
    """Chat-style completion (alias for generate for compatibility)"""
    return await generate_text(request)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,  # Set to True for development
        log_level="info"
    )
