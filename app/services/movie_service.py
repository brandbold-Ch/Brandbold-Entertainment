from uuid import uuid4
from sqlalchemy import ScalarResult
from sqlmodel import Session, select
from app.decorators.handle_error import handle_error
from app.decorators.injectables import injectable_entity
from app.models import Movie, MovieGenre, MovieFranchise
from app.utils.files_tools import (save_thumbnail, save_movie,
                                   delete_thumbnail, delete_video)
from werkzeug.datastructures import FileStorage


class MovieService:

    def __init__(self, session: Session) -> None:
        self.session = session

    @handle_error
    @injectable_entity(Movie, only_parse=True, index=0)
    def create_movie(
            self,
            movie: Movie | dict,
            genres_ids: list,
            franchises_ids: list,
            thumb_file: FileStorage,
            movie_file: FileStorage
    ) -> None:
        generic_name = uuid4().__str__()
        thumb_url = save_thumbnail(thumb_file, generic_name)
        video_url = save_movie(movie_file, generic_name)

        movie = Movie(**movie)
        movie.thumbnail_url = thumb_url
        movie.video_url = video_url

        self.session.add(movie)
        self.session.commit()

        if genres_ids:
            for g in genres_ids:
                self.session.add(MovieGenre(movie_id=movie.id, genre_id=g))
            self.session.commit()
        if franchises_ids:
            for f in franchises_ids:
                self.session.add(MovieFranchise(movie_id=movie.id, franchise_id=f))
            self.session.commit()

    @handle_error
    @injectable_entity(Movie)
    def update_movie(self, movie_id: str, movie: Movie, **kwargs) -> None:
        movie.update_fields(**kwargs)
        self.session.commit()

    @handle_error
    def get_movies(self) -> ScalarResult[Movie]:
        return self.session.exec(select(Movie))

    @handle_error
    @injectable_entity(Movie)
    def delete_movie(self, movie_id: str, movie: Movie) -> None:
        self.session.delete(movie)
        self.session.commit()

        delete_thumbnail(movie.thumbnail_url)
        delete_video(movie.video_url)

    @handle_error
    @injectable_entity(Movie)
    def get_movie(self, movie_id: str, movie: Movie) -> dict:
        return movie.model_dump()
