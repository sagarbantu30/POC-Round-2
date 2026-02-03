"""
Document Management Endpoints
Upload and manage documents for RAG using MongoDB
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from typing import List
from datetime import datetime
from bson import ObjectId
from app.db.session import get_database
from app.api.api_v1.endpoints.auth import get_current_user
from app.services.rag_service import RAGService

router = APIRouter()


@router.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    is_company_policy: bool = False,
    current_user: dict = Depends(get_current_user)
):
    """Upload a document for RAG processing"""
    # Validate file type
    allowed_extensions = ['.pdf', '.docx', '.doc', '.txt']
    file_extension = file.filename.split('.')[-1].lower()
    if f'.{file_extension}' not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    # Read file content
    content = await file.read()
    
    # Create document record in MongoDB
    db = get_database()
    document = {
        "filename": file.filename,
        "original_filename": file.filename,
        "file_type": file_extension,
        "file_size": len(content),
        "is_company_policy": is_company_policy,
        "uploaded_by": str(current_user["_id"]),
        "status": "processing",
        "created_at": datetime.utcnow(),
        "updated_at": None
    }
    result = await db.documents.insert_one(document)
    document_id = str(result.inserted_id)
    
    # Process document in background
    async def process_doc():
        rag_service = RAGService()
        success = await rag_service.process_document(
            content, 
            file.filename, 
            document_id,
            is_company_policy
        )
        await db.documents.update_one(
            {"_id": ObjectId(document_id)},
            {"$set": {"status": "completed" if success else "failed", "updated_at": datetime.utcnow()}}
        )
    
    background_tasks.add_task(process_doc)
    
    document["id"] = document_id
    document.pop("_id", None)
    return document


@router.get("/")
async def get_documents(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """Get all documents"""
    db = get_database()
    cursor = db.documents.find().skip(skip).limit(limit)
    documents = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string
    for doc in documents:
        doc["id"] = str(doc.pop("_id"))
    
    return documents


@router.get("/{document_id}")
async def get_document(
    document_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific document"""
    db = get_database()
    document = await db.documents.find_one({"_id": ObjectId(document_id)})
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    document["id"] = str(document.pop("_id"))
    return document


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a document"""
    db = get_database()
    document = await db.documents.find_one({"_id": ObjectId(document_id)})
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete embeddings from MongoDB vector store
    rag_service = RAGService()
    await rag_service.delete_document_embeddings(document_id)
    
    # Delete document record
    await db.documents.delete_one({"_id": ObjectId(document_id)})
    
    return {"message": "Document deleted successfully"}
