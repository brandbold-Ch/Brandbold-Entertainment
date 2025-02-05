from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from app.models.movie_genre_model import MovieGenre


class Genres(Enum):
    ACTION = "Action"
    ADVENTURE = "Adventure"
    ANIMATION = "Animation"
    BIOGRAPHY = "Biography"
    COMEDY = "Comedy"
    CRIME = "Crime"
    DOCUMENTARY = "Documentary"
    DRAMA = "Drama"
    FAMILY = "Family"
    FANTASY = "Fantasy"
    HISTORY = "History"
    HORROR = "Horror"
    MUSIC = "Music"
    MYSTERY = "Mystery"
    ROMANCE = "Romance"
    SCI_FI = "Science Fiction"
    SPORT = "Sport"
    THRILLER = "Thriller"
    WAR = "War"
    WESTERN = "Western"


class Genre(SQLModel, table=True):
    id: UUID = Field(default_factory=lambda: uuid4(), primary_key=True, index=True)
    genre_name: Genres
    movies: List["Movie"] = Relationship(
        back_populates="genres",
        link_model=MovieGenre
    )
