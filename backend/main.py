# ==============================================================================
# MAIN BACKEND APPLICATION ENTRY POINT
# ==============================================================================
# This file initializes the FastAPI application, sets up middleware (CORS),
# registers all endpoint routers, and provides a way to start the web server.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import our custom API route modules from the 'routers' directory:
# - health: endpoint for checking if the server is alive and functioning
# - policy: endpoint for uploading and processing PDF documents
# - search: endpoint for querying documents and streaming AI answers
from routers import health, policy, search

# Import the centralized configuration settings defined in config.py
from config import settings

# ------------------------------------------------------------------------------
# 1. Initialize the FastAPI Application
# ------------------------------------------------------------------------------
# FastAPI automatically generates interactive API documentation (Swagger UI at /docs
# and ReDoc at /redoc) using the title, version, and debug parameters provided here.
app = FastAPI(title=settings.app_name, version=settings.version, debug=settings.debug)

# ------------------------------------------------------------------------------
# 2. Configure Cross-Origin Resource Sharing (CORS) Middleware
# ------------------------------------------------------------------------------
# What is CORS?
# Web browsers enforce a security policy called Same-Origin Policy. By default, a web
# application running on one address (e.g., frontend on http://localhost:3000) is blocked
# from making HTTP requests to a backend on a different port (e.g., http://localhost:8000).
# CORS middleware tells the browser that requests from other origins are allowed.
app.add_middleware(
    CORSMiddleware,
    # allow_origins: Which domains can talk to this backend.
    # ["*"] allows all origins (useful in local development and desktop prototype).
    # In production, this should be restricted to specific URLs like ["https://mycompany.com"].
    allow_origins=["*"],
    # allow_credentials: Allow cookies, authorization headers, etc.
    allow_credentials=True,
    # allow_methods: HTTP methods allowed (GET, POST, PUT, DELETE, OPTIONS, etc.). "*" means all.
    allow_methods=["*"],
    # allow_headers: HTTP headers allowed in the request (Content-Type, Authorization, etc.).
    allow_headers=["*"],
)

# ------------------------------------------------------------------------------
# 3. Register Route Modules (Separation of Concerns)
# ------------------------------------------------------------------------------
# Instead of writing all endpoints in this single file, endpoints are organized
# into modular "routers" in the routers/ folder and mounted onto the main app here.
app.include_router(health.router)  # Mounted: GET /health
app.include_router(policy.router)  # Mounted: POST /policy/upload
app.include_router(search.router)  # Mounted: GET /policy/search

# ------------------------------------------------------------------------------
# 4. Direct Execution Entry Point
# ------------------------------------------------------------------------------
# If this file is run directly (e.g., `python main.py`), Uvicorn (an ASGI web server)
# will start serving the FastAPI app on all network interfaces (0.0.0.0) at port 8000.
if __name__ == "__main__":
    import uvicorn
    # host="0.0.0.0" makes the server accessible across the local network/container.
    # port=8000 is the standard port where the frontend expects the backend to be.
    uvicorn.run(app, host="0.0.0.0", port=8000)

