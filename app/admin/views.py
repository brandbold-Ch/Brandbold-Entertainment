from flask import Blueprint, render_template, request
from uuid import uuid4
from os import path
from sqlmodel import Session
from werkzeug.datastructures import FileStorage
from config.sqlmodel_config import engine
from services.movie_service import MovieService

admin_bl = Blueprint("admin", __name__,
                     url_prefix="/admin", template_folder="templates")
movie_services = MovieService(Session(engine))

RESOURCES_DIR = "../../../static"
THUMBNAIL_DIR = "thumbnail"
MOVIES_DIR = "movies"
THUMBNAIL_EXT = "webp"
MOVIE_EXT = "mkv"


def res_path(file: str, _type: str, _dir: str) -> str:
    filename = f"{RESOURCES_DIR}/{_dir}/{file}.{_type}"
    return path.abspath(path.join(__file__, filename))


@admin_bl.route("/", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")


@admin_bl.route("/movie_list", methods=["GET"])
def movie_list():
    movies = movie_services.get_movies()
    return render_template("movie_list.html", movies=movies)


@admin_bl.route("/upload_movie", methods=["GET", "POST"])
def upload_movie():
    if request.method == "POST":
        movie_file: FileStorage = request.files["video_url"]
        thumb_file: FileStorage = request.files["thumbnail_url"]
        filename = str(uuid4())

        thumbnail_path = res_path(filename, THUMBNAIL_EXT, THUMBNAIL_DIR)
        with open(thumbnail_path, "wb") as thumb:
            thumb.write(thumb_file.read())

        movie_path = res_path(filename, MOVIE_EXT, MOVIES_DIR)
        with open(movie_path, "wb") as movie:
            movie.write(movie_file.read())

        data = request.form.to_dict()
        data.update({"thumbnail_url": f"{filename}.{THUMBNAIL_EXT}"})
        data.update({"video_url": f"{filename}.{MOVIE_EXT}"})
        movie_services.add_movie(**data)

    return render_template("upload_movie.html")


@admin_bl.route("/user_list", methods=["GET", "POST"])
def user_list():
    return render_template("user_list.html")


@admin_bl.route("/video_streaming/<movie_path>", methods=["GET"])
def video_streaming(movie_path: str):
    return render_template("video_streaming.html", file=movie_path)
