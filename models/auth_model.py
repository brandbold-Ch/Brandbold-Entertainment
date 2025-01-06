from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import EmailStr
from bcrypt import hashpw, gensalt


class Roles(Enum):
    USER = "user"
    ADMIN = "admin"


class Auth(SQLModel, table=True):
    id: UUID = Field(default_factory=lambda: uuid4(), primary_key=True, index=True)
    user_id: Optional[UUID] = Field(foreign_key="user.id")
    admin_id: Optional[UUID] = Field(foreign_key="admin.id")
    username: str = Field(unique=True, index=True)
    email: EmailStr = Field(unique=True, index=True)
    password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    role: Roles

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
