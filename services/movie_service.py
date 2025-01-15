from os import listdir, path, remove

from sqlalchemy import ScalarResult
from sqlalchemy.engine import TupleResult
from sqlmodel import Session, select, delete

from decorators.handle_error import handle_error
from models.movie_model import Movie
from models.genre_model import Genres


def resource(file) -> str:
    return path.abspath(path.join(__file__, f"../../static/{file}"))


class MovieService:

    def __init__(self, session: Session):
        self.session = session

    @handle_error
    def add_movie(self, **kwargs) -> None:
        movie = Movie(**kwargs)
        self.session.add(movie)
        self.session.commit()

    @handle_error
    def get_movies(self) -> ScalarResult[Movie]:
        return self.session.exec(select(Movie))

    @handle_error
    def del_movie(self, movie_id) -> None:
        query = select(Movie).where(Movie.id == movie_id)
        movie = self.session.exec(query).first()
        self.session.delete(movie)
        self.session.commit()

        remove(f"{resource('movies')}/{movie.video_url}")
        remove(f"{resource('thumbnail')}/{movie.thumbnail_url}")

    @handle_error
    def get_movie(self, movie_id) -> Movie:
        query = select(Movie).where(Movie.id == movie_id)
        return self.session.exec(query).first()
