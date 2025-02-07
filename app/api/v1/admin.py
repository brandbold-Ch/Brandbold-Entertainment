from app.config.sqlmodel_config import engine
from app.services.admin_services import AdminService
from app.services.auth_services import AuthService
from flask import Blueprint, request, jsonify, Response, render_template
from app.exceptions.exceptions import DataValidationError
from sqlmodel import Session
from app.services import MovieService, GenreService, FranchiseService, UserServices
from werkzeug.datastructures import FileStorage

admin_bl = Blueprint("admin", __name__,
                     url_prefix="/admins",
                     template_folder="../templates")
admin_service = AdminService(Session(engine))
movie_services = MovieService(Session(engine))
genre_service = GenreService(Session(engine))
franchise_service = FranchiseService(Session(engine))
user_service = UserServices(Session(engine))
auth_service = AuthService(Session(engine))


@admin_bl.route("/", methods=["GET"])
def dashboard_view() -> str:
    return render_template("dashboard_view.html")


@admin_bl.route("/franchises", methods=["GET", "POST"])
@admin_bl.route("/franchises/<uuid:franchise_id>", methods=["DELETE"])
def franchises_view(franchise_id=None) -> str:
    if request.method == "POST":
        data = request.form.to_dict()
        franchise_service.create_franchise(data)

    elif request.method == "DELETE":
        franchise_service.delete_franchise(franchise_id)

    franchises = franchise_service.get_franchises()
    return render_template("franchises_view.html", data=franchises)


@admin_bl.route("/movies", methods=["GET"])
@admin_bl.route("/movies/<uuid:movie_id>", methods=["PUT", "DELETE"])
def movies_view(movie_id=None) -> str:
    if request.method == "DELETE":
        movie_services.delete_movie(movie_id)

    elif request.method == "PUT":
        movie_services.update_movie(movie_id, **request.get_json())

    movies = movie_services.get_movies()
    return render_template("movies_view.html", data=movies)


@admin_bl.route("/movies/upload", methods=["GET", "POST"])
def upload_movie_view() -> str:
    if request.method == "POST":
        video_file: FileStorage = request.files.get("video_url")
        thumb_file: FileStorage = request.files.get("thumbnail_url")
        genres = request.form.getlist("genre")
        franchises = request.form.getlist("franchise")
        data = request.form.to_dict()

        movie_services.create_movie(data, genres, franchises,
                                    thumb_file, video_file)

    genres = genre_service.get_genres()
    franchises = franchise_service.get_franchises()
    return render_template(
        "upload_movie.html",
        data={
            "genres": genres,
            "franchises": franchises
        }
    )


@admin_bl.route("/users", methods=["GET"])
@admin_bl.route("/users/<uuid:user_id>", methods=["PUT", "DELETE"])
def users_view(user_id=None) -> str:
    if request.method == "DELETE":
        user_service.delete_user(user_id)

    elif request.method == "PUT":
        auth_service.update_status()
        ...

    users = user_service.get_users()
    return render_template("users_view.html", data=users)


@admin_bl.route("/video_streaming/<movie_path>", methods=["GET"])
def video_streaming_view(movie_path: str) -> str:
    return render_template("video_streaming.html", file=movie_path)


@admin_bl.route("/genres", methods=["GET", "POST"])
@admin_bl.route("/genres/<uuid:genre_id>", methods=["DELETE", "PUT"])
def genres_view(genre_id=None) -> str:
    if request.method == "POST":
        data = request.form.to_dict()
        genre_service.create_genre(data)

    elif request.method == "DELETE":
        genre_service.delete_genre(genre_id)

    genres = genre_service.get_genres()
    return render_template("categories_view.html", data=genres)


@admin_bl.route("/<uuid:admin_id>", methods=["GET"])
def get_admin(admin_id) -> tuple[Response, int]:
    admin = admin_service.get_admin(admin_id)
    return jsonify(admin), 200


@admin_bl.route("/", methods=["POST"])
def create_admin() -> tuple[Response, int]:
    data = request.get_json()

    if "admin" not in data or "auth" not in data:
        raise DataValidationError("Don't found admin key or auth key")

    result = (admin_service
              .create_admin(data["admin"], data["auth"]))
    return jsonify(result), 201


@admin_bl.route("/<uuid:admin_id>", methods=["PUT"])
def update_admin(admin_id) -> tuple[Response, int]:
    data = admin_service.update_admin(admin_id, **request.get_json())
    return jsonify(data), 202


@admin_bl.route("/<uuid:admin_id>", methods=["DELETE"])
def delete_admin(admin_id) -> tuple[Response, int]:
    data = admin_service.delete_admin(admin_id)
    return jsonify(data), 200
