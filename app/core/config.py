from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "Portfolio Backend API"
    VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    DATABASE_URL: str
    DATABASE_URL_SYNC: str
    
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]
    
    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )



settings = Settings()