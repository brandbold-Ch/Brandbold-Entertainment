from datetime import time, datetime
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field
from typing_extensions import Optional


class WatchHistory(SQLModel, table=True):
    id: UUID = Field(default_factory=lambda: uuid4(), primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="user.id")
    movie_id: UUID = Field(foreign_key="movie.id")
    watched_at: datetime = Field(default_factory=lambda: datetime.now())
    last_position: Optional[time]
    