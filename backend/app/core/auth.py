from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Literal
from .exceptions import UnauthorizedError

security = HTTPBearer()

class RoleChecker:
    def __init__(self, allowed_roles: list[Literal["superuser", "org_admin"]]):
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)) -> None:
        # In a real application, validate JWT token and extract role
        # For this demo, we'll use a simple token format: "role_token"
        token = credentials.credentials
        role = token.split("_")[0] if "_" in token else None
        
        if not role or role not in self.allowed_roles:
            raise UnauthorizedError()

# Role checker dependencies
check_superuser = RoleChecker(["superuser"])
check_org_admin = RoleChecker(["org_admin"])
check_any_role = RoleChecker(["superuser", "org_admin"]) 