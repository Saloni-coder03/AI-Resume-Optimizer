from pydantic import BaseModel
from typing import List


class MatchResponse(BaseModel):
    match_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    recommendations: List[str]
    roadmap: List[str]
    resume_skills: List[str]
    job_skills: List[str]