# backend/database/db_models.py
import datetime
from sqlalchemy import Column, String, Float, Integer, JSON, DateTime, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    raw_text = Column(Text, nullable=True)
    skills = Column(JSON, default=list)
    education = Column(JSON, default=list)
    years_experience = Column(Integer, default=0)
    word_count = Column(Integer, default=0)
    contact = Column(JSON, default=dict)
    uploaded_at = Column(
        DateTime,
        default=datetime.datetime.utcnow
    )


class MatchResult(Base):
    __tablename__ = "match_results"

    id = Column(String, primary_key=True)
    resume_id = Column(String, nullable=False)
    job_title = Column(String, default="Unknown")
    company = Column(String, default="Unknown")
    overall_score = Column(Float, default=0.0)
    skills_score = Column(Float, default=0.0)
    experience_score = Column(Float, default=0.0)
    education_score = Column(Float, default=0.0)
    ats_score = Column(Float, default=0.0)
    final_score = Column(Float, default=0.0)
    matched_skills = Column(JSON, default=list)
    missing_skills = Column(JSON, default=list)
    recommendations = Column(JSON, default=list)
    roadmap = Column(JSON, default=list)
    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow
    )
    
# --------------------------------------------------
# DASHBOARD ANALYSIS HISTORY
# --------------------------------------------------

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    filename = Column(
        String,
        nullable=False,
    )

    job_label = Column(
        String,
        nullable=False,
    )

    match_score = Column(
        Float,
        nullable=False,
    )

    matched_skills = Column(
        JSON,
        nullable=False,
        default=list,
    )

    missing_skills = Column(
        JSON,
        nullable=False,
        default=list,
    )

    created_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        nullable=False,
    )
