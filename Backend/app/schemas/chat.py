from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    query: str
    document_id: Optional[str] = None  # MongoDB ObjectId as string
    use_company_policy: bool = False


class ChatResponse(BaseModel):
    answer: str
    source_documents: list[str] = []
    return_source_documents: bool = True
