from cmath import e
import os

from app.models.user import User
from app.repository.user_repository import UserRepository
from app.core.security import hash_password, verify_password
from app.core.logger import setup_logger
from app.middleware.jwt import create_access_token
from app.exceptions.custom_exception import (
    DuplicateResourceError,
    DatabaseError,
    BadRequest,
    ServiceError,
    UnauthorizedError
)
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse

logger = setup_logger(__name__)

class UserService:

    def __init__(self):
        self.repo = UserRepository()

    def create_user(self, payload: UserCreate, profile_pic):

        existing_user = self.repo.get_existing_user(payload.email, payload.username)

        if existing_user:
            raise BadRequest(
                f"Email '{payload.email}' or username '{payload.username}' already exists"
            )

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
                    "username": user.username
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