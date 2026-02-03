from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DocumentBase(BaseModel):
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    is_company_policy: bool = False


class DocumentCreate(DocumentBase):
    uploaded_by: int


class DocumentUpdate(BaseModel):
    status: Optional[str] = None
    is_company_policy: Optional[bool] = None


class DocumentResponse(DocumentBase):
    id: int
    uploaded_by: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
