from app.config.sqlmodel_config import engine
from app.services.admin_services import AdminService
from flask import Blueprint, request, jsonify, Response, render_template
from app.exceptions.exceptions import DataValidationError
from sqlmodel import Session
from app.services import MovieService, GenreService, FranchiseService
from uuid import uuid4
from os import path
from werkzeug.datastructures import FileStorage

admin_bl = Blueprint("admin", __name__,
                     url_prefix="/admin",
                     template_folder="../templates")
admin = AdminService(Session(engine))
movie_services = MovieService(Session(engine))
genre_service = GenreService(Session(engine))
franchise_service = FranchiseService(Session(engine))

RESOURCES_DIR = "../../../../static"
THUMBNAIL_DIR = "thumbnail"
MOVIES_DIR = "movies"
THUMBNAIL_EXT = "webp"


def res_path(file: str, _type: str, _dir: str) -> str:
    filename = f"{RESOURCES_DIR}/{_dir}/{file}.{_type}"
    return path.abspath(path.join(__file__, filename))


def select_format(content: str) -> str:
    match content:
        case "video/mp4":
            return "mp4"
        case "video/x-matroska":
            return "mkv"
        case "video/webm":
            return "webm"
        case "video/ogg":
            return "ogg"
        case "video/avi":
            return "avi"


def save_file(file: FileStorage, filename: str,
              extension: str, directory: str) -> None:
    file_path = res_path(filename, extension, directory)
    with open(file_path, "wb") as f:
        f.write(file.read())


@admin_bl.route("/delete_movie/<uuid:movie_id>", methods=["DELETE"])
def delete_movie(movie_id) -> Response:
    movie_services.delete_movie(movie_id)
    return jsonify({"message": "Película Eliminada Correctamente"})


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


@admin_bl.route("/movies", methods=["GET", "POST"])
def movies_view() -> str:
    movies = movie_services.get_movies()
    return render_template("movies_view.html", data=movies)


@admin_bl.route("/update_movie/<movie_data>", methods=["GET"])
def update_movie(movie_data) -> str:
    return render_template("update_movie.html", data=movie_data)


@admin_bl.route("/upload_movie", methods=["GET", "POST"])
def upload_movie() -> str:
    if request.method == "POST":
        movie_file: FileStorage = request.files.get("video_url")
        thumb_file: FileStorage = request.files.get("thumbnail_url")
        genres = request.form.getlist("genre")
        franchises = request.form.getlist("franchise")
        generic_name = uuid4().__str__()

        video_format = select_format(movie_file.content_type)
        save_file(thumb_file, generic_name, THUMBNAIL_EXT, THUMBNAIL_DIR)
        save_file(movie_file, generic_name, video_format, MOVIES_DIR)

        data = request.form.to_dict()
        data.update({"thumbnail_url": f"{generic_name}.{THUMBNAIL_EXT}"})
        data.update({"video_url": f"{generic_name}.{video_format}"})

        movie_services.create_movie(data, genres, franchises)

    genres = genre_service.get_genres()
    franchises = franchise_service.get_franchises()
    return render_template(
        "upload_movie.html",
        data={"genres": genres, "franchises": franchises}
    )


@admin_bl.route("/user_list", methods=["GET", "POST"])
def users_view() -> str:
    return render_template("users_view.html")


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
def get_admin(admin_id) -> dict:
    return admin.get_admin(admin_id)


@admin_bl.route("/", methods=["POST"])
def create_admin() -> Response:
    data = request.get_json()

    if "admin" not in data or "auth" not in data:
        raise DataValidationError("Don't found admin key or auth key")

    result = admin.create_admin(data["admin"], data["auth"])
    return jsonify(result)


@admin_bl.route("/<uuid:admin_id>", methods=["PUT"])
def update_admin(admin_id) -> Response:
    data = admin.update_admin(admin_id, **request.get_json())
    return jsonify(data)


@admin_bl.route("/<uuid:admin_id>", methods=["DELETE"])
def delete_admin(admin_id) -> Response:
    data = admin.delete_admin(admin_id)
    return jsonify(data)
