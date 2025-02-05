from datetime import time, datetime
from typing import List
from uuid import uuid4, UUID
from sqlmodel import SQLModel, Field, Relationship
from typing_extensions import Optional

from app.models.franchise_model import Franchise
from app.models.movie_genre_model import MovieGenre
from app.models.movie_franchise_model import MovieFranchise


class Movie(SQLModel, table=True):
    id: UUID = Field(default_factory=lambda: uuid4(), primary_key=True, index=True)
    title: str
    description: str
    release_year: int
    rating: Optional[float] = None
    duration: str
    thumbnail_url: str
    video_url: str
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: Optional[datetime] = None
    genres: List["Genre"] = Relationship(
        back_populates="movies",
        link_model=MovieGenre
    )
    franchises: List["Franchise"] = Relationship(
        back_populates="movies",
        link_model=MovieFranchise
    )

