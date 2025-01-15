from enum import Enum
from models.base_user_model import BaseUser


class Plan(Enum):
    FREE = "$0"
    MONTH = "$150"
    YEAR = "$1200"


class User(BaseUser, table=True):
    subscription_plan: Plan = Plan.FREE
