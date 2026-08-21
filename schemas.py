# schemas.py
# These are NOT the database table. They define what shape of data the
# API accepts (requests) and returns (responses). FastAPI uses these to
# auto-validate incoming JSON and auto-generate the docs at /docs.

from typing import Optional
from pydantic import BaseModel, ConfigDict


class LeadCreate(BaseModel):
    name: str
    email: str
    company: Optional[str] = None
    status: Optional[str] = "new"


class LeadUpdate(BaseModel):
    # Every field optional, so a PATCH request can send just the one
    # field it wants to change (e.g. only "status").
    name: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None


class LeadOut(BaseModel):
    id: int
    name: str
    email: str
    company: Optional[str] = None
    status: str

    # This lets FastAPI build a LeadOut directly from a SQLAlchemy
    # Lead object (database row), not just from a plain dict.
    model_config = ConfigDict(from_attributes=True)
