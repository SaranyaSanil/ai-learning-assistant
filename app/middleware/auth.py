from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.middleware.jwt import verify_access_token
from app.exceptions.custom_exception import UnauthorizedError
from app.repository.user_repository import UserRepository


security = HTTPBearer()
user_repository = UserRepository()

def get_current_user_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    payload = verify_access_token(token)

    if not payload:
        raise UnauthorizedError("Invalid or expired token")
    
    if user_repository.is_blacklisted(token):
        raise UnauthorizedError("User has been logged out")


    return payload