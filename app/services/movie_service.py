from os import path, remove
from sqlalchemy import ScalarResult
from sqlalchemy.orm.sync import update
from sqlmodel import Session, select
from app.decorators.handle_error import handle_error
from app.decorators.injectables import injectable_entity
from app.models import Movie, MovieGenre, MovieFranchise


def resource(file) -> str:
    return path.abspath(path.join(__file__, f"../../static/{file}"))


class MovieService:

    def __init__(self, session: Session):
        self.session = session

    @handle_error
    @injectable_entity(Movie, only_parse=True, index=0)
    def create_movie(self, movie, genres_ids, franchises_ids) -> None:
        movie = Movie(**movie)

        self.session.add(movie)
        self.session.commit()

        if genres_ids:
            for item in genres_ids:
                self.session.add(MovieGenre(movie_id=movie.id, genre_id=item))
            self.session.commit()
        if franchises_ids:
            for item in franchises_ids:
                self.session.add(MovieFranchise(movie_id=movie.id, genre_id=item))
            self.session.commit()

    @handle_error
    @injectable_entity(Movie)
    def update_movie(self, movie_id, **kwargs) -> None:
        movie = Movie.model_validate(kwargs)
        query = (update(Movie)
                 .where(Movie.id == movie)
                 .values(**movie.model_dump(exclude_unset=True)))
        self.session.exec(query)
        self.session.commit()

    @handle_error
    def get_movies(self) -> ScalarResult[Movie]:
        return self.session.exec(select(Movie))

    @handle_error
    @injectable_entity(Movie)
    def delete_movie(self, movie_id, inject=None) -> None:
        self.session.delete(inject)
        self.session.commit()

        remove(f"{resource('movies')}/{inject.video_url}")
        remove(f"{resource('thumbnail')}/{inject.thumbnail_url}")

    @handle_error
    @injectable_entity(Movie)
    def get_movie(self, movie_id, inject=None) -> dict:
        return inject.model_dump()
