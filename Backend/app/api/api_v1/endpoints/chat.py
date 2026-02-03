"""
Chat Endpoints
RAG-based chat with documents using MongoDB
"""
from fastapi import APIRouter, Depends
from app.schemas.chat import ChatRequest, ChatResponse
from app.api.api_v1.endpoints.auth import get_current_user
from app.services.rag_service import RAGService

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """Chat with documents using RAG"""
    rag_service = RAGService()
    
    answer, source_documents = await rag_service.chat(
        query=chat_request.query,
        document_id=chat_request.document_id,
        use_company_policy=chat_request.use_company_policy
    )
    
    return ChatResponse(
        answer=answer,
        source_documents=source_documents,
        return_source_documents=True
    )
