from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore
from functools import lru_cache

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Jawnt Banking API"
    VERSION: str = "1.0.0"
    PORT: int = 8001  # Added port configuration
    
    # Plaid Settings
    PLAID_CLIENT_ID: str = "6758563294bbe4001b5c5279"
    PLAID_SECRET: str = "386a94d4b632d57fe91b7b0f8506b3"
    PLAID_ENV: str = "sandbox"
    
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="allow"  # Allow extra fields from .env file
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings() 