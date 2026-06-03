"""
App Configuration — reads from .env
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os

class Settings(BaseSettings):
    # App
    APP_NAME: str = "MilkyRoots"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production-use-256-bit-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Database (PostgreSQL)
    @property
    def async_database_url(self) -> str:
        """Get the database URL, ensuring it uses the async pg driver."""
        url = os.getenv("DATABASE_URL")
        
        # If we are on Vercel (or production) and URL is missing, FAIL FAST
        if not url:
            # Only allow localhost fallback if explicitly in DEBUG mode locally
            if self.DEBUG:
                url = "postgresql+asyncpg://milkyroots:password@localhost:5432/milkyroots_db"
            else:
                # This will show up in your Vercel logs and as a 500 error
                raise ValueError("CRITICAL ERROR: DATABASE_URL environment variable is MISSING on Vercel.")
            
        # Fix Vercel's 'postgres://' scheme
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://") and "+asyncpg" not in url:
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
            
        return url

    # WhatsApp
    WHATSAPP_SELLER_NUMBER: str = os.getenv("WHATSAPP_SELLER_NUMBER", "918949553581")

    # Pricing (₹) — single source of truth
    PRICE_MILK_PER_LITRE: float = 70.0
    PRICE_CURD_PER_KG: float = 80.0
    PRICE_BUTTERMILK_500ML: float = 20.0
    PRICE_GHEE_500G: float = 900.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
