"""Authentication endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.user import (
    UserCreateRequest,
    UserResponse,
    UserLoginResponse,
    TokenRefreshRequest,
    TokenRefreshResponse
)
from app.services.user_service import UserService
from app.services.token_service import TokenService
from app.core.security import create_token_pair
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email, username, and password."
)
async def register(
    user_data: UserCreateRequest,
    db: AsyncSession = Depends(get_db)
) -> User:
    """Register a new user."""
    user_service = UserService(db)
    
    try:
        user = await user_service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/login",
    response_model=UserLoginResponse,
    summary="User login",
    description="Authenticate user and return access/refresh tokens."
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Authenticate user and return tokens."""
    user_service = UserService(db)
    token_service = TokenService(db)
    
    # Authenticate user
    user = await user_service.authenticate_user(
        form_data.username,  # OAuth2 form uses username field for email
        form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    await user_service.update_last_login(user)
    
    # Create tokens
    access_token, refresh_token = create_token_pair(user.id, user.email)
    
    # Store refresh token
    await token_service.create_refresh_token(user.id, refresh_token)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 1800,  # 30 minutes in seconds
        "user": user
    }


@router.post(
    "/refresh",
    response_model=TokenRefreshResponse,
    summary="Refresh access token",
    description="Use refresh token to get a new access token."
)
async def refresh_token(
    refresh_data: TokenRefreshRequest,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Refresh access token using refresh token."""
    token_service = TokenService(db)
    user_service = UserService(db)
    
    # Get stored refresh token
    stored_token = await token_service.get_refresh_token(refresh_data.refresh_token)
    
    if not stored_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Check if token is valid
    if not await token_service.is_token_valid(stored_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired or revoked"
        )
    
    # Get user
    user = await user_service.get_user_by_id(stored_token.user_id)
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Rotate tokens
    access_token, refresh_token = await token_service.rotate_refresh_token(
        refresh_data.refresh_token,
        user.id,
        user.email
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 1800  # 30 minutes in seconds
    }


@router.post(
    "/logout",
    summary="User logout",
    description="Revoke current refresh token."
)
async def logout(
    refresh_data: TokenRefreshRequest,
    db: AsyncSession = Depends(get_db)
) -> dict:
    """Logout user by revoking refresh token."""
    token_service = TokenService(db)
    
    # Revoke the refresh token
    revoked = await token_service.revoke_refresh_token(refresh_data.refresh_token)
    
    if not revoked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token not found or already revoked"
        )
    
    return {"message": "Successfully logged out"}
