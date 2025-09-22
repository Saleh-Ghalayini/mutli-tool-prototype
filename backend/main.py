from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import health, policy, search
from config import settings

app = FastAPI(title=settings.app_name, version=settings.version, debug=settings.debug)

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(policy.router)
app.include_router(search.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
