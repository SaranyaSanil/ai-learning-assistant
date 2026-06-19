from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text
from app.core.database import Base
from sqlalchemy.orm import relationship

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"),primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"),primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    profile_image_url = Column(String, nullable=True)  
    role_id = Column(
        Integer,
        ForeignKey("roles.id")
    )
    role = relationship("Role",back_populates="users")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    users = relationship("User",back_populates="role")
    permissions = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles"
    )

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    roles = relationship(
        "Role",
        secondary=role_permissions,
        back_populates="permissions"
    )

class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(1000), nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)