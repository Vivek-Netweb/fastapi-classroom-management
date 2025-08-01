from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
from fastapi import Request
import os
from app.utils.api_response import error_response

SECURITY_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

EXCLUDE_PATHS = [
    "/auth/login",
    "/auth/register",
    "/openapi.json",
    "/docs",
    "/docs/oauth2-redirect",
    "/redoc",
    "/"
]


EXCLUDE_PREFIXES = ["/uploads"]


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if request.url.path in EXCLUDE_PATHS or request.url.path.startswith("/static"):
            return await call_next(request)

        # Prefix match for directories
        if any(request.url.path.startswith(prefix) for prefix in EXCLUDE_PREFIXES):
            return await call_next(request)

        token = None
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "").strip()
        else:
            token = request.cookies.get("access_token")

        if not token:
            return error_response(
                message="Missing Access Token",
                status_code=401,
                delete_cookies=["access_token"],
            )

        try:
            payload = jwt.decode(token, SECURITY_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            role = payload.get("role")

            if user_id is None or role is None:
                raise JWTError()

            request.state.user = {"id": int(user_id), "role": role}

        except JWTError:
            # Delete the cookie if invalid or expired
            return error_response(
                message="Missing Access Token",
                status_code=401,
                delete_cookies=["access_token"],
            )

        response = await call_next(request)
        return response
