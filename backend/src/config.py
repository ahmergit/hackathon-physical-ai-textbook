"""
Application configuration using pydantic-settings.
Loads environment variables from .env file.
"""

from typing import List
from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str

    # Authentication & Security
    secret_key: str
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    # SendGrid Email Service
    sendgrid_api_key: str
    from_email: EmailStr
    from_name: str = "Physical AI Learning Platform"

    # Google OAuth
    google_client_id: str
    google_client_secret: str

    # Frontend URLs
    frontend_url: str = "http://localhost:3000"
    email_verification_url: str = "http://localhost:3000/verify-email"

    # Environment
    environment: str = "development"

    # CORS
    cors_origins: str = "http://localhost:3000"

    # Server Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    # Chatbot Configuration
    openai_api_key: str
    qdrant_url: str
    qdrant_api_key: str = ""
    qdrant_collection_name: str = "physical-ai-textbook"
    chat_model: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-small"
    max_tokens: int = 8000
    embedding_dimension: int = 1536
    chunk_size: int = 512
    chunk_overlap: int = 64
    
    @property
    def qdrant_collection(self) -> str:
        """Alias for qdrant_collection_name for backward compatibility."""
        return self.qdrant_collection_name


    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment.lower() == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"


# Global settings instance
settings = Settings()
