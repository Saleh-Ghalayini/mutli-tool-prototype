workflow.

Here is a step-by-step guide to the entire process:

1. Application Startup
When you launch the application, the Tauri framework takes charge.

Tauri Backend (main.rs): The Rust-based Tauri backend starts up. Its primary role is to create a native window for the user interface.
Python Sidecar: The Tauri configuration in tauri.conf.json is set up to spawn the Python FastAPI server as a "sidecar" process. This means the Python backend starts automatically and runs alongside the main desktop application.
Frontend Loading: The native window created by Tauri loads the Vue.js single-page application from the frontend directory. The entry point for this is index.html, which then loads main.ts to initialize the Vue app.
2. User Interface and Initial State
The main user interface is defined in App.vue.

UI Components: The UI is composed of several Vue components:
ChatContainer.vue: Displays the conversation history.
InputArea.vue: Provides the text box and buttons for user input, including sending messages and uploading files.
MessageBubble.vue: Renders individual messages in the chat.
LoadingIndicator.vue: Shows a visual cue when the application is processing.
API Service: The frontend communicates with the Python backend through apiService.ts. This service uses axios to make HTTP requests to the FastAPI server running on http://127.0.0.1:8000.
3. The RAG Workflow: Uploading and Processing a Policy Document
The core functionality revolves around a user uploading a document (e.g., a PDF policy document) and then asking questions about it.

File Upload (Frontend):

The user clicks an "Upload" button in the InputArea.vue component.
This triggers the uploadPolicy function in apiService.ts, which sends the selected file to the backend endpoint /api/policy/upload.
File Processing (Backend):

The request hits the upload_policy_pdf function in the policy.py router.
The uploaded PDF is saved to the uploads directory by the file_service.py.
The text content is extracted from the PDF using pdf_service.py.
The extracted text is split into smaller, manageable "chunks" by chunking_service.py.
The embedding_service.py then converts each text chunk into a numerical vector (an embedding) using a pre-trained model.
Finally, vector_store_service.py saves these chunks and their corresponding embeddings into a default_client_embeddings.jsonl file inside vector_store. This file acts as your local vector database.
4. The RAG Workflow: Asking a Question
Once a document has been processed and its embeddings are stored, the user can ask questions.

Sending a Query (Frontend):

The user types a question into the InputArea.vue and hits "Send".
This calls the searchPolicy function in apiService.ts, which sends the user's query to the /api/search/ endpoint.
Query Processing (Backend):

The request is handled by the search_policy function in search.py.
The backend first converts the user's question into an embedding using the same embedding_service.py.
It then loads all the document chunk embeddings from the vector_store_service.py.
A similarity search is performed to find the document chunks that are most semantically similar to the user's question.
The prompt_service.py takes the user's original question and the most relevant document chunks and combines them into a single, comprehensive prompt. This prompt is specifically structured to guide the LLM in generating a relevant answer based on the provided context.
LLM Inference:

The generated prompt is sent to the llm_service.py.
This service uses the llama-cpp-python library to load the local phi3-mini.gguf model from the models directory.
It runs the model with the prompt to generate an answer. The response is streamed back token-by-token to provide a real-time, "typing" effect in the UI.
Displaying the Response (Frontend):

The searchPolicy function in the frontend receives the streamed response from the backend.
As each token arrives, it is appended to a MessageBubble.vue component within the ChatContainer.vue, allowing the user to see the answer being generated in real-time.
This entire cycle, from document upload to question answering, constitutes a complete RAG pipeline, enabling the application to answer questions based on documents it has never seen before, all while running locally on your machine.