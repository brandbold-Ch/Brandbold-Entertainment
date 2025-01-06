from datetime import time, datetime
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field
from typing_extensions import Optional


class Device(SQLModel, table=True):
    id: UUID = Field(default_factory=lambda: uuid4(), primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="user.id")
    device_branch: str
    device_model: str
    ip_address: str
    last_used_at: Optional[datetime]
