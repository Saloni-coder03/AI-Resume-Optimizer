
# backend/api/models/response_models.py

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


# --------------------------------------------------
# AI RESUME MATCHING RESPONSE
# --------------------------------------------------

class MatchResponse(BaseModel):
    match_score: float

    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)

    recommendations: List[str] = Field(default_factory=list)
    roadmap: List[str] = Field(default_factory=list)

    resume_skills: List[str] = Field(default_factory=list)
    job_skills: List[str] = Field(default_factory=list)


# --------------------------------------------------
# DASHBOARD STATISTICS RESPONSE
# --------------------------------------------------

class DashboardStats(BaseModel):
    total_analyses: int = 0
    average_score: float = 0.0
    best_score: float = 0.0


# --------------------------------------------------
# DASHBOARD HISTORY ITEM RESPONSE
# --------------------------------------------------

class HistoryItem(BaseModel):
    id: int

    filename: str
    job_label: str

    match_score: float

    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)

    created_at: datetime
