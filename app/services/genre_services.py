from sqlalchemy import ScalarResult
from sqlmodel import Session, select, update
from app.decorators.handle_error import handle_error
from app.decorators.injectables import injectable_entity
from app.models import Genre, Genres


class GenreService:

    def __init__(self, session: Session):
        self.session = session

    @handle_error
    @injectable_entity(Genre, only_parse=True, index=0)
    def create_genre(self, genre: Genre | dict) -> None:
        genre = Genre(**genre)
        self.session.add(genre)
        self.session.commit()

    @handle_error
    @injectable_entity(Genre)
    def update_genre(self, genre_id: str,
                     genre: Genre, **kwargs) -> None:
        genre.update_fields(**kwargs)
        self.session.commit()

    @handle_error
    def get_genres(self) -> ScalarResult[Genre]:
        return self.session.exec(select(Genre))

    @handle_error
    @injectable_entity(Genre)
    def delete_genre(self, genre_id: str, genre: Genre) -> None:
        self.session.delete(genre)
        self.session.commit()

    @handle_error
    def get_movies_by_genre(self, genre_name) -> Genre:
        query = (select(Genre)
                 .where(Genre.genre_name == Genres(genre_name)))
        genre: Genre = self.session.exec(query).first()
        return genre
