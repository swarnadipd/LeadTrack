# main.py
# This is the FastAPI app itself. Run it with:
#   uvicorn main:app --reload
# Then open http://localhost:8000/docs to see and test it interactively.

import socket
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
import schemas
from ai_pipeline import extract_lead, qualify_lead
from database import Base, engine, get_db

# Creates the "leads" table in Postgres if it doesn't exist yet.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LeadTrack API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.post("/leads/qualify", response_model=schemas.QualifiedLeadOut, status_code=201)
def qualify_and_create_lead(
    payload: schemas.RawLeadInput, db: Session = Depends(get_db)
):
    """
    The AI pipeline endpoint. Paste in raw notes about a prospect (an
    email, a call summary, anything unstructured) and this:
      1. Calls the LLM to extract structured fields from the text.
      2. Calls the LLM again — using step 1's output as input — to decide
         a follow-up priority.
      3. Creates the lead in the database using the extracted + qualified
         data.
    Step 2 depends on step 1's result, so this is a genuine two-step
    chain, not a single passthrough call to a model.
    """
    try:
        extracted = extract_lead(payload.raw_text)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"AI extraction step failed: {e}",
        )

    try:
        qualification = qualify_lead(
            name=extracted.get("name", ""),
            company=extracted.get("company", ""),
            notes_summary=extracted.get("notes_summary", ""),
        )
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"AI qualification step failed: {e}",
        )

    priority = qualification.get("priority", "medium")
    status = "contacted" if priority == "high" else "new"

    db_lead = models.Lead(
        name=extracted.get("name") or "Unknown",
        email=extracted.get("email") or "unknown@example.com",
        company=extracted.get("company"),
        status=status,
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)

    return schemas.QualifiedLeadOut(
        id=db_lead.id,
        name=db_lead.name,
        email=db_lead.email,
        company=db_lead.company,
        status=db_lead.status,
        ai_priority=priority,
        ai_reason=qualification.get("reason", ""),
        ai_notes_summary=extracted.get("notes_summary", ""),
    )
