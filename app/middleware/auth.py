from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.middleware.jwt import verify_access_token
from app.exceptions.custom_exception import UnauthorizedError


security = HTTPBearer()


def get_current_user_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    payload = verify_access_token(token)

    if not payload:
        raise UnauthorizedError("Invalid or expired token")

    return payload