from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from app.schemas.content_schema import (
    ContentSchema,
    ContentCreateSchema,
    ContentUpdateSchema,
    CategorySchema,
    CategoryCreateSchema,
    AuthorSchema,
    AuthorCreateSchema
)
from app.services.content_service import ContentService
from app.services.category_service import CategoryService

router = APIRouter()


# Content routes
@router.get("/content", response_model=List[ContentSchema], tags=["Content"])
async def get_content_items(
    category: Optional[str] = Query(None, description="Filter by category ID"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    limit: int = Query(50, ge=1, le=100)
):
    """Get all content items with optional filtering"""
    items = await ContentService.get_all_content(category, search, limit)
    return items


@router.get("/content/{item_id}", response_model=Content Schema, tags=["Content"])
async def get_content_item(item_id: str):
    """Get a single content item by ID"""
    item = await ContentService.get_content_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Content item not found")
    return item


@router.post("/content", response_model=ContentSchema, status_code=status.HTTP_201_CREATED, tags=["Content"])
async def create_content_item(content: ContentCreateSchema):
    """Create a new content item"""
    item = await ContentService.create_content(content)
    return item


@router.put("/content/{item_id}", response_model=ContentSchema, tags=["Content"])
async def update_content_item(item_id: str, content: ContentUpdateSchema):
    """Update a content item"""
    item = await ContentService.update_content(item_id, content)
    if not item:
        raise HTTPException(status_code=404, detail="Content item not found or no fields to update")
    return item


@router.delete("/content/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Content"])
async def delete_content_item(item_id: str):
    """Delete a content item"""
    deleted = await ContentService.delete_content(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Content item not found")
    return None


# Category routes
@router.get("/categories", response_model=List[CategorySchema], tags=["Categories"])
async def get_categories():
    """Get all categories"""
    categories = await CategoryService.get_all_categories()
    return categories


@router.get("/categories/{category_id}", response_model=CategorySchema, tags=["Categories"])
async def get_category(category_id: str):
    """Get a single category by ID"""
    category = await CategoryService.get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/categories", response_model=CategorySchema, status_code=status.HTTP_201_CREATED, tags=["Categories"])
async def create_category(category: CategoryCreateSchema):
    """Create a new category"""
    created_category = await CategoryService.create_category(category)
    if not created_category:
        raise HTTPException(status_code=400, detail="Category slug already exists")
    return created_category
