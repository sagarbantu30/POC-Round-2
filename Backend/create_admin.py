"""
Create Admin User Script
Simple script to create an admin user in MongoDB
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.security import get_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


async def create_admin():
    # Get MongoDB URI from environment
    mongodb_uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGODB_DB_NAME", "rag_database")
    
    if not mongodb_uri:
        print("Error: MONGODB_URI not found in .env file")
        print("Please copy .env.example to .env and configure your MongoDB URI")
        return
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(mongodb_uri)
    db = client[db_name]
    
    try:
        # Check if admin already exists
        existing = await db.users.find_one({"email": "admin@example.com"})
        if existing:
            print("Admin user already exists!")
            return
        
        # Create admin user
        admin_user = {
            "email": "admin@example.com",
            "username": "admin",
            "hashed_password": get_password_hash("admin123"),
            "is_active": True,
            "is_superuser": True,
            "created_at": datetime.utcnow(),
            "updated_at": None
        }
        
        result = await db.users.insert_one(admin_user)
        print(f"✅ Admin user created successfully!")
        print(f"📧 Email: admin@example.com")
        print(f"🔑 Password: admin123")
        print(f"🆔 User ID: {result.inserted_id}")
        print(f"\n⚠️  Please change the password after first login!")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(create_admin())
