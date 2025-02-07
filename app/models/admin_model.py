from sqlmodel import Relationship
from app.models.base_user_model import BaseUser


class Admin(BaseUser, table=True):
    auth: "Auth" = Relationship(back_populates="admin",
                                sa_relationship_kwargs={"cascade": "all, delete-orphan"})
