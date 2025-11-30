"""
OAuth router for Google authentication.
"""

import logging
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from httpx_oauth.clients.google import GoogleOAuth2
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..database import get_async_session
from ..models.user import User

# Google OAuth client
google_oauth_client = GoogleOAuth2(
    client_id=settings.google_client_id,
    client_secret=settings.google_client_secret,
)

router = APIRouter(prefix="/auth", tags=["OAuth"])

# Docusaurus base URL path
FRONTEND_BASE_PATH = "/physical-ai-humaniod-robotics"

# Backend callback URL (must match Google Console exactly)
BACKEND_CALLBACK_URI = "http://localhost:8000/api/auth/google/callback"

logger = logging.getLogger(__name__)


# Custom authorize endpoint that redirects
@router.get("/google/authorize")
async def google_authorize() -> RedirectResponse:
    """
    Redirect to Google OAuth authorization page.
    """
    logger.info(f"Google authorize called - client_id: {settings.google_client_id[:20]}...")
    authorization_url = await google_oauth_client.get_authorization_url(
        redirect_uri=BACKEND_CALLBACK_URI,
        scope=["openid", "email", "profile"],
    )
    logger.info(f"Redirecting to: {authorization_url[:100]}...")
    return RedirectResponse(url=authorization_url)


# Custom callback endpoint to handle the OAuth response
@router.get("/google/callback")
async def google_callback(
    code: str,
    state: str = None,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Handle Google OAuth callback and exchange code for tokens.
    """
    from ..dependencies.auth import get_jwt_strategy
    from passlib.hash import argon2
    import uuid
    
    logger.info(f"OAuth callback received - code: {code[:20]}..., redirect_uri: {BACKEND_CALLBACK_URI}")
    logger.info(f"Google client_id: {settings.google_client_id}")
    logger.info(f"Google client_secret present: {bool(settings.google_client_secret)}")
    
    try:
        # Exchange code for access token
        token = await google_oauth_client.get_access_token(
            code=code,
            redirect_uri=BACKEND_CALLBACK_URI,
        )
        
        # Get user info from Google
        async with google_oauth_client.get_httpx_client() as client:
            response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {token['access_token']}"},
            )
            user_info = response.json()
        
        email = user_info.get("email")
        google_name = user_info.get("name", "")  # Get name from Google
        logger.info(f"Google OAuth: Got user info for {email}, name: {google_name}")
        
        # Check if user exists
        result = await session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        is_new_user = False
        
        if not user:
            # Create new user with random password (OAuth users don't use password)
            random_password = str(uuid.uuid4())
            hashed_password = argon2.hash(random_password)
            
            user = User(
                email=email,
                hashed_password=hashed_password,
                is_active=True,
                is_verified=True,  # Trust Google's verification
                is_superuser=False,
                name=google_name,  # Save name from Google
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            is_new_user = True
            logger.info(f"Google OAuth: Created new user {email} with name {google_name}")
        else:
            # Update name if not set
            if not user.name and google_name:
                user.name = google_name
                await session.commit()
            logger.info(f"Google OAuth: Found existing user {email}")
        
        # Generate JWT token
        jwt_strategy = get_jwt_strategy()
        token_value = await jwt_strategy.write_token(user)
        
        # Redirect new users to onboarding, existing users to home
        # Pass token and user info as URL params for frontend to pick up
        import urllib.parse
        user_data = urllib.parse.quote(f'{{"id":"{user.id}","email":"{email}","name":"{user.name or google_name}"}}')
        
        if is_new_user:
            redirect_url = f"{settings.frontend_url}{FRONTEND_BASE_PATH}/?auth_token={token_value}&user={user_data}&new_user=1"
        else:
            redirect_url = f"{settings.frontend_url}{FRONTEND_BASE_PATH}/?auth_token={token_value}&user={user_data}"
        
        redirect_response = RedirectResponse(
            url=redirect_url,
            status_code=302,
        )
        
        # Also set auth cookie for backend API calls
        redirect_response.set_cookie(
            key="physicalai_auth",
            value=token_value,
            httponly=True,
            secure=settings.is_production,
            samesite="lax",
            max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        )
        
        logger.info(f"Google OAuth: Successfully authenticated {email}, redirecting to {redirect_url[:80]}...")
        return redirect_response
                    
    except Exception as e:
        logger.error(f"OAuth callback error: {e}", exc_info=True)
        import urllib.parse
        error_msg = urllib.parse.quote(str(e)[:100])  # Truncate error message
        return RedirectResponse(
            url=f"{settings.frontend_url}{FRONTEND_BASE_PATH}/login?error={error_msg}",
            status_code=302,
        )
