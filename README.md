# Multi-Tool AI Prototype

A full-stack offline AI-powered policy document search and question-answering system built with FastAPI and Vue.js.

## Overview

This application allows users to upload PDF policy documents, processes them into a searchable knowledge base, and provides real-time AI-powered answers to questions about the content. The system operates entirely offline using local AI models, ensuring data privacy and security.

## Architecture

### Backend (FastAPI)

- RESTful API with streaming response support
- Offline AI inference using llama-cpp-python
- Vector similarity search for document retrieval
- PDF text extraction and processing
- Retrieval-Augmented Generation (RAG) implementation

### Frontend (Vue.js 3)

- Real-time chat interface with streaming responses
- Dark theme optimized for extended use
- Responsive design with modern UI components
- TypeScript support for type safety

## Tech Stack

### Backend Technologies

- **FastAPI**: Modern Python web framework for building APIs
- **llama-cpp-python**: Python bindings for llama.cpp, enables local LLM inference
- **sentence-transformers**: Pre-trained models for text embeddings
- **PyPDF2**: PDF text extraction library
- **NumPy**: Mathematical operations for vector similarity
- **Uvicorn**: ASGI server for production deployment
- **Pydantic**: Data validation and settings management

### Frontend Technologies

- **Vue.js 3**: Progressive JavaScript framework with Composition API
- **Vite**: Fast build tool and development server
- **TypeScript**: Type-safe JavaScript for better development experience
- **Axios**: HTTP client for API communication

### AI Models

- **Microsoft Phi-3 Mini**: Quantized GGUF model for text generation
- **all-MiniLM-L6-v2**: Sentence transformer for text embeddings

## Data Processing Pipeline

### 1. Document Upload

```
PDF Files → File Storage → Text Extraction → Chunking → Embedding → Vector Store
```

### 2. Query Processing

```
User Query → Embedding → Similarity Search → Context Retrieval → LLM Generation → Streaming Response
```

## Core Components

### Text Chunking

The system splits documents into manageable chunks using sentence boundaries:

- **Max Length**: 500 characters per chunk
- **Overlap**: 50 characters between consecutive chunks
- **Strategy**: Sentence-aware splitting to preserve context
- **Purpose**: Optimizes embedding quality and retrieval accuracy

### Embedding Generation

Text chunks are converted to vector representations:

- **Model**: all-MiniLM-L6-v2 (384-dimensional vectors)
- **Purpose**: Enables semantic similarity search
- **Storage**: JSON Lines format for efficient loading
- **Encoding**: Real-time embedding for user queries

### Vector Similarity Search

Retrieves relevant document chunks:

- **Algorithm**: Cosine similarity between query and chunk embeddings
- **Top-K Selection**: Returns 3 most relevant chunks by default
- **Scoring**: Normalized similarity scores (0-1 range)
- **Performance**: In-memory operations for fast retrieval

### Knowledge Base Management

- **Client Isolation**: Separate vector stores per client
- **Persistence**: File-based storage in `policy_data/vector_store/`
- **Format**: JSON Lines with chunk text and embeddings
- **Scalability**: Efficient loading and updating of embeddings

### Tokenization and Text Processing

- **PDF Extraction**: PyPDF2 handles various PDF formats
- **Text Normalization**: Preserves formatting while cleaning content
- **Sentence Detection**: Regex-based sentence boundary detection
- **Overlap Handling**: Maintains context continuity across chunks

### LLM Integration

Local AI model handling:

- **Model Loading**: Singleton pattern for memory efficiency
- **Context Window**: 2048 tokens maximum
- **Threading**: Multi-threaded inference for performance
- **Streaming**: Real-time token generation with yield
- **Memory Management**: Persistent model loading to avoid reload delays

### I/O Operations

#### File Handling

- **Upload Processing**: Multi-file support with validation
- **Storage Strategy**: Organized directory structure
- **Format Support**: PDF documents with text content
- **Error Handling**: Graceful handling of corrupted or unsupported files

#### API Communication

- **Request/Response**: JSON format for structured data
- **Streaming**: Server-Sent Events for real-time responses
- **CORS**: Configured for frontend-backend communication
- **Error Handling**: HTTP status codes with detailed error messages

#### Database Operations

- **Vector Storage**: File-based JSON Lines format
- **Query Processing**: In-memory loading for fast access
- **Data Integrity**: Validation of embeddings and metadata
- **Backup Strategy**: File-based storage enables easy backup

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Git

### Backend Setup

1. Navigate to the backend directory:

```bash
cd backend
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Download the AI model:
   Place `phi3-mini.gguf` in the `models/` directory at the project root.

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

## Usage

### Starting the Application

1. Start the backend server:

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Start the frontend development server:

```bash
cd frontend
npm run dev
```

3. Access the application at `http://localhost:5173`

### Using the System

#### Document Upload

Use the API endpoint to upload PDF documents:

```bash
curl -X POST "http://localhost:8000/policy/upload" \
     -H "Content-Type: multipart/form-data" \
     -F "files=@your-policy.pdf"
```

#### Interactive Chat

1. Open the web interface
2. Type questions about your uploaded documents
3. Receive real-time AI responses based on document content

## API Endpoints

### Health Check

- **GET** `/health` - Application health status

### Document Management

- **POST** `/policy/upload` - Upload PDF documents for processing

### Search and Query

- **GET** `/policy/search?query=<your_question>` - Search documents and get AI responses

## Configuration

### Backend Settings

Configuration is managed through `config.py`:

- Application name and version
- Debug mode settings
- Environment variable support

### Model Configuration

LLM settings in `llm_service.py`:

- Context window size (n_ctx)
- Thread count for inference
- Model path configuration

### Frontend Configuration

Vite configuration in `vite.config.ts`:

- Development server settings
- Build optimization
- Plugin configuration

## Development

### Project Structure

```
mutli-tool-prototype/
├── backend/                    # FastAPI backend
│   ├── routers/               # API route handlers
│   ├── services/              # Business logic
│   │   └── policy/           # Policy-specific services
│   ├── main.py               # Application entry point
│   ├── config.py             # Configuration settings
│   └── requirements.txt      # Python dependencies
├── frontend/                  # Vue.js frontend
│   ├── src/
│   │   ├── components/       # Vue components
│   │   ├── services/         # API communication
│   │   └── style.css        # Global styles
│   ├── package.json          # Node.js dependencies
│   └── vite.config.ts       # Build configuration
├── models/                   # AI model files
├── policy_data/             # Document storage and vector DB
└── llama.cpp/              # LLM inference binaries
```

### Adding New Features

1. Backend: Create new routers and services
2. Frontend: Add components and update API services
3. Testing: Use the health endpoint for connectivity verification

## Performance Considerations

### Memory Usage

- LLM model loaded once and reused
- Vector embeddings cached in memory
- Efficient chunk processing

### Response Times

- Streaming responses for immediate feedback
- Optimized vector similarity calculations
- Local inference eliminates network latency

### Scalability

- Stateless API design
- File-based storage for easy scaling
- Configurable chunk sizes and model parameters

## Troubleshooting

### Common Issues

1. **Model not found**: Ensure `phi3-mini.gguf` is in the `models/` directory
2. **CORS errors**: Verify backend CORS configuration
3. **Slow responses**: Check available system memory and CPU cores
4. **Upload failures**: Confirm PDF files contain extractable text

### Performance Optimization

- Increase thread count for faster inference
- Adjust chunk size based on document characteristics
- Monitor memory usage with large document sets

## License

This project is open source and available under the MIT License.
