import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field


# --------------------------------
# Load environment variables
# --------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT_DIR / ".env"

load_dotenv(ENV_FILE)


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite",
)


if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. "
        "Add it to the root .env file."
    )


# --------------------------------
# Gemini model
# --------------------------------

llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    api_key=GEMINI_API_KEY,
    max_retries=2,
)


# --------------------------------
# Structured output models
# --------------------------------

class ExtractedLead(BaseModel):
    name: str = Field(
        description="Prospect's full name, or empty string if unknown"
    )

    email: str = Field(
        description="Prospect's email, or empty string if unknown"
    )

    company: str = Field(
        description="Prospect's company, or empty string if unknown"
    )

    notes_summary: str = Field(
        description="One-sentence summary of the raw notes"
    )


class LeadQualification(BaseModel):
    priority: Literal["high", "medium", "low"] = Field(
        description="How urgently the sales team should follow up"
    )

    reason: str = Field(
        description="One-sentence reason for the priority"
    )


# --------------------------------
# CHAIN 1: Extract lead data
# --------------------------------

extraction_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You extract sales lead information for a CRM. "
            "Never invent missing personal information. "
            "Use an empty string when name, email, or company is not present.",
        ),
        (
            "human",
            "Extract the lead information from these raw notes:\n\n{raw_text}",
        ),
    ]
)


extraction_model = llm.with_structured_output(
    schema=ExtractedLead.model_json_schema(),
    method="json_schema",
)


extraction_chain = (
    extraction_prompt
    | extraction_model
)


# --------------------------------
# CHAIN 2: Qualify lead
# --------------------------------

qualification_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a sales operations assistant. "
            "Choose high, medium, or low follow-up priority "
            "based only on the lead summary.",
        ),
        (
            "human",
            "Name: {name}\n"
            "Company: {company}\n"
            "Notes: {notes_summary}\n\n"
            "Decide the follow-up priority and give one short reason.",
        ),
    ]
)


qualification_model = llm.with_structured_output(
    schema=LeadQualification.model_json_schema(),
    method="json_schema",
)


qualification_chain = (
    qualification_prompt
    | qualification_model
)


# --------------------------------
# Functions used by FastAPI
# --------------------------------

def extract_lead(raw_text: str) -> dict:
    """
    Step 1:
    Raw text -> structured lead information.
    """

    result = extraction_chain.invoke(
        {
            "raw_text": raw_text,
        }
    )

    return ExtractedLead.model_validate(
        result
    ).model_dump()


def qualify_lead(
    name: str,
    company: str,
    notes_summary: str,
) -> dict:
    """
    Step 2:
    Extracted lead -> qualification priority.
    """

    result = qualification_chain.invoke(
        {
            "name": name,
            "company": company,
            "notes_summary": notes_summary,
        }
    )

    return LeadQualification.model_validate(
        result
    ).model_dump()