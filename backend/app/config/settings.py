from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import json

class Settings(BaseSettings):
    """
    Application settings, loaded from environment variables and .env file.
    """
    app_name: str = "Deep Research Agent"
    app_version: str = "1.0.0"
    environment: str = "development"
    
    host: str = "0.0.0.0"
    port: int = 8000
    
    log_level: str = "INFO"
    
    cors_origins: str = '["http://localhost:5173", "http://localhost:3000", "*"]'
    
    # Gemini Configuration
    google_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    gemini_temperature: float = 0.0
    gemini_max_tokens: int = 8192
    gemini_timeout: float = 30.0
    gemini_max_retries: int = 3
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    
    @property
    def get_cors_origins(self) -> List[str]:
        return json.loads(self.cors_origins)

settings = Settings()
