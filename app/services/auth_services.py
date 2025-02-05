from sqlmodel import Session, select, update
from app.decorators.handle_error import handle_error
from app.exceptions.exceptions import NotFound
from app.models import Auth


class AuthService:

    def __init__(self, session: Session):
        self.session = session

    @handle_error
    def get_auth(self, auth_id) -> dict:
        query = select(Auth).where(Auth.id == auth_id)
        auth: Auth = self.session.exec(query).first()

        if not auth:
            raise NotFound("Auth not found")

        return auth.model_dump()

    @handle_error
    def create_auth(self, **kwargs) -> dict:
        admin = Auth(**kwargs)
        self.session.add(admin)
        self.session.commit()
        self.session.refresh(admin)
        return admin.model_dump()

    @handle_error
    def update_auth(self, auth_id, **kwargs) -> dict:
        query = update(Auth).where(Auth.id == auth_id).values(**kwargs)
        auth = self.session.exec(query)
        self.session.commit()
        return auth.model_dump()
