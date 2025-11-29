from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# MongoDB client instance
client = None
database = None


async def connect_to_mongo():
    """Connect to MongoDB on application startup"""
    global client, database
    client = AsyncIOMotorClient(settings.mongodb_url)
    database = client[settings.mongodb_db_name]
    
    # Test connection
    try:
        await client.admin.command('ping')
        print(f"✓ Connected to MongoDB: {settings.mongodb_db_name}")
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection on application shutdown"""
    global client
    if client:
        client.close()
        print("✓ Closed MongoDB connection")


def get_database():
    """Get database instance"""
    return database
