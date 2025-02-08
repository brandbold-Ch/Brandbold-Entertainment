from sqlmodel import Session
from app.config.sqlmodel_config import engine
from app.services.genre_services import GenreService
from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import jwt_required


genre_bl = Blueprint("genre", __name__, url_prefix="/genres")
genre_services = GenreService(Session(engine))


@genre_bl.route("/", methods=["GET"])
@jwt_required()
def get_genders() -> tuple[Response, int]:
    genres = genre_services.get_genres()
    genres_dict = [
        genre.model_dump(mode="json")
        for genre in genres
    ]
    return jsonify(genres_dict), 200


@genre_bl.route("/<genre_name>")
@jwt_required()
def ger_movies_by_genre(genre_name) -> tuple[Response, int]:
    genre = genre_services.get_movies_by_genre(genre_name)
    movies_dict = {
        **genre.model_dump(mode="json"),
        "movies": [
            {
                **movie.model_dump(mode="json"),
                "video_url": f"{request.host_url}movies/stream/{movie.video_url}",
                "thumbnail_url": f"{request.host_url}movies/thumbnail/{movie.thumbnail_url}",
                "genres": [
                    genre.model_dump(mode="json")
                    for genre in movie.genres
                ],
                "franchises": [
                    franchise.model_dump(mode="json")
                    for franchise in movie.franchises
                ]
            }
            for movie in genre.movies
        ]
    }
    return jsonify(movies_dict), 200
