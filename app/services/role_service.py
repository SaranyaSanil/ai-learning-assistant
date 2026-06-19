from unittest import result
from app.repository.user_repository import UserRepository
from app.services.permission_service import PermissionService
from app.repository.role_repository import RoleRepository
from app.schemas.role_schema import (
    RoleCreateRequest,
    RolePaginationResponse,
    RolePermissionsResponse,
    RoleResponse
)
from app.exceptions.custom_exception import (
    DuplicateResourceError,
    ResourceNotFoundError,
    ServiceError,
    UnauthorizedError
)

import logging

logger = logging.getLogger(__name__)


class RoleService:

    def __init__(self):
        self.repo = RoleRepository()
        self.permission_service = PermissionService(UserRepository())

    def create_role(self, payload: RoleCreateRequest, current_user: dict):
        try:
            if not self.permission_service.has_permission(current_user["user_id"], "ROLE_CREATE"):
                raise UnauthorizedError("You don't have permission to create roles")
            
            role = self.repo.create_role(payload)
            return RoleResponse(
                id=role.id,
                name=role.name
            )
        except DuplicateResourceError:
            raise DuplicateResourceError(f"Role with name '{payload.name}' already exists")
        except UnauthorizedError:
            raise
        except Exception as e:
            logger.error(str(e))
            raise ServiceError("Failed to create role")
        
    def get_all_roles(self, page: int = 1, page_size: int = 10, sort: str = "asc",payload: dict = None):
        try:
            if not self.permission_service.has_permission(payload["user_id"], "ROLE_VIEW"):
                raise UnauthorizedError("You don't have permission to view roles")
            
            roles,total = self.repo.get_all_roles(page, page_size, sort)
            return RolePaginationResponse(
                items=[
                    RoleResponse(id=role.id, name=role.name)
                    for role in roles
                ],
                total=total,
                page=page,
                page_size=page_size
            )
        except UnauthorizedError:
            raise
        except Exception as e:
            logger.error(str(e))
            raise ServiceError("Failed to retrieve roles")
        
    def get_role_by_id(self, role_id: int,payload: dict= None):
        try:
            if not self.permission_service.has_permission(payload["user_id"], "ROLE_VIEW"):
                raise UnauthorizedError("You don't have permission to view roles")
            role = self.repo.get_role_by_id(role_id)
            if not role:
                raise ResourceNotFoundError("Role not found")
            return RoleResponse(
                id=role.id,
                name=role.name
            )
        except ResourceNotFoundError:
            raise
        except UnauthorizedError:
            raise
        except ServiceError:
            raise
        except Exception as e:
            logger.error(str(e))
            raise ServiceError("Failed to retrieve role")
        
    def delete_role(self, role_id: int, current_user: dict):
        try:
            if not self.permission_service.has_permission(current_user["user_id"], "ROLE_DELETE"):
                raise UnauthorizedError("You don't have permission to delete roles")    
            
            role=self.repo.delete_role(role_id)
            if not role:
                raise ResourceNotFoundError("Role not found")
            return {"message": "Role deleted successfully"}
        except ResourceNotFoundError:
            raise 
        except UnauthorizedError:
            raise
        except Exception as e:
            logger.error(str(e))
            raise ServiceError("Failed to delete role")
        
    def get_role_permissions(self, role_id: int, payload: dict = None):
        try:
            if not self.permission_service.has_permission(payload["user_id"], "ROLE_VIEW"):
                raise UnauthorizedError("You don't have permission to view role permissions")

            role = self.repo.get_role_permissions(role_id)
            if not role:
                raise ResourceNotFoundError("Role not found")
            return RolePermissionsResponse(
                role_id=role.id,
                role_name=role.name,
                permissions=[
                    permission.name
                    for permission in role.permissions
                ]
            )
        except ResourceNotFoundError:
            raise
        except Exception as e:
            logger.error(str(e))
            raise ServiceError("Failed to retrieve role permissions")
        
    def assign_permissions(self, role_id: int, permission_ids: list[int],current_user: dict):
        try:
            if not self.permission_service.has_permission(current_user["user_id"], "MANAGE_PERMISSIONS"):
                raise UnauthorizedError("You don't have permission to edit roles")

            result = self.repo.assign_permissions(role_id, permission_ids)

            if not result:
                raise ResourceNotFoundError("Role not found")

            role, permissions, new_permissions = result

            found_ids = {p.id for p in permissions}

            missing = set(permission_ids) - found_ids

            if missing:
                raise ResourceNotFoundError(
                    f"Permissions not found: {list(missing)}"
                )

            if len(new_permissions) == 0:
                raise DuplicateResourceError(
                    "Permissions already assigned to role"
                )

            return {
                "message": "Permissions assigned successfully"
            }

        except ResourceNotFoundError:
            raise
        except UnauthorizedError:
            raise
        except DuplicateResourceError:
            raise

        except Exception as e:
            logger.error(str(e))
            raise ServiceError("Failed to assign permissions")
                
    def remove_permission(self, role_id: int, permission_id: int,payload: dict):
        try:
            if not self.permission_service.has_permission(payload["user_id"], "MANAGE_PERMISSIONS"):
                raise UnauthorizedError("You don't have permission to edit roles")

            result = self.repo.remove_permission(role_id, permission_id)
            if not result:
                raise ResourceNotFoundError("Role not found")
            role, permission = result
            if permission is None:
                raise ResourceNotFoundError("Permission not found in role")
            return {
                "message": "Permission removed successfully from role"
            }
        except ResourceNotFoundError:
            raise
        except Exception as e:
            logger.error(str(e))
            raise ServiceError("Failed to remove permission from role") 
        
    