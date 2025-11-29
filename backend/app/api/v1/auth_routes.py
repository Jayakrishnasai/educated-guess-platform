from fastapi import APIRouter, HTTPException, status
from app.schemas.user_schema import UserCreateSchema, UserLoginSchema, UserSchema
from app.schemas.auth_schema import TokenSchema
from app.services.user_service import UserService
from app.core.security import create_access_token
from datetime import timedelta
from app.core.config import settings

router = APIRouter()


@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED, tags=["Authentication"])
async def register(user: UserCreateSchema):
    """Register a new user"""
    created_user = await UserService.create_user(user)
    
    if not created_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    return created_user


@router.post("/login", response_model=TokenSchema, tags=["Authentication"])
async def login(credentials: UserLoginSchema):
    """Login and receive JWT token"""
    user = await UserService.authenticate_user(credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user["email"], "user_id": user["_id"]},
        expires_delta=access_token_expires
    )
    
    return TokenSchema(
        access_token=access_token,
        token_type="bearer",
        user={
            "email": user["email"],
            "full_name": user["full_name"]
        }
    )
