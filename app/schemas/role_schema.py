from pydantic import BaseModel
from typing import List, Optional


class RoleCreateRequest(BaseModel):
    name: str


class RoleUpdateRequest(BaseModel):
    name: Optional[str] = None


class RoleResponse(BaseModel):
    id: int
    name: str

class RolePaginationResponse(BaseModel):
    items: List[RoleResponse]
    total: int
    page: int
    page_size: int

class AssignPermissionsRequest(BaseModel):
    permission_ids: list[int]
    
class RolePermissionsResponse(BaseModel):
    role_id: int
    role_name: str
    permissions: list[str]

    class Config:
        from_attributes = True