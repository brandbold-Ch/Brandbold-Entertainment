from sqlalchemy import ScalarResult
from sqlmodel import Session, select, update
from app.decorators.handle_error import handle_error
from app.decorators.injectables import injectable_entity
from app.models import Genre


class GenreService:

    def __init__(self, session: Session):
        self.session = session

    @handle_error
    @injectable_entity(Genre, only_parse=True, index=0)
    def create_genre(self, genre) -> None:
        genre = Genre(**genre)
        self.session.add(genre)
        self.session.commit()

    @handle_error
    @injectable_entity(Genre)
    def update_movie(self, genre_id, **kwargs) -> None:
        genre = Genre.model_validate(kwargs)
        query = (update(Genre)
                 .where(Genre.id == genre_id)
                 .values(**genre.model_dump(exclude_unset=True)))
        self.session.exec(query)
        self.session.commit()

    @handle_error
    def get_genres(self) -> ScalarResult[Genre]:
        return self.session.exec(select(Genre))

    @handle_error
    @injectable_entity(Genre)
    def delete_genre(self, genre_id, inject=None) -> None:
        self.session.delete(inject)
        self.session.commit()
