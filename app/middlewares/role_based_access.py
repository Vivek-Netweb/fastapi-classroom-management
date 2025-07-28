from fastapi import Depends , HTTPException ,status, Request
from typing import List
from app.utils.api_response import error_response
def required_roles(allowed_roles : List[str]):
    async def role_checker(request:Request):
        user = request.state.user
        if not user or user.get("role") not in allowed_roles:
            raise HTTPException (
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this resource",
            )
    return role_checker