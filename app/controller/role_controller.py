from http import HTTPStatus
from fastapi import APIRouter, Depends

from app.middleware.auth import get_current_user_payload
from app.schemas.role_schema import (
    AssignPermissionsRequest,
    RoleCreateRequest,
    RolePaginationResponse,
    RolePermissionsResponse,
    RoleResponse
)

from app.services.role_service import RoleService

import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)

role_service = RoleService()

@router.post("", response_model=RoleResponse, status_code=HTTPStatus.CREATED)
def create_role(payload: RoleCreateRequest,current_user: dict = Depends(get_current_user_payload)):
    logger.info(f"Processing create role request with name: {payload.name}")
    result = role_service.create_role(payload,current_user)
    logger.info(f"Role created successfully with id: {result.id} and name: {result.name}")
    return result

@router.get("/all", response_model=RolePaginationResponse, status_code=HTTPStatus.OK)
def get_all_roles(page: int = 1,page_size: int = 10,sort: str = "asc",payload: dict = Depends(get_current_user_payload)):
    logger.info("Processing get all roles request")
    result = role_service.get_all_roles(page,page_size,sort,payload)
    logger.info(f"Roles retrieved successfully: {len(result.items)}")
    return result

@router.get("/{role_id}", response_model=RoleResponse, status_code=HTTPStatus.OK)
def get_role(role_id: int,payload: dict = Depends(get_current_user_payload)):
    logger.info(f"Processing get role request for role_id: {role_id}")
    result = role_service.get_role_by_id(role_id,payload)
    logger.info(f"Role retrieved successfully with id: {result.id} and name: {result.name}")
    return result

@router.delete("/{role_id}", status_code=HTTPStatus.OK)
def delete_role(role_id: int,current_user: dict = Depends(get_current_user_payload)):
    logger.info(f"Processing delete role request for role_id: {role_id}")
    result=role_service.delete_role(role_id,current_user)
    logger.info(f"Role with id: {role_id} deleted successfully")
    return result

@router.get("/{role_id}/permissions",response_model=RolePermissionsResponse,status_code=HTTPStatus.OK)
def get_role_permissions(role_id: int,payload: dict = Depends(get_current_user_payload)):
    logger.info(f"Processing get role permissions request for role_id: {role_id}")
    result = role_service.get_role_permissions(role_id,payload)
    logger.info(f"Permissions retrieved successfully for role_id: {role_id}")
    return result

@router.post("/{role_id}/assign-permissions",status_code=HTTPStatus.OK)
def assign_permissions(role_id: int,payload: AssignPermissionsRequest,current_user: dict = Depends(get_current_user_payload)):
    logger.info(f"Assigning permissions to role {role_id}")
    result =role_service.assign_permissions(role_id,payload.permission_ids,current_user)
    logger.info(f"Permissions assigned successfully to role {role_id}")
    return result

@router.delete("/{role_id}/permissions/{permission_id}",status_code=HTTPStatus.OK)
def remove_permission(role_id: int, permission_id: int,payload: dict = Depends(get_current_user_payload)):
    logger.info(f"Removing permission {permission_id} from role {role_id}")
    result = role_service.remove_permission(role_id, permission_id,payload)
    logger.info(f"Permission {permission_id} removed successfully from role {role_id}")
    return result
