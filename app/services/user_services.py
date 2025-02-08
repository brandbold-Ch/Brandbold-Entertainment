from sqlalchemy import ScalarResult
from sqlmodel import Session, select
from app.decorators.handle_error import handle_error
from app.decorators.injectables import injectable_entity
from app.models import Admin, Auth, User
from app.models.auth_model import Roles


class UserServices:

    def __init__(self, session: Session):
        self.session = session

    @handle_error
    @injectable_entity(User, only_parse=True, index=0)
    @injectable_entity(Auth, only_parse=True, index=1)
    def create_user(self, user: dict, auth: dict) -> dict:
        user = User(**user)
        auth.update({"user_id": user.id, "role": Roles.USER})
        auth = Auth(**auth)

        self.session.add(user)
        self.session.add(auth)
        self.session.commit()

        self.session.refresh(user)
        self.session.refresh(auth)
        return {
            "user": user.model_dump(mode="json"),
            "auth": auth.model_dump(
                mode="json",
                exclude={"password"}
            )
        }

    @handle_error
    def get_users(self) -> ScalarResult[User]:
        return self.session.exec(select(User))

    @handle_error
    @injectable_entity(User)
    def delete_user(self, user_id: str, user: User) -> dict:
        self.session.delete(user)
        self.session.commit()
        return user.model_dump()
