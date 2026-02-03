"""
User Management Endpoints
CRUD operations for users using MongoDB
"""
from typing import List
from fastapi import APIRouter, HTTPException, status
from app.schemas import user as user_schema
from app.services import user_service

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user_in: user_schema.UserCreate):
    """Create new user"""
    user = await user_service.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    user = await user_service.get_by_username(username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    new_user = await user_service.create(obj_in=user_in)
    # Convert ObjectId to string for JSON response
    new_user["id"] = str(new_user.pop("_id"))
    return new_user


@router.get("/")
async def read_users(skip: int = 0, limit: int = 100):
    """Get all users with pagination"""
    users = await user_service.get_multi(skip=skip, limit=limit)
    # Convert ObjectIds to strings
    for user in users:
        user["id"] = str(user.pop("_id"))
    return users


@router.get("/{user_id}")
async def read_user(user_id: str):
    """Get user by ID"""
    user = await user_service.get(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user["id"] = str(user.pop("_id"))
    return user


@router.put("/{user_id}")
async def update_user(user_id: str, user_in: user_schema.UserUpdate):
    """Update user"""
    user = await user_service.get(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    updated_user = await user_service.update(id=user_id, obj_in=user_in)
    if updated_user:
        updated_user["id"] = str(updated_user.pop("_id"))
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """Delete user"""
    user = await user_service.get(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    await user_service.remove(id=user_id)
    return None
