from sqlmodel import create_engine, SQLModel
from sqlalchemy.schema import CreateTable
from app.models.user_model import User
from app.models.auth_model import Auth
from app.models.watch_history_model import WatchHistory


engine = create_engine("postgresql://postgres:mypostgres@localhost:5432/postgres", echo=False)
SQLModel.metadata.create_all(engine)

"""for table in SQLModel.metadata.tables.values():
    print(str(CreateTable(table).compile(engine)))"""