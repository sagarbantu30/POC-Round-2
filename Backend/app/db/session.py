"""
MongoDB Database Connection
Simple async MongoDB connection using Motor driver
"""
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

db = Database()

async def connect_to_mongo():
    """Connect to MongoDB on startup"""
    db.client = AsyncIOMotorClient(settings.MONGODB_URI)
    db.db = db.client[settings.MONGODB_DB_NAME]
    print(f"Connected to MongoDB: {settings.MONGODB_DB_NAME}")

async def close_mongo_connection():
    """Close MongoDB connection on shutdown"""
    db.client.close()
    print("Closed MongoDB connection")

def get_database():
    """Get MongoDB database instance"""
    return db.db
