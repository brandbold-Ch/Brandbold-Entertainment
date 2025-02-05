from sqlmodel import Session
from app.config.sqlmodel_config import engine
from app.services.movie_service import MovieService
from flask import Blueprint, jsonify, send_file


movie_bl = Blueprint("movie", __name__, url_prefix="/movies")
movie_services = MovieService(Session(engine))


@movie_bl.route("/", methods=["GET"])
def get_movies():
    movies = movie_services.get_movies()
    movies_dict = {
        "movies": []
    }
    genres = []
    franchises = []

    for movie in movies:

        for genre in movie.genres:
            genres.append(genre.model_dump(mode="json"))

        for franchise in movie.franchises:
            franchises.append(franchise.model_dump(mode="json"))

        m = movie.model_dump(mode="json")
        m["genres"] = genres
        m["franchises"] = franchises
        movies_dict["movies"].append(m)
        print(movies_dict)
    return jsonify(movies_dict)
