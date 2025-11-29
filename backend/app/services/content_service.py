from typing import List, Optional
from bson import ObjectId
from app.core.database import get_database
from app.schemas.content_schema import ContentCreateSchema, ContentUpdateSchema
from datetime import datetime


class ContentService:
    """Service layer for content operations"""
    
    @staticmethod
    async def get_all_content(
        category: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 50
    ) -> List[dict]:
        """Get all content items with optional filtering"""
        db = get_database()
        
        # Build query
        query = {}
        if category:
            query["category_id"] = category
        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}},
                {"tags": {"$regex": search, "$options": "i"}}
            ]
        
        # Fetch content items
        cursor = db.content_items.find(query).sort("created_at", -1).limit(limit)
        items = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string
        for item in items:
            item["_id"] = str(item["_id"])
        
        return items
    
    @staticmethod
    async def get_content_by_id(item_id: str) -> Optional[dict]:
        """Get a single content item by ID"""
        if not ObjectId.is_valid(item_id):
            return None
        
        db = get_database()
        item = await db.content_items.find_one({"_id": ObjectId(item_id)})
        
        if item:
            item["_id"] = str(item["_id"])
        
        return item
    
    @staticmethod
    async def create_content(content: ContentCreateSchema) -> dict:
        """Create a new content item"""
        db = get_database()
        
        content_dict = content.model_dump()
        content_dict["created_at"] = datetime.utcnow()
        
        result = await db.content_items.insert_one(content_dict)
        created_item = await db.content_items.find_one({"_id": result.inserted_id})
        created_item["_id"] = str(created_item["_id"])
        
        return created_item
    
    @staticmethod
    async def update_content(item_id: str, content: ContentUpdateSchema) -> Optional[dict]:
        """Update a content item"""
        if not ObjectId.is_valid(item_id):
            return None
        
        db = get_database()
        
        # Only update provided fields
        update_data = {k: v for k, v in content.model_dump().items() if v is not None}
        
        if not update_data:
            return None
        
        result = await db.content_items.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            return None
        
        updated_item = await db.content_items.find_one({"_id": ObjectId(item_id)})
        updated_item["_id"] = str(updated_item["_id"])
        
        return updated_item
    
    @staticmethod
    async def delete_content(item_id: str) -> bool:
        """Delete a content item"""
        if not ObjectId.is_valid(item_id):
            return False
        
        db = get_database()
        result = await db.content_items.delete_one({"_id": ObjectId(item_id)})
        
        return result.deleted_count > 0
