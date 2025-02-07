from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel, Field


class MovieFranchise(SQLModel, table=True):
    movie_id: Optional[UUID] = Field(foreign_key="movie.id", primary_key=True, index=True, ondelete="CASCADE")
    franchise_id: Optional[UUID] = Field(foreign_key="franchise.id", primary_key=True, index=True, ondelete="CASCADE")
