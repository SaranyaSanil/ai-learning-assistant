from cmath import e
from datetime import datetime
import os
from jose import jwt
from app.services.permission_service import PermissionService
from app.models.user import User
from app.repository.user_repository import UserRepository
from app.core.security import hash_password, verify_password
from app.core.logger import setup_logger
from app.middleware.jwt import SECRET_KEY, create_access_token,verify_access_token
from app.exceptions.custom_exception import (
    DuplicateResourceError,
    DatabaseError,
    ExpiredSignatureError,
    InvalidTokenError,
    BadRequest,
    ResourceNotFoundError,
    ServiceError,
    UnauthorizedError
)
from app.schemas.user_schema import AssignRoleResponse, UserCreate, UserLogin, UserResponse

logger = setup_logger(__name__)

class UserService:

    def __init__(self):
        self.repo = UserRepository()
        self.permission_service = PermissionService(self.repo)

    def create_user(self, payload: UserCreate, profile_pic):

        existing_user = self.repo.get_existing_user(payload.email, payload.username)
        if existing_user:
            raise BadRequest(f"Email '{payload.email}' or username '{payload.username}' already exists")

        try:
            # default value
            profile_image_url = None
            # if image uploaded
            if profile_pic:
                os.makedirs("uploads", exist_ok=True)
                file_location = f"uploads/{profile_pic.filename}"
                with open(file_location, "wb") as file:
                    file.write(profile_pic.file.read())
                profile_image_url = file_location
            user = User(
                name=payload.name,
                username=payload.username,
                email=payload.email,
                password=hash_password(payload.password),
                profile_image_url=profile_image_url
            )

            result = self.repo.create(user)
            return UserResponse(
                id=result.id,
                name=result.name,
                username=result.username,
                email=result.email,
                profile_image_url=result.profile_image_url
            )

        except Exception as e:
            print("ERROR:", str(e))
            raise ServiceError("Failed to create user")
        
    def login_user(self, payload: UserLogin):
        try:
            user = self.repo.get_by_username(payload.username)
            if not user:
                raise UnauthorizedError("Invalid credentials")
            if not verify_password(payload.password,user.password):
                raise UnauthorizedError("Invalid credentials")
            token = create_access_token(
                {
                    "user_id": user.id,
                    "username": user.username,
                    "role_id": user.role_id
                }
            )
            return {
                "access_token": token,
                "token_type": "bearer"
            }

        except UnauthorizedError:
            raise
        except Exception as e:
            logger.error(str(e))
            raise ServiceError("Failed to login user" )
        
    def get_current_user(self, payload: dict):
        try:
            user_id = payload.get("user_id")
            user = self.repo.get_by_id(user_id)
            if not user:
                raise UnauthorizedError("User not found")
            return UserResponse(
                id=user.id,
                name=user.name,
                username=user.username,
                email=user.email,
                profile_image_url=user.profile_image_url
            )
        except UnauthorizedError:
            raise
        except Exception as e:
            logger.error(str(e))
            raise ServiceError("Failed to retrieve current user")
        
    def assign_role_to_user(self,user_id: int,role_id: int, current_user: dict):
        try:
            if not self.permission_service.has_permission(current_user["user_id"],"ASSIGN_ROLE"):
                raise UnauthorizedError("You don't have permission to assign roles")
            
            user = self.repo.get_by_id(user_id)
            if not user:
                raise ResourceNotFoundError("User not found")

            role = self.repo.get_role_by_id(role_id)

            if not role:
                raise ResourceNotFoundError("Role not found")

            updated_user = self.repo.assign_role(
                user_id,
                role_id
            )

            return AssignRoleResponse(
                id=updated_user.id,
                username=updated_user.username,
                role_id=updated_user.role_id
            )
        except UnauthorizedError:
            raise
        except ResourceNotFoundError:
            raise
        except Exception as e:
            logger.error(str(e))
            raise ServiceError("Failed to assign role to user")
            
    def delete_user(self,user_id: int,payload: dict):

        try:
            if not self.permission_service.has_permission(payload["user_id"],"DELETE_USER"):
                raise UnauthorizedError("You don't have permission to delete users")

            user = self.repo.delete_user(user_id)
            if not user:
                raise ResourceNotFoundError("User not found")

            return {
                "message": "User deleted successfully"
            }

        except UnauthorizedError:
            raise
        except ResourceNotFoundError:
            raise
        except Exception as e:
            logger.error(str(e))
            raise ServiceError(
                "Failed to delete user"
            )
        
    def get_all_users(self,payload: dict):
        try:
            if not self.permission_service.has_permission(payload["user_id"],"USER_LIST"):
                raise UnauthorizedError("You don't have permission to view users")
            users = self.repo.get_all_users()
            return [
                UserResponse(
                    id=user.id,
                    name=user.name,
                    username=user.username,
                    email=user.email,
                    profile_image_url=user.profile_image_url
                ) for user in users
            ]
        except UnauthorizedError:
            raise
        except Exception as e:
            logger.error(str(e))
            raise ServiceError("Failed to retrieve all users")
        

    def get_user_by_id(self,user_id: int,payload: dict):
        try:
            if not self.permission_service.has_permission(payload["user_id"],"USER_VIEW"):
                raise UnauthorizedError("You don't have permission to view this user")

            user = self.repo.get_by_id(user_id)
            if not user:
                raise ResourceNotFoundError("User not found")
            return UserResponse(
                id=user.id,
                name=user.name,
                username=user.username,
                email=user.email,
                profile_image_url=user.profile_image_url
            )   
        except ResourceNotFoundError:
            raise
        except Exception as e:
            logger.error(str(e))
            raise ServiceError("Failed to retrieve user by id")
        
         
    def change_password(self, payload, current_user: dict):
        try:

            user = self.repo.get_by_id(current_user["user_id"])
            if not user:
                raise ResourceNotFoundError("User not found")
            # verify old password
            if not verify_password(payload.old_password,user.password):
                raise UnauthorizedError("Old password is incorrect")
            # hash new password
            hashed_password = hash_password(payload.new_password)

            updated_user = self.repo.change_password(user,hashed_password)

            return {
                "success": True,
                "message": "Password changed successfully"
            }

        except ResourceNotFoundError:
            raise
        except UnauthorizedError:
            raise
        except Exception as e:
            logger.error(str(e))
            raise ServiceError(
                "Failed to change password"
            )    
        
    def update_user( self, user_id: int,payload,current_user: dict):
        try:
            if not self.permission_service.has_permission(current_user["user_id"],"USER_UPDATE"):
                raise UnauthorizedError("You don't have permission to update users")

            user = self.repo.get_by_id(user_id)
            if not user:
                raise ResourceNotFoundError("User not found")
            # permission check
            # update fields here
            if payload.name is not None:
                user.name = payload.name

            if payload.username is not None:
                user.username = payload.username

            if payload.email is not None:
                user.email = payload.email

            updated_user = self.repo.update_user(user)

            return UserResponse(
                id=updated_user.id,
                name=updated_user.name,
                username=updated_user.username,
                email=updated_user.email,
                role_id=updated_user.role_id
            )

        except ResourceNotFoundError:
            raise
        except UnauthorizedError:
            raise
        except DuplicateResourceError:
            raise
        except Exception as e:
            logger.error(str(e))
            raise ServiceError(
                "Failed to update user"
            )
   
    def get_user_permissions(self, user_id: int, payload: dict = None):
        try:
            if payload and not self.permission_service.has_permission(payload["user_id"], "USER_VIEW"):
                raise UnauthorizedError("You don't have permission to view user permissions")

            result = self.repo.get_user_permissions(user_id)
            if not result:
                raise ResourceNotFoundError("User not found")
            user, permissions = result
            return {
                "user_id": user.id,
                "permissions": [
                    {
                        "id": p.id,
                        "name": p.name
                    }
                    for p in permissions
                ]
            }
        except ResourceNotFoundError:
            raise
        except Exception as e:
            logger.error(str(e))
            raise ServiceError("Failed to fetch user permissions")
        
    def logout_user(self, token: str):
        try:
            if self.repo.is_blacklisted(token):
                return {"message": "Already logged out"}
            
            payload = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
            expires_at = datetime.fromtimestamp(payload["exp"])
            self.repo.add_blacklisted_token(token,expires_at)     
            return {"message": "Logged out successfully"}
        
        except ExpiredSignatureError:
            raise UnauthorizedError("Token has expired")
        except InvalidTokenError:
            raise UnauthorizedError("Invalid token")
        except Exception as e:
            logger.error(str(e))
            raise ServiceError("Failed to logout user")