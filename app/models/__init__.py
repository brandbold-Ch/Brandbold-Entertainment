from app.models.admin_model import Admin
from app.models.auth_model import Auth
from app.models.base_user_model import BaseUser
from app.models.device_model import Device
from app.models.genre_model import Genre, Genres
from app.models.movie_model import Movie
from app.models.user_model import User
from app.models.watch_history_model import WatchHistory
from app.models.movie_genre_model import MovieGenre
from app.models.movie_franchise_model import MovieFranchise
from app.models.franchise_model import Franchise

__all__ = [
    "Admin",
    "Auth",
    "BaseUser",
    "Device",
    "Genre",
    "Movie",
    "User",
    "WatchHistory",
    "Genres",
    "MovieGenre",
    "MovieFranchise",
    "Franchise"
]
