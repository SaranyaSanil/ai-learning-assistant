from http import HTTPStatus
from typing import List, Tuple
from unicodedata import name
from unittest import result

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

from fastapi import APIRouter, Form, File, UploadFile
from fastapi.params import Depends

from app.core.logger import setup_logger
from app.middleware.auth import get_current_user_payload
from app.schemas.user_schema import AssignRoleRequest, AssignRoleResponse, ChangePasswordRequest, UpdateUserRequest, UserCreate, UserLogin, UserResponse
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
    profile_pic: UploadFile = File(None)):
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

@router.put("/{user_id}/role", response_model=AssignRoleResponse, status_code=HTTPStatus.OK)
def assign_role(user_id: int,
    payload: AssignRoleRequest,current_user: dict = Depends(get_current_user_payload)):
    logger.info(f"Processing assign role request for user_id: {user_id} with role_id: {payload.role_id}")
    result = user_service.assign_role_to_user(user_id,payload.role_id,current_user)
    logger.info(f"Role assigned successfully to user_id: {user_id} with role_id: {payload.role_id}")
    return result

@router.delete("/delete/{user_id}",status_code=HTTPStatus.OK)
def delete_user(user_id: int,
    payload:dict=Depends(get_current_user_payload)):
    logger.info("Processing delete user request")
    result = user_service.delete_user(user_id, payload)
    logger.info(f"User deleted successfully: {result['message']}")
    return result

@router.get("/all", response_model=List[UserResponse], status_code=HTTPStatus.OK)
def get_all_users(payload:dict=Depends(get_current_user_payload)):
    logger.info("Processing get all users request")
    result = user_service.get_all_users(payload)
    logger.info(f"Total users retrieved successfully: {len(result)}")
    return result

@router.get("/{user_id}", response_model=UserResponse, status_code=HTTPStatus.OK)
def get_user_by_id(user_id: int,payload:dict=Depends(get_current_user_payload)):
    logger.info(f"Processing get user by id request for user_id: {user_id}")
    result = user_service.get_user_by_id(user_id,payload)
    logger.info(f"User retrieved successfully: {result.id}")
    return result

@router.patch("/change-password",status_code=HTTPStatus.OK)
def change_password(
    payload: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user_payload)):
    logger.info("Processing change password request")
    result = user_service.change_password(payload,current_user)
    logger.info("Password changed successfully")
    return result

@router.patch("/{user_id}",response_model=UserResponse,status_code=HTTPStatus.OK)
def update_user(user_id: int,
    payload: UpdateUserRequest,
    current_user: dict = Depends(get_current_user_payload)):
    logger.info(f"Processing update user request: {user_id}")
    result = user_service.update_user(user_id,payload,current_user )
    logger.info(f"User updated successfully: {result.id}")
    return result

@router.get("/{user_id}/permissions", status_code=HTTPStatus.OK)
def get_user_permissions(user_id: int, payload: dict = Depends(get_current_user_payload)):
    logger.info(f"Fetching permissions for user {user_id}")
    result = user_service.get_user_permissions(user_id,payload)
    logger.info(f"Permissions fetched successfully for user {user_id}")
    return result

@router.post("/logout", status_code=HTTPStatus.OK)
def logout_user(token: str = Depends(oauth2_scheme),current_user: dict = Depends(get_current_user_payload)):
    logger.info(f"Processing logout request for user_id: {current_user['user_id']}")
    result = user_service.logout_user(token)
    logger.info(f"User logged out successfully: {current_user['user_id']}")
    return result
