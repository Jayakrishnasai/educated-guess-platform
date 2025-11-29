from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserSchema(BaseModel):
    """User response schema"""
    id: str = Field(alias="_id")
    email: EmailStr
    full_name: str
    is_active: bool
    created_at: datetime
    
    class Config:
        populate_by_name = True


class UserCreateSchema(BaseModel):
    """User creation schema"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: str = Field(..., min_length=1, max_length=100)


class UserLoginSchema(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str
