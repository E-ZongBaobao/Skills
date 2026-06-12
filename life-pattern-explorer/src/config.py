"""
应用配置
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API
    APP_NAME: str = "AI 人生模式探索器"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # API Keys
    OPENROUTER_API_KEY: str

    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/life_patterns"

    # AI Model
    LLM_MODEL: str = "anthropic/claude-sonnet-4-5"
    EMBEDDING_MODEL: str = "text-embedding-3-large"

    # Pattern Detection
    MIN_RECORDS_FOR_INSIGHT: int = 3
    SIMILARITY_THRESHOLD: float = 0.8

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
