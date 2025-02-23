from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    ATTIO_API_KEY: str
    DATABASE_URL: str
    TELEGRAM_API_ID: Optional[str] = None
    TELEGRAM_API_HASH: Optional[str] = None
    BATCH_INTERVAL_MINUTES: int = 60
    
    # Attio specific settings
    TELEGRAM_IDENTIFIER_ATTRIBUTE_ID: str = "9385a09a-0b1e-4683-b153-7726e3f83405"
    
    class Config:
        env_file = ".env"

settings = Settings()
