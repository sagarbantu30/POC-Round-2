from pydantic import BaseModel, Field
from typing import Optional


class RAGSettingsBase(BaseModel):
    chunk_size: int = Field(default=1000, ge=100, le=5000)
    chunk_overlap: int = Field(default=200, ge=0, le=1000)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)
    top_k: int = Field(default=4, ge=1)
    model_name: str = "gpt-3.5-turbo"


class RAGSettingsCreate(RAGSettingsBase):
    pass


class RAGSettingsUpdate(BaseModel):
    chunk_size: Optional[int] = Field(None, ge=100, le=5000)
    chunk_overlap: Optional[int] = Field(None, ge=0, le=1000)
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0)
    top_k: Optional[int] = Field(None, ge=1)
    model_name: Optional[str] = None


class RAGSettingsResponse(RAGSettingsBase):
    id: int

    model_config = {
        "from_attributes": True
    }
