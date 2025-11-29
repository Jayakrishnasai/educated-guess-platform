from pydantic import BaseModel


class TokenSchema(BaseModel):
    """JWT token response schema"""
    access_token: str
    token_type: str = "bearer"
    user: dict
