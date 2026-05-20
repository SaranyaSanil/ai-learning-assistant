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

# ---------- RESPONSE ----------
class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    profile_image_url: str | None = None


    class Config:
        from_attributes = True   