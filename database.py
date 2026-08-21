# database.py
# This file sets up the connection to Postgres.
# Everything else in the app imports "Base" and "get_db" from here.

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# We read the DB connection string from an environment variable, so the
# SAME code works whether Postgres is running on your laptop, inside
# Docker, or on Render later. This is a very common real-world pattern.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://leadtrack:leadtrack@localhost:5432/leadtrack",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    FastAPI calls this for every request that needs the database.
    It hands over one connection ('session'), and closes it afterwards
    even if something goes wrong. This pattern is called a 'dependency'.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
