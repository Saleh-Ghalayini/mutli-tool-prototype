from fastapi import FastAPI
from routers import health
from config import settings

app = FastAPI(title=settings.app_name, version=settings.version, debug=settings.debug)

# Include routers
app.include_router(health.router)
