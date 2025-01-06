from models.base_user_model import BaseUser


class Admin(BaseUser, table=True):
    ...
