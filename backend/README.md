# Multi-Tool AI Platform - Python Backend

A fast, reliable Python backend for LLM inference using `llama-cpp-python` with native GGUF support.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Ensure Model is Available

The model is included in the `models/` directory:

```
backend/
├── models/
│   └── phi3-mini.gguf      # Your 2.3GB GGUF model
├── main.py
└── requirements.txt
```

### 3. Run the Server

```bash
python main.py
```

The server will start on `http://127.0.0.1:8000`

## 📡 API Endpoints

### Health Check

- `GET /` - Basic health check
- `GET /health` - Detailed system status

### LLM Inference

- `POST /generate` - Generate text from prompt
- `POST /chat` - Chat completion (alias for generate)

### File Processing

- `POST /upload_file` - Upload files for processing
- `POST /summarize_pdf` - Summarize PDF documents

## 🔧 Configuration

### Model Loading

The server automatically loads your Phi-3 model on startup with optimized settings:

- Context window: 2048 tokens
- CPU optimization: All available threads
- Batch processing: 512 tokens

### Performance Tips

For better CPU performance, reinstall llama-cpp-python with BLAS:

```bash
CMAKE_ARGS="-DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS" pip install --upgrade --force-reinstall llama-cpp-python
```

## 🔗 Integration with Tauri

Your existing Tauri frontend just needs to change the HTTP calls from:

```javascript
// Old (Rust backend)
await invoke("generate_ai_response", { prompt: "Hello" });

// New (Python backend)
await fetch("http://127.0.0.1:8000/generate", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ prompt: "Hello", max_tokens: 256 }),
});
```

## 🛠️ Development

### Hot Reload

For development with hot reload:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### API Documentation

Once running, visit:

- `http://127.0.0.1:8000/docs` - Interactive Swagger UI
- `http://127.0.0.1:8000/redoc` - ReDoc documentation

## ✅ Advantages

✅ **Native GGUF Support** - Works perfectly with Phi-3 model  
✅ **No Build Issues** - No C++ compilation headaches  
✅ **Fast Performance** - Optimized llama.cpp backend  
✅ **Easy Integration** - Simple HTTP API  
✅ **Rich Ecosystem** - Full Python LLM ecosystem  
✅ **Auto Documentation** - FastAPI generates docs automatically  
✅ **Type Safety** - Pydantic models for validation  
✅ **CORS Ready** - Works seamlessly with Tauri frontend
