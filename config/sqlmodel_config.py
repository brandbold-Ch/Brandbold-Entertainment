from sqlmodel import create_engine, SQLModel, Session
from models.user_model import User
from models.admin_model import Admin
from models.movie_model import Movie
from models.genre_model import Genres
from models.device_model import Device
from models.watch_history_model import WatchHistory
from models.auth_model import Auth, Roles

engine = create_engine("postgresql://postgres:mypostgres@localhost:5432/postgres", echo=True)
SQLModel.metadata.create_all(engine)

"""admin = Admin(first_name="Brandon Jared", last_name="Molina Vazquez")
auth = Auth(admin_id=admin.id, username="@brandbold", email="jaredbrandon970@gmail.com",
            password="qwerty", role=Roles.ADMIN)

with Session(engine) as session:
    session.add(admin)
    session.add(auth)
    session.commit()"""
