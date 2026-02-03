"""
Application Configuration
Simple configuration for MongoDB-based RAG POC
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from pydantic import field_validator, Field


class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str = "RAG POC Backend"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = Field(default=[])
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str):
            if v.startswith("["):
                import json
                try:
                    return json.loads(v)
                except:
                    return [i.strip() for i in v.split(",") if i.strip()]
            else:
                return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return []
    
    # MongoDB Configuration
    MONGODB_URI: str = "mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority"
    MONGODB_DB_NAME: str = "rag_database"
    MONGODB_COLLECTION_NAME: str = "documents_collection"
    MONGODB_VECTOR_INDEX_NAME: str = "vector_index"

    # PGVector Configuration
    PGVECTOR_CONNECTION: str = "postgresql+psycopg://postgres:postgres@localhost:5432/ragdb"
    PGVECTOR_COLLECTION: str = "rag_documents"
    
    # OpenAI API Key
    OPENAI_API_KEY: str = ""
    
    # RAG Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TEMPERATURE: float = 0.7
    TOP_P: float = 1.0
    TOP_K: int = 4
    MODEL_NAME: str = "gpt-3.5-turbo"
    
    # Security
    SECRET_KEY: str = "change-this-to-a-secure-random-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        json_schema_extra={"BACKEND_CORS_ORIGINS": {"mode": "str"}}
    )


settings = Settings()
