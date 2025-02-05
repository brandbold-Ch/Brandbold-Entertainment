from enum import Enum

from sqlmodel import Relationship

from app.models.base_user_model import BaseUser


class Plan(Enum):
    FREE = "$0"
    MONTH = "$150"
    YEAR = "$1200"


class User(BaseUser, table=True):
    subscription_plan: Plan = Plan.FREE
    auth: "Auth" = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
