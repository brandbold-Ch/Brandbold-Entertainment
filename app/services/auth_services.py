from re import match

import bcrypt
from sqlmodel import Session, select
from app.decorators.handle_error import handle_error
from app.decorators.injectables import injectable_entity
from app.models import Auth
from app.exceptions.exceptions import NotFoundException, PasswordMismatchException
from app.models.auth_model import Status


class AuthService:

    def __init__(self, session: Session) -> None:
        self.session = session

    @handle_error
    def get_auth_by_id(self, auth_id: str) -> dict:
        query = select(Auth).where(Auth.id == auth_id)
        auth: Auth = self.session.exec(query).first()

        if not auth:
            raise NotFoundException("Auth ID not found")

        return auth.model_dump()

    @handle_error
    def get_auth_by_username(self, username: str) -> Auth:
        query = (select(Auth)
                 .where(Auth.username == username))
        auth: Auth = self.session.exec(query).first()

        if not auth:
            raise NotFoundException("Username not found")
        return auth

    @handle_error
    def get_auth_by_email(self, email: str) -> Auth:
        query = (select(Auth)
                 .where(Auth.email == email))
        auth: Auth = self.session.exec(query).first()

        if not auth:
            raise NotFoundException("Email not found")
        return auth

    @handle_error
    def get_auth(self, username: str, password: str) -> dict:
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if match(regex, username):
            auth = self.get_auth_by_email(username)
        else:
            auth = self.get_auth_by_username(username)

        if not bcrypt.checkpw(password.encode("utf-8"),
                              auth.password.encode("utf-8")):
            raise PasswordMismatchException("Incorrect Password")
        return auth.user.model_dump(mode="json")

    @handle_error
    def create_auth(self, **kwargs) -> dict:
        auth = Auth(**kwargs)
        self.session.add(auth)
        self.session.commit()
        self.session.refresh(auth)
        return auth.model_dump()

    @handle_error
    @injectable_entity(Auth)
    def update_status(self, auth_id: str, auth: Auth, **kwargs) -> None:
        auth.status = Status(kwargs["status"])
        self.session.commit()
