# models.py
# This defines the "leads" table in Postgres using SQLAlchemy.
# Each class attribute here = one column in the table.

from sqlalchemy import Column, Integer, String
from database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    company = Column(String, nullable=True)
    status = Column(String, default="new")  # new -> contacted -> won / lost
