from sqlmodel import Session
from app.decorators.handle_error import handle_error
from app.decorators.injectables import injectable_entity
from app.models import Admin, Auth
from app.models.auth_model import Roles


class AdminService:

    def __init__(self, session: Session) -> None:
        self.session = session

    @handle_error
    @injectable_entity(Admin)
    def get_admin(self, admin_id, admin: Admin) -> dict:
        return admin.model_dump()

    @handle_error
    @injectable_entity(Admin, only_parse=True, index=0)
    @injectable_entity(Auth, only_parse=True, index=1)
    def create_admin(self, admin: dict, auth: dict) -> dict:
        admin = Admin(**admin)
        auth.update({
            "admin_id": admin.id,
            "role": Roles.ADMIN
        })
        auth = Auth(**auth)

        self.session.add(admin)
        self.session.add(auth)
        self.session.commit()

        self.session.refresh(admin)
        self.session.refresh(auth)
        return {
            "admin": admin.model_dump(mode="json"),
            "auth": auth.model_dump(
                mode="json",
                exclude={"password"}
            )
        }

    @handle_error
    @injectable_entity(Admin)
    def update_admin(self, admin_id: str, admin: Admin, **kwargs) -> dict:
        admin.update_fields(**kwargs)
        self.session.commit()
        self.session.refresh(admin)
        return admin.model_dump()

    @handle_error
    @injectable_entity(Admin)
    def delete_admin(self, admin_id: str, admin: Admin) -> dict:
        self.session.delete(admin)
        self.session.commit()
        return admin.model_dump()
