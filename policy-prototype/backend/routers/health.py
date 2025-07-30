from fastapi import APIRouter
from services.app_info_service import get_app_info

router = APIRouter()

@router.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint with app metadata."""
    return {"status": "ok", **get_app_info()}
