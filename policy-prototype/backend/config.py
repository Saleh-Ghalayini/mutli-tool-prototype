from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Policy Prototype Backend"
    version: str = "0.1.0"
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
