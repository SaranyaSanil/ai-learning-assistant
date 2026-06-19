from typing import Optional

from fastapi import Form
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        username: str = Form(...),
        email: EmailStr = Form(...),
        password: str = Form(...)
    ):
        return cls(
            name=name,
            username=username,
            email=email,
            password=password
        )


class UserLogin(BaseModel):
    username: str
    password: str 

class AssignRoleRequest(BaseModel):
    role_id: int


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

# ---------- RESPONSE ----------
class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    profile_image_url: str | None = None
    role_id: Optional[int] = None

class AssignRoleResponse(BaseModel):
    id: int
    username: str
    role_id: int
    
    class Config:
        from_attributes = True   