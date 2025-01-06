from sqlmodel import Session, select
from models.movie_model import Movie
from models.genre_model import Genres


class MovieService:

    def __init__(self, session: Session):
        self.session = session

    def add_movie(self, **kwargs: dict[str, str]):
        movie = Movie(**kwargs)
        self.session.add(movie)
        self.session.commit()
        return movie.model_dump()

    def get_movies(self):
        return self.session.exec(select(Movie))
