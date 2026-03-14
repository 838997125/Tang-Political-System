"""User Pydantic schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# Base schema
class UserBase(BaseModel):
    """Base user schema with common attributes."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, max_length=200)


# Create schemas
class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, max_length=100)


class UserCreateRequest(BaseModel):
    """Request schema for user registration."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    full_name: Optional[str] = Field(None, max_length=200)


# Update schemas
class UserUpdate(BaseModel):
    """Schema for updating user information."""
    full_name: Optional[str] = Field(None, max_length=200)
    is_active: Optional[bool] = None


# Response schemas
class UserResponse(UserBase):
    """Schema for user response."""
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None


class UserInDB(UserResponse):
    """Schema for user in database (includes hashed password)."""
    hashed_password: str


# Login schemas
class UserLoginRequest(BaseModel):
    """Request schema for user login."""
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    """Response schema for user login."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


# Token schemas
class TokenRefreshRequest(BaseModel):
    """Request schema for token refresh."""
    refresh_token: str


class TokenRefreshResponse(BaseModel):
    """Response schema for token refresh."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenPayload(BaseModel):
    """Schema for JWT token payload."""
    sub: str
    email: str
    exp: datetime
    type: str
