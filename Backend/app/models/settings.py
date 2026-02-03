"""
RAG Settings Model for MongoDB
"""
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class RAGSettings(BaseModel):
    """RAG settings document model"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    chunk_size: int = 1000
    chunk_overlap: int = 200
    temperature: float = 0.7
    top_p: float = 1.0
    top_k: int = 4
    model_name: str = "gpt-3.5-turbo"

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }
