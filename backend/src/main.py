"""
Main FastAPI application entry point.
Physical AI Learning Platform - Authentication System
"""

import logging
import os
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware

from .config import settings
from .routers import profile, chat  # Removed: auth, oauth (migrated to Better Auth)
from .utils.rate_limit import limiter

# Set OpenAI API key for the agents SDK (it looks for this env var)
os.environ["OPENAI_API_KEY"] = settings.openai_api_key

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.is_development else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to all responses."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # HSTS (only in production with HTTPS)
        if settings.is_production:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        return response


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info(f"Starting Physical AI Auth API in {settings.environment} mode")
    logger.info(f"Database: {settings.database_url.split('@')[-1]}")  # Hide credentials
    yield
    # Shutdown
    logger.info("Shutting down Physical AI Auth API")


# Create FastAPI application
app = FastAPI(
    title="Physical AI Learning Platform - Auth API",
    description="Authentication, onboarding, and email verification system",
    version="0.1.0",
    docs_url="/docs" if settings.is_development else None,
    redoc_url="/redoc" if settings.is_development else None,
    lifespan=lifespan,
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler for unhandled errors.

    Args:
        request: The request that caused the exception
        exc: The exception that was raised

    Returns:
        JSONResponse with error details
    """
    logger.error(
        f"Unhandled exception: {exc}",
        exc_info=True,
        extra={
            "path": request.url.path,
            "method": request.method,
            "client": request.client.host if request.client else "unknown",
        },
    )

    if settings.is_development:
        # Return detailed error in development
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": str(exc),
                "type": type(exc).__name__,
            },
        )
    else:
        # Return generic error in production
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "An internal server error occurred. Please try again later."
            },
        )


# Include routers
# Removed: auth.router, oauth.router (migrated to Better Auth TypeScript service)
app.include_router(profile.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        dict: Service status and version information.
    """
    return {
        "status": "healthy",
        "service": "physical-ai-auth",
        "version": "0.1.0",
        "environment": settings.environment,
    }


@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    """
    Root endpoint with API information.

    Returns:
        dict: Welcome message and documentation links.
    """
    return {
        "message": "Physical AI Learning Platform - Auth API",
        "docs": "/docs" if settings.is_development else "Documentation disabled in production",
        "health": "/health",
    }
