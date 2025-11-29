from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ContentSchema(BaseModel):
    """Content item response schema"""
    id: str = Field(alias="_id")
    title: str
    description: str
    category_id: Optional[str] = None
    author_id: Optional[str] = None
    image_url: Optional[str] = None
    tags: List[str] = []
    created_at: datetime
    
    class Config:
        populate_by_name = True


class ContentCreateSchema(BaseModel):
    """Content item creation schema"""
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    category_id: Optional[str] = None
    author_id: Optional[str] = None
    image_url: Optional[str] = None
    tags: List[str] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Leaning Into the Mundane",
                "description": "Exploring the beauty in everyday moments",
                "category_id": "507f1f77bcf86cd799439011",
                "author_id": "507f1f77bcf86cd799439012",
                "image_url": "https://example.com/image.jpg",
                "tags": ["philosophy", "mindfulness"]
            }
        }


class ContentUpdateSchema(BaseModel):
    """Content item update schema"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    category_id: Optional[str] = None
    author_id: Optional[str] = None
    image_url: Optional[str] = None
    tags: Optional[List[str]] = None


class CategorySchema(BaseModel):
    """Category response schema"""
    id: str = Field(alias="_id")
    name: str
    slug: str
    description: Optional[str] = None
    
    class Config:
        populate_by_name = True


class CategoryCreateSchema(BaseModel):
    """Category creation schema"""
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class AuthorSchema(BaseModel):
    """Author response schema"""
    id: str = Field(alias="_id")
    name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    
    class Config:
        populate_by_name = True


class AuthorCreateSchema(BaseModel):
    """Author creation schema"""
    name: str = Field(..., min_length=1, max_length=100)
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
