from sqlalchemy import ScalarResult
from sqlmodel import Session, select
from app.decorators.handle_error import handle_error
from app.decorators.injectables import injectable_entity
from app.models import Franchise


class FranchiseService:

    def __init__(self, session: Session) -> None:
        self.session = session

    @handle_error
    @injectable_entity(Franchise, only_parse=True, index=0)
    def create_franchise(self, franchise) -> None:
        self.session.add(Franchise(**franchise))
        self.session.commit()

    @handle_error
    @injectable_entity(Franchise)
    def update_franchise(self, franchise_id: str,
                         franchise: Franchise, **kwargs) -> None:
        franchise.update_fields(**kwargs)
        self.session.commit()

    @handle_error
    def get_franchises(self) -> ScalarResult[Franchise]:
        return self.session.exec(select(Franchise))

    @handle_error
    @injectable_entity(Franchise)
    def delete_franchise(self, franchise_id: str,
                         franchise: Franchise) -> None:
        self.session.delete(franchise)
        self.session.commit()
