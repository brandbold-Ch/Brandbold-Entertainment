from datetime import time, datetime
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field
from typing_extensions import Optional


class Movie(SQLModel, table=True):
    id: UUID = Field(default_factory=lambda: uuid4(), primary_key=True, index=True)
    title: str
    description: str
    release_year: int
    rating: Optional[float]
    duration: str
    thumbnail_url: str
    video_url: str
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime]
