from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from app.models.movie_franchise_model import MovieFranchise


class Franchise(SQLModel, table=True):
    id: UUID = Field(default_factory=lambda: uuid4(), primary_key=True, index=True)
    name: str
    description: str
    movies: List["Movie"] = Relationship(
        back_populates="franchises",
        link_model=MovieFranchise
    )

    def update_fields(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
