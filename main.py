# main.py
# This is the FastAPI app itself. Run it with:
#   uvicorn main:app --reload
# Then open http://localhost:8000/docs to see and test it interactively.

import socket
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import Base, engine, get_db

# Creates the "leads" table in Postgres if it doesn't exist yet.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LeadTrack API")


@app.get("/health")
def health():
    """
    Returns which container answered the request. Once you run two
    copies of this app behind Nginx (Day 2), hitting this endpoint
    repeatedly will show the hostname alternating — that's the load
    balancer working.
    """
    return {"status": "ok", "instance": socket.gethostname()}


@app.post("/leads", response_model=schemas.LeadOut, status_code=201)
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):
    db_lead = models.Lead(**lead.model_dump())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead


@app.get("/leads", response_model=List[schemas.LeadOut])
def list_leads(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Lead)
    if status:
        query = query.filter(models.Lead.status == status)
    return query.all()


@app.get("/leads/{lead_id}", response_model=schemas.LeadOut)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@app.patch("/leads/{lead_id}", response_model=schemas.LeadOut)
def update_lead(
    lead_id: int, updates: schemas.LeadUpdate, db: Session = Depends(get_db)
):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(lead, field, value)
    db.commit()
    db.refresh(lead)
    return lead


@app.delete("/leads/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    db.delete(lead)
    db.commit()
    return {"deleted": lead_id}
