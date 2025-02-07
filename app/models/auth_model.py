from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import EmailStr
from bcrypt import hashpw, gensalt


class Roles(Enum):
    USER = "user"
    ADMIN = "admin"


class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Auth(SQLModel, table=True):
    id: UUID = Field(default_factory=lambda: uuid4(), primary_key=True, index=True)
    user_id: Optional[UUID] = Field(foreign_key="user.id", default=None, ondelete="CASCADE")
    admin_id: Optional[UUID] = Field(foreign_key="admin.id", default=None, ondelete="CASCADE")
    username: Optional[str] = Field(unique=True, index=True, default=None)
    email: EmailStr = Field(unique=True, index=True)
    password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    role: Roles = Roles.USER
    status: Status = Status.ACTIVE
    admin: "Admin" = Relationship(back_populates="auth", sa_relationship_kwargs={'uselist': False})
    user: "User" = Relationship(back_populates="auth", sa_relationship_kwargs={'uselist': False})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.password:
            self.password = self.password_hash(self.password)

    @classmethod
    def password_hash(cls, password: str) -> str:
        return hashpw(
            password.encode("utf-8"),
            gensalt(12)
        ).decode("utf-8")
