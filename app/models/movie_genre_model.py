from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel, Field


class MovieGenre(SQLModel, table=True):
    movie_id: Optional[UUID] = Field(foreign_key="movie.id", primary_key=True, index=True, ondelete="CASCADE")
    genre_id: Optional[UUID] = Field(foreign_key="genre.id", primary_key=True, index=True, ondelete="CASCADE")
