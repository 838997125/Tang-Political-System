"""Token service for managing refresh tokens."""
from typing import Optional
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.token import RefreshToken
from app.core.config import settings
from app.core.security import create_token_pair, decode_token


class TokenService:
    """Service class for token-related operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_refresh_token(self, user_id: str, token: str) -> RefreshToken:
        """Store a new refresh token in the database."""
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        
        db_token = RefreshToken(
            token=token,
            user_id=user_id,
            expires_at=expires_at,
            is_revoked=False
        )
        
        self.db.add(db_token)
        await self.db.commit()
        await self.db.refresh(db_token)
        return db_token
    
    async def get_refresh_token(self, token: str) -> Optional[RefreshToken]:
        """Get refresh token by token string."""
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.token == token)
        )
        return result.scalar_one_or_none()
    
    async def revoke_refresh_token(self, token: str) -> bool:
        """Revoke a refresh token."""
        result = await self.db.execute(
            update(RefreshToken)
            .where(RefreshToken.token == token)
            .values(
                is_revoked=True,
                revoked_at=datetime.now(timezone.utc)
            )
        )
        await self.db.commit()
        return result.rowcount > 0
    
    async def revoke_all_user_tokens(self, user_id: str) -> int:
        """Revoke all refresh tokens for a user."""
        result = await self.db.execute(
            update(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.is_revoked == False
            )
            .values(
                is_revoked=True,
                revoked_at=datetime.now(timezone.utc)
            )
        )
        await self.db.commit()
        return result.rowcount
    
    async def is_token_valid(self, token: RefreshToken) -> bool:
        """Check if a refresh token is valid (not revoked and not expired)."""
        if token.is_revoked:
            return False
        if token.is_expired:
            return False
        return True
    
    async def cleanup_expired_tokens(self) -> int:
        """Delete expired tokens from database."""
        result = await self.db.execute(
            RefreshToken.__table__.delete().where(
                RefreshToken.expires_at < datetime.now(timezone.utc)
            )
        )
        await self.db.commit()
        return result.rowcount
    
    async def rotate_refresh_token(
        self, old_token: str, user_id: str, email: str
    ) -> tuple[str, str]:
        """Rotate refresh token - revoke old and create new."""
        # Revoke old token
        await self.revoke_refresh_token(old_token)
        
        # Create new token pair
        access_token, refresh_token = create_token_pair(user_id, email)
        
        # Store new refresh token
        await self.create_refresh_token(user_id, refresh_token)
        
        return access_token, refresh_token
