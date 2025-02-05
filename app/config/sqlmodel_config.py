from sqlmodel import create_engine, SQLModel

engine = create_engine("postgresql://postgres:mypostgres@localhost:5432/postgres", echo=True)
SQLModel.metadata.create_all(engine)
