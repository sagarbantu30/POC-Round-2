"""
Settings Management Endpoints
Manage RAG settings in MongoDB
"""
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from app.db.session import get_database
from app.api.api_v1.endpoints.auth import get_current_user
from app.core.config import settings as app_settings
from app.schemas.settings import RAGSettingsUpdate, RAGSettingsResponse

router = APIRouter()


@router.get("/")
async def get_settings(current_user: dict = Depends(get_current_user)):
    """Get current RAG settings from database"""
    db = get_database()
    rag_settings = await db.rag_settings.find_one()
    
    if not rag_settings:
        # Create default settings from .env
        rag_settings = {
            "chunk_size": app_settings.CHUNK_SIZE,
            "chunk_overlap": app_settings.CHUNK_OVERLAP,
            "temperature": app_settings.TEMPERATURE,
            "top_p": app_settings.TOP_P,
            "top_k": app_settings.TOP_K,
            "model_name": app_settings.MODEL_NAME,
            "created_at": datetime.utcnow()
        }
        result = await db.rag_settings.insert_one(rag_settings)
        rag_settings["_id"] = result.inserted_id
    
    # Convert ObjectId to string for response
    return {
        "id": str(rag_settings["_id"]),
        "chunk_size": rag_settings.get("chunk_size", app_settings.CHUNK_SIZE),
        "chunk_overlap": rag_settings.get("chunk_overlap", app_settings.CHUNK_OVERLAP),
        "temperature": rag_settings.get("temperature", app_settings.TEMPERATURE),
        "top_p": rag_settings.get("top_p", app_settings.TOP_P),
        "top_k": rag_settings.get("top_k", app_settings.TOP_K),
        "model_name": rag_settings.get("model_name", app_settings.MODEL_NAME)
    }


@router.put("/")
async def update_settings(
    settings_update: RAGSettingsUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update RAG settings in database"""
    if not current_user.get("is_superuser", False):
        raise HTTPException(status_code=403, detail="Only superusers can update settings")
    
    db = get_database()
    rag_settings = await db.rag_settings.find_one()
    
    if not rag_settings:
        # Create default settings first
        rag_settings = {
            "chunk_size": app_settings.CHUNK_SIZE,
            "chunk_overlap": app_settings.CHUNK_OVERLAP,
            "temperature": app_settings.TEMPERATURE,
            "top_p": app_settings.TOP_P,
            "top_k": app_settings.TOP_K,
            "model_name": app_settings.MODEL_NAME,
            "created_at": datetime.utcnow()
        }
        result = await db.rag_settings.insert_one(rag_settings)
        rag_settings["_id"] = result.inserted_id
    
    # Prepare update data (only include non-None values)
    update_data = {}
    if settings_update.chunk_size is not None:
        update_data["chunk_size"] = settings_update.chunk_size
    if settings_update.chunk_overlap is not None:
        update_data["chunk_overlap"] = settings_update.chunk_overlap
    if settings_update.temperature is not None:
        update_data["temperature"] = settings_update.temperature
    if settings_update.top_p is not None:
        update_data["top_p"] = settings_update.top_p
    if settings_update.top_k is not None:
        update_data["top_k"] = settings_update.top_k
    if settings_update.model_name is not None:
        update_data["model_name"] = settings_update.model_name
    
    update_data["updated_at"] = datetime.utcnow()
    
    await db.rag_settings.update_one(
        {"_id": rag_settings["_id"]},
        {"$set": update_data}
    )
    
    # Get and return updated settings
    updated = await db.rag_settings.find_one({"_id": rag_settings["_id"]})
    return {
        "id": str(updated["_id"]),
        "chunk_size": updated.get("chunk_size", app_settings.CHUNK_SIZE),
        "chunk_overlap": updated.get("chunk_overlap", app_settings.CHUNK_OVERLAP),
        "temperature": updated.get("temperature", app_settings.TEMPERATURE),
        "top_p": updated.get("top_p", app_settings.TOP_P),
        "top_k": updated.get("top_k", app_settings.TOP_K),
        "model_name": updated.get("model_name", app_settings.MODEL_NAME)
    }
