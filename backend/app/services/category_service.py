from typing import List, Optional
from bson import ObjectId
from app.core.database import get_database
from app.schemas.content_schema import CategoryCreateSchema


class CategoryService:
    """Service layer for category operations"""
    
    @staticmethod
    async def get_all_categories() -> List[dict]:
        """Get all categories"""
        db = get_database()
        cursor = db.categories.find()
        categories = await cursor.to_list(length=100)
        
        for cat in categories:
            cat["_id"] = str(cat["_id"])
        
        return categories
    
    @staticmethod
    async def get_category_by_id(category_id: str) -> Optional[dict]:
        """Get a single category by ID"""
        if not ObjectId.is_valid(category_id):
            return None
        
        db = get_database()
        category = await db.categories.find_one({"_id": ObjectId(category_id)})
        
        if category:
            category["_id"] = str(category["_id"])
        
        return category
    
    @staticmethod
    async def get_category_by_slug(slug: str) -> Optional[dict]:
        """Get a category by slug"""
        db = get_database()
        category = await db.categories.find_one({"slug": slug})
        
        if category:
            category["_id"] = str(category["_id"])
        
        return category
    
    @staticmethod
    async def create_category(category: CategoryCreateSchema) -> Optional[dict]:
        """Create a new category"""
        db = get_database()
        
        # Check if slug already exists
        existing = await db.categories.find_one({"slug": category.slug})
        if existing:
            return None
        
        category_dict = category.model_dump()
        result = await db.categories.insert_one(category_dict)
        created_category = await db.categories.find_one({"_id": result.inserted_id})
        created_category["_id"] = str(created_category["_id"])
        
        return created_category
