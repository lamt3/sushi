from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from typing import Optional
import logging

from tuna.config import Config

logger = logging.getLogger(__name__)

# These should match your token creation settings
SECRET_KEY = Config.JWT_SECRET_KEY
ALGORITHM = Config.JWT_ALGORITHM
from starlette.middleware.base import BaseHTTPMiddleware

async def auth_middleware(request: Request, call_next):
    # List of paths that don't need authentication
    public_paths = ["/api/v1/login", "/api/v1/health", "/api/v1/pixel", "/api/v1/shopify/oauth", "/api/v1/shopify/oauth/callback"]
    
    if request.url.path in public_paths:
        return await call_next(request)

    try:
        token = request.cookies.get("token")
        print(token)
        if not token:
            logger.error(f"Auth Middleware - No Cookie")
            raise HTTPException(status_code=401, detail="Authentication Failed. Please Re-Login")

        try:
            # Verify the JWT token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.member = payload
        except JWTError as e:
            logger.error(f"Auth Middleware - Invalid Token: {e}")
            return JSONResponse(
                status_code=401,
                content={"detail": "Authetication Failed. Please Re-Login"}
            )

        # Continue processing the request
        return await call_next(request)

    except Exception as e:
        logger.error(f"Auth middleware error: {e}")
        return JSONResponse(
            status_code=401,
            content={"detail": "Authentication Failed. Please Re-Login."}
        )