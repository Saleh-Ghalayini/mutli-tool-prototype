# ==============================================================================
# APPLICATION INFO SERVICE
# ==============================================================================
# In software engineering, following the "Service Layer" pattern means business logic
# and data retrieval are separated from HTTP routing logic (routers).
# This service is responsible for retrieving and formatting application information.

from config import settings

def get_app_info():
    """
    Return application metadata for status or info endpoints.
    
    Why separate this from health.py?
    If another part of the system (e.g., CLI, loggers, or admin panels) needs this
    information, they can call get_app_info() directly without simulating an HTTP request.
    
    Returns:
        dict: A dictionary containing the app name, current version, and debug status.
    """
    return {
        "app_name": settings.app_name,
        "version": settings.version,
        "debug": settings.debug
    }

