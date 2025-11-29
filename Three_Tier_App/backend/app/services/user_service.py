from typing import Optional
from app.core.database import get_database
from app.core.security import get_password_hash, verify_password
from app.schemas.user_schema import UserCreateSchema
from datetime import datetime


class UserService:
    """Service layer for user operations"""
    
    @staticmethod
    async def create_user(user: UserCreateSchema) -> Optional[dict]:
        """Create a new user"""
        db = get_database()
        
        # Check if user already exists
        existing_user = await db.users.find_one({"email": user.email})
        if existing_user:
            return None
        
        # Create new user
        hashed_password = get_password_hash(user.password)
        user_dict = {
            "email": user.email,
            "hashed_password": hashed_password,
            "full_name": user.full_name,
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        
        result = await db.users.insert_one(user_dict)
        created_user = await db.users.find_one({"_id": result.inserted_id})
        created_user["_id"] = str(created_user["_id"])
        
        return created_user
    
    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[dict]:
        """Authenticate a user"""
        db = get_database()
        
        user = await db.users.find_one({"email": email})
        if not user:
            return None
        
        if not verify_password(password, user["hashed_password"]):
            return None
        
        user["_id"] = str(user["_id"])
        return user
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[dict]:
        """Get a user by email"""
        db = get_database()
        
        user = await db.users.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])
        
        return user
