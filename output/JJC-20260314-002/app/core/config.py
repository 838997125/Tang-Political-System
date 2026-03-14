"""Application configuration."""
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:password@localhost:5432/userdb",
        description="PostgreSQL connection URL"
    )
    
    # JWT Configuration
    SECRET_KEY: str = Field(
        default="your-super-secret-key-change-this-in-production",
        description="Secret key for JWT signing"
    )
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Access token expiration time in minutes"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        description="Refresh token expiration time in days"
    )
    
    # Application
    DEBUG: bool = Field(default=False, description="Debug mode")
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "User Registration System"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
