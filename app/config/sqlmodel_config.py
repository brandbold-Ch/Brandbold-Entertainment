from sqlmodel import create_engine, SQLModel
from app.models.user_model import User
from app.models.watch_history_model import WatchHistory
engine = create_engine("postgresql://postgres:mypostgres@localhost:5432/postgres", echo=True)
SQLModel.metadata.create_all(engine)
