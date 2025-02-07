from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field


class BaseUser(SQLModel):
    id: UUID = Field(default_factory=lambda: uuid4(), primary_key=True, index=True)
    first_name: str
    last_name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    last_login: Optional[datetime] = None

    def update_fields(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)
