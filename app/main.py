from fastapi import FastAPI

from app.core.database import Base, engine
from app.models.user import User
from app.controller.user_controller import router as user_router
Base.metadata.create_all(bind=engine)

from app.middleware.exception_handler import (
    bad_request_exception_handler,
    service_exception_handler,
    unauthorized_exception_handler
)

from app.exceptions.custom_exception import (
    BadRequest,
    ServiceError,
    UnauthorizedError
)

app = FastAPI()

app.include_router(user_router)

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

@app.get("/")
def home():
    return {"message": "AI Learning Assistant"}