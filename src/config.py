"""Configuration management for TurboAssist AI."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI
    openai_api_key: str
    openai_embedding_model: str = "text-embedding-3-small"
    openai_llm_model: str = "gpt-4o-mini"
    
    # Azure Search (optional)
    azure_search_endpoint: Optional[str] = None
    azure_search_key: Optional[str] = None
    azure_search_index: str = "turboassist-index"
    
    # Application
    environment: str = "development"
    log_level: str = "INFO"
    max_chunk_size: int = 512
    chunk_overlap: int = 50
    top_k_retrieval: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
