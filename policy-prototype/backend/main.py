from fastapi import FastAPI
from routers import health, policy, search
from config import settings

app = FastAPI(title=settings.app_name, version=settings.version, debug=settings.debug)

# Include routers
app.include_router(health.router)
app.include_router(policy.router)
app.include_router(search.router)
