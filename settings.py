from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central, typed application configuration loaded from .env file"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra = "ignore"
    )
    
    # ------------------------------------------------------------------------------------------------------
    # OpenRouter
    # ------------------------------------------------------------------------------------------------------
    openrouter_api_key: str = Field(..., alias = "OPENROUTER_API_KEY")
    openrouter_model: str = Field(
        default = "openrouter/free",
        alias = "OPENROUTER_MODEL",
    )
    
    openrouter_base_url: str = Field(
        default = "https://openrouter.ai/api/v1",
        alias = "OPENROUTER_BASE_URL",
    )
    
    # ------------------------------------------------------------------------------------------------------
    #   Qdrant Database Configuration
    # ------------------------------------------------------------------------------------------------------
    qdrant_host: str = Field(default="localhost", alias="QDRANT_HOST")
    qdrant_port: int = Field(default=6333, alias="QDRANT_PORT")
    qdrant_collection: str = Field(
        default = "transcripts",
        alias = "QDRANT_COLLECTION"
    )
    
    # ------------------------------------------------------------------------------------------------------
    #   Local Embeddings
    # ------------------------------------------------------------------------------------------------------
    embedding_model: str = Field(
        default = "sentence-transformers/all-mpnet-base-v2",
        alias = "EMBEDDING_MODEL"
    )
    
    # ------------------------------------------------------------------------------------------------------
    #   Local ReRanker
    # ------------------------------------------------------------------------------------------------------
    reranker_model: str = Field(
        default = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        alias = "RERANKER_MODEL",
    )
    
    # ------------------------------------------------------------------------------------------------------
    #   Transcript Ingestion
    # ------------------------------------------------------------------------------------------------------
    transcript_director: str = Field(
        default = "./data/transcripts",
        alias = "TRANSCRIPT_DIRECTORY",
    )
    
    chunk_size: int = Field(default=800, alias = "CHUNK_SIZE")
    chunk_overlap: int = Field(default=120, alias = "CHUNK_OVERLAP")
    
    # ------------------------------------------------------------------------------------------------------
    #   Hybrid Retrieval
    # ------------------------------------------------------------------------------------------------------
    dense_weight: float = Field(default = 0.6, alias = "DENSE_WEIGHT")
    bm25_weight: float = Field(default = 0.4, alias = "BM25_WEIGHT")
    
    retrieval_k: int = Field(default = 20, alias = "RETRIEVAL_K")
    rerank_k: int = Field(default = 5, alias = "RERANK_K")
    

@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings instance."""
    return Settings()

settings = get_settings()