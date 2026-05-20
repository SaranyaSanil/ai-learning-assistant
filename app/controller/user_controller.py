from http import HTTPStatus
from typing import Tuple
from unicodedata import name
from unittest import result

from fastapi import APIRouter, Form, File, UploadFile
from fastapi.params import Depends

from app.core.logger import setup_logger
from app.middleware.auth import get_current_user_payload
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.services.user_service import UserService
from app.utils.response_builder import ResponseBuilder

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

logger = setup_logger(__name__)

user_service = UserService()
@router.post("", response_model=UserResponse, status_code=HTTPStatus.CREATED)
def create_user(
    payload: UserCreate = Depends(UserCreate.as_form),
    profile_pic: UploadFile = File(None)
):
    logger.info("Processing create user request")
    result = user_service.create_user(payload, profile_pic)
    logger.info(f"User created successfully: {result.id}")
    return result
       
@router.post("/login", status_code=HTTPStatus.OK)
def login_user(payload: UserLogin):
    """Login user and return JWT token."""
    logger.info("Processing login request")
    result = user_service.login_user(payload)
    logger.info(f"User logged in successfully: {payload.username}")
    return ResponseBuilder.success(
        data=result,
        message="Login successful"     
    )

@router.get("/current_user",response_model=UserResponse,status_code=HTTPStatus.OK)
def get_current_user(
    payload:dict=Depends(get_current_user_payload)):
    logger.info("Processing get current user request")
    result = user_service.get_current_user(payload)
    logger.info(f"Current user retrieved successfully: {result.id}")
    return result