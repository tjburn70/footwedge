from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

FOOTWEDGE_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/footwedge'
engine = create_engine(FOOTWEDGE_DATABASE_URI)
db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

Base = declarative_base()


# def init_db():
#     # import all modules here that might define models so that
#     # they will be registered properly on the metadata.  Otherwise
#     # you will have to import them first before calling init_db()
#     import models
#     Base.metadata.create_all(bind=engine)
