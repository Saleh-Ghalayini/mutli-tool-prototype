# Policy-Prototype Project Plan

## Overview

A fully offline, client-specific desktop application that leverages an embedded LLM (Phi-3 mini) and RAG (Retrieval Augmented Generation) to answer company policy questions. The app is distributed as an MSI installer, with all models and data pre-baked for each client. Built with Tauri (Rust backend, web frontend) for efficiency and cross-platform support.

---

## 1. Project Structure

- `policy-prototype/`
  - `frontend/` — Web UI (React/Vue/Svelte, etc.)
  - `backend/` — Business logic, PDF parsing, chunking, embedding, RAG, etc. (Python or Rust)
  - `src-tauri/` — Tauri project (Rust, app shell, system integration)
  - `models/` — Pre-baked, quantized LLM (Phi-3 mini, e.g., 4-bit GGUF) and embedding model (e.g., all-MiniLM-L6-v2 ONNX)
  - `policy_data/` — Client-specific vector index and text chunks, structured as `policy_data/[client_id]/`, output from internal scripts
  - `docs/` — Documentation, architecture diagrams, requirements, etc.
  - `scripts/` — Internal tools for PDF ingestion, chunking, embedding, MSI build automation
  - `tests/` — Automated tests for backend, frontend, and integration
  - `config/` — App configuration, client-specific settings, prompt templates

---

## 2. Development Phases

### Phase 1: Requirements & Design

- Finalize requirements with stakeholders
- Define user stories and acceptance criteria
- Design system architecture (RAG pipeline, Tauri integration, update flow)
- Choose frontend stack (React/Vue/Svelte)
- Plan for accessibility, error handling, and update mechanism
- **Consult legal counsel** on LLM licensing (Phi-3, embedding model), data privacy, and liability disclaimers

### Phase 2: Core Infrastructure

- Scaffold Tauri app (Rust + chosen frontend)
- Set up folder structure as above
- Integrate LLM and embedding model loading in Rust
- Implement secure local storage for models and policy data
- **All backend logic (PDF parsing, chunking, embedding, vector search, RAG) should be implemented in Rust** for performance and seamless Tauri integration (avoid Python dependencies)

### Phase 3: Backend & RAG Pipeline

- PDF parsing and chunking (Rust; use crates like `pdf-extract`, `lopdf`)
- Embedding generation (Rust ML inference, e.g., `candle`, `ort` for ONNX, or `llm` for GGUF)
- Vector index creation (prefer `faiss-rs` or `lancedb` for local, persistent vector search)
- RAG retrieval logic (query embedding, similarity search, prompt construction)
- Strict prompt engineering for scope control
- **Specify embedding model** (e.g., all-MiniLM-L6-v2 ONNX, 384-dim)
- **Specify quantization** (e.g., 4-bit GGUF for Phi-3 mini)
- **Chunking strategy:** semantic chunking (by section/paragraph), overlap, and metadata (page, section) for source citation
- **Fallback strategy:** define responses for no relevant chunks, LLM refusal, hallucination, or internal error

### Phase 4: Frontend Development

- Chat UI for Q&A
- Display source citations for answers (show chunk metadata: section, page)
- Loading indicators, error messages, and fallback responses
- Policy browsing/search (optional)
- Branding and client-specific customization
- **Accessibility:** screen reader support, keyboard navigation, color contrast
- **Error reporting:** user-friendly messages, suggest solutions, allow log export

### Phase 5: Packaging & Updates

- Bundle all models, data, and app into MSI installer
- **Automate MSI build for each client** (scripts select correct policy data, inject config/branding, set ProductCode/ProductVersion, sign installer)
- **Installer signing**: use code signing certificate for Windows trust
- Plan for major upgrades (full MSI reinstall for updates)
- Document update process for clients (clear, step-by-step instructions)

### Phase 6: Testing & QA

- Unit and integration tests for backend and frontend
- Performance and memory usage testing on low-spec hardware
- User acceptance testing with sample clients
- Security and privacy review
- **Memory management:** profile RAM usage for LLM and vector index
- **Cold start:** provide splash/loading screen while models load
- **Concurrency:** run LLM inference and RAG on background threads (Tauri async)

### Phase 7: Documentation & Support

- User and admin manuals
- Internal documentation for policy processing pipeline
- Troubleshooting and support procedures
- **EULA/Terms of Service:** formal agreement outlining app limitations, update policy, support, and liability

---

## 3. Key Considerations

- Only one copy of Phi-3 mini and embedding model per app (quantized, e.g., 4-bit GGUF)
- All data and inference fully offline
- Client-specific knowledge base bundled at build time (`policy_data/[client_id]/`)
- Major updates via new MSI installer
- Robust error handling and user feedback
- Security: encryption at rest, signed installers, no data exfiltration
- Accessibility and legal compliance
- **Memory/cold start:** optimize for RAM usage and provide user feedback during model load
- **Proof of Concept:** build a PoC to validate LLM and embedding model inference, RAG, and Tauri integration before full build

---

## 4. Next Steps

1. Create project folder structure
2. Build a PoC: load Phi-3 mini and embedding model in Rust, run a basic RAG query, return result to Tauri frontend
3. Scaffold Tauri app and frontend
4. Begin backend RAG pipeline prototyping
5. Draft UI wireframes and requirements
6. Set up documentation and config templates

---

This plan will be updated as the project progresses. All major decisions and changes should be documented in the `docs/` folder.
