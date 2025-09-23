# Import BaseSettings from pydantic_settings.
# Pydantic is a data validation library that ensures settings have the correct data types
# and can automatically load values from environment variables or a .env file.
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Settings Class:
    Centralized configuration repository for the backend application.
    By inheriting from BaseSettings, Pydantic will check if an environment variable
    with the same name exists (e.g., APP_NAME, DEBUG). If found, it uses that value;
    otherwise, it falls back to the default values specified below.
    """
    # The human-readable name of the backend application displayed in API documentation (Swagger UI)
    app_name: str = "Policy Prototype Backend"
    
    # Semantic versioning of the backend service (Major.Minor.Patch)
    version: str = "0.1.0"
    
    # Debug flag: when True, provides detailed error traces and auto-reloads during local development
    debug: bool = True

    class Config:
        # Specifies the path to the optional environment file.
        # If a file named '.env' exists in the working directory, Pydantic will read it automatically.
        env_file = ".env"

# Instantiate a single global instance of Settings (Singleton pattern).
# Other modules across the backend can import 'settings' directly without re-reading files or re-validating.
settings = Settings()

