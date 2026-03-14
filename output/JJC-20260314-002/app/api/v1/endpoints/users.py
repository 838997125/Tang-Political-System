"""User endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService
from app.api.deps import get_current_active_user, get_current_user
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get information about the currently authenticated user."
)
async def get_me(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Get current authenticated user information."""
    return current_user


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update current user",
    description="Update information for the currently authenticated user."
)
async def update_me(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Update current user information."""
    user_service = UserService(db)
    updated_user = await user_service.update_user(current_user, user_data)
    return updated_user


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Get information about a specific user by ID."
)
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get user by ID."""
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user
