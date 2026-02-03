"""
User Service for MongoDB
Simplified service layer for user operations
"""
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.db.session import get_database


class UserService:
    def __init__(self):
        self.collection_name = "users"
    
    async def get(self, id: str) -> Optional[dict]:
        """Get user by ID"""
        db = get_database()
        return await db[self.collection_name].find_one({"_id": ObjectId(id)})
    
    async def get_by_email(self, email: str) -> Optional[dict]:
        """Get user by email"""
        db = get_database()
        return await db[self.collection_name].find_one({"email": email})
    
    async def get_by_username(self, username: str) -> Optional[dict]:
        """Get user by username"""
        db = get_database()
        return await db[self.collection_name].find_one({"username": username})
    
    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get multiple users with pagination"""
        db = get_database()
        cursor = db[self.collection_name].find().skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
    
    async def create(self, obj_in: UserCreate) -> dict:
        """Create new user"""
        db = get_database()
        user_dict = {
            "email": obj_in.email,
            "username": obj_in.username,
            "hashed_password": get_password_hash(obj_in.password),
            "is_active": obj_in.is_active,
            "is_superuser": obj_in.is_superuser,
            "created_at": datetime.utcnow(),
            "updated_at": None
        }
        result = await db[self.collection_name].insert_one(user_dict)
        user_dict["_id"] = result.inserted_id
        return user_dict
    
    async def update(self, id: str, obj_in: UserUpdate) -> Optional[dict]:
        """Update user"""
        db = get_database()
        update_data = obj_in.model_dump(exclude_unset=True)
        
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        
        update_data["updated_at"] = datetime.utcnow()
        
        result = await db[self.collection_name].find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_data},
            return_document=True
        )
        return result
    
    async def remove(self, id: str) -> bool:
        """Delete user"""
        db = get_database()
        result = await db[self.collection_name].delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
    
    async def authenticate(self, email: str, password: str) -> Optional[dict]:
        """Authenticate user"""
        user = await self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user["hashed_password"]):
            return None
        return user


user_service = UserService()
