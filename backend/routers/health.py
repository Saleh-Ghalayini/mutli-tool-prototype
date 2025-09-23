# ==============================================================================
# HEALTH CHECK ROUTER
# ==============================================================================
# In cloud deployments, microservices, and desktop apps, systems need a quick,
# lightweight way to ask the backend: "Are you alive and running properly?"
# This router provides that endpoint.

from fastapi import APIRouter
from services.app_info_service import get_app_info

# APIRouter is FastAPI's way to group related API paths together.
# It acts like a mini-application that gets plugged into the main app in main.py.
router = APIRouter()

@router.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint:
    - HTTP Method: GET
    - Path: /health
    - Tags: ["Health"] (used for organizing categories in Swagger UI docs)
    
    Returns:
        JSON response with {"status": "ok"} merged with metadata like
        app_name, version, and debug mode via dictionary unpacking (**).
        Example response:
        {
            "status": "ok",
            "app_name": "Policy Prototype Backend",
            "version": "0.1.0",
            "debug": true
        }
    """
    # The double-star (**) operator is Python's dictionary unpacking.
    # It takes key-value pairs from get_app_info() and unpacks them into this new dict.
    return {"status": "ok", **get_app_info()}

