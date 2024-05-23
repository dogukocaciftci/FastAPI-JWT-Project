from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from app.config import SECRET_KEY, ALGORITHM


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")

            # Authorization check based on HTTP methods
            if not self.check_permission(request.method, credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="You do not have permission to perform this action.")

            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.")

    # Function to verify JWT
    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = jwt.decode(jwtoken, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            isTokenValid = False
        if payload:
            isTokenValid = True
        return isTokenValid

    # Function to check permission based on HTTP method and user role
    def check_permission(self, method: str, jwtoken: str) -> bool:
        try:
            payload = jwt.decode(jwtoken, SECRET_KEY, algorithms=[ALGORITHM])
            user_role = payload.get("role")
            method_roles = {
                "GET": ["user", "admin"],
                "POST": ["admin"],
                "PUT": ["admin"],
                "DELETE": ["admin"]
            }
            if method in method_roles and user_role not in method_roles[method]:
                return False
            return True
        except JWTError:
            return False
