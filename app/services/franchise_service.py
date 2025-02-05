from sqlalchemy import ScalarResult
from sqlmodel import Session, select, update
from app.decorators.handle_error import handle_error
from app.decorators.injectables import injectable_entity
from app.models import Franchise


class FranchiseService:

    def __init__(self, session: Session):
        self.session = session

    @handle_error
    @injectable_entity(Franchise, only_parse=True, index=0)
    def create_franchise(self, franchise) -> None:
        print(franchise)
        franchise = Franchise(**franchise)
        self.session.add(franchise)
        self.session.commit()

    @handle_error
    @injectable_entity(Franchise)
    def update_franchise(self, franchise_id, **kwargs) -> None:
        franchise = Franchise.model_validate(kwargs)
        query = (update(Franchise)
                 .where(Franchise.id == franchise_id)
                 .values(**franchise.model_dump(exclude_unset=True)))
        self.session.exec(query)
        self.session.commit()

    @handle_error
    def get_franchises(self) -> ScalarResult[Franchise]:
        return self.session.exec(select(Franchise))

    @handle_error
    @injectable_entity(Franchise)
    def delete_franchise(self, franchise_id, inject=None) -> None:
        self.session.delete(inject)
        self.session.commit()
