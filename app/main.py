from fastapi import FastAPI

from app.core.database import Base, engine
from app.models.user import User,Role
from app.controller.user_controller import router as user_router
from app.controller.role_controller import router as role_router
Base.metadata.create_all(bind=engine)

from app.middleware.exception_handler import (
    bad_request_exception_handler,
    service_exception_handler,
    unauthorized_exception_handler,
    resource_not_found_exception_handler,
    expired_signature_exception_handler,
    invalid_token_exception_handler
)

from app.exceptions.custom_exception import (
    BadRequest,
    InvalidTokenError,
ExpiredSignatureError,
    ResourceNotFoundError,
    ServiceError,
    UnauthorizedError,
    DuplicateResourceError
)

app = FastAPI()

app.include_router(user_router)
app.include_router(role_router)

app.add_exception_handler(
    BadRequest,
    bad_request_exception_handler
)

app.add_exception_handler(
    ServiceError,
    service_exception_handler
)
app.add_exception_handler(
    UnauthorizedError,  
    unauthorized_exception_handler
)

app.add_exception_handler(
    ResourceNotFoundError,
    resource_not_found_exception_handler
)

app.add_exception_handler(
    DuplicateResourceError,
    bad_request_exception_handler
)

app.add_exception_handler(
    ExpiredSignatureError,
    expired_signature_exception_handler
)
app.add_exception_handler(
    InvalidTokenError,
    invalid_token_exception_handler
)

@app.get("/")
def home():
    return {"message": "AI Learning Assistant"}