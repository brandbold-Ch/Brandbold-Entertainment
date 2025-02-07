from sqlmodel import Session, select, update
from app.decorators.handle_error import handle_error
from app.decorators.injectables import injectable_entity
from app.exceptions.exceptions import NotFound
from app.models import Auth
from app.exceptions.exceptions import NotFound
from app.models.auth_model import Status


class AuthService:

    def __init__(self, session: Session) -> None:
        self.session = session

    @handle_error
    def get_auth_by_id(self, auth_id: str) -> dict:
        query = select(Auth).where(Auth.id == auth_id)
        auth: Auth = self.session.exec(query).first()

        if not auth:
            raise NotFound("Auth ID not found")

        return auth.model_dump()

    @handle_error
    def get_auth_by_username(self, username: str):
        query = (select(Auth)
                 .where(Auth.username == username))
        auth: Auth = self.session.exec(query).first()

        if not auth:
            raise NotFound("Username not found")

        return auth.model_dump()

    @handle_error
    def get_auth_by_email(self, email: str):
        query = (select(Auth)
                 .where(Auth.email == email))
        auth: Auth = self.session.exec(query).first()

        if not auth:
            raise NotFound("Email not found")

        return auth.model_dump()

    @handle_error
    def create_auth(self, **kwargs) -> dict:
        admin = Auth(**kwargs)
        self.session.add(admin)
        self.session.commit()
        self.session.refresh(admin)

        return admin.model_dump()

    @handle_error
    @injectable_entity(Auth)
    def update_status(self, auth_id: str,
                      auth: Auth, status: str) -> None:
        auth.status = Status(status)
        self.session.commit()
