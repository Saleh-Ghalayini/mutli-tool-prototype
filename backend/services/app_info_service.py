from config import settings

def get_app_info():
    """Return application metadata for status or info endpoints."""
    return {
        "app_name": settings.app_name,
        "version": settings.version,
        "debug": settings.debug
    }
