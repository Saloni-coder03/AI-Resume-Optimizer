# backend/database/db_queries.py
import uuid
import datetime
from sqlalchemy.orm import Session

from core.logger import db_logger
from core.exceptions import DatabaseOperationError
from database.db_models import Resume, MatchResult


def save_resume(
    db: Session,
    resume_id: str,
    filename: str,
    raw_text: str,
    skills: list,
    education: list,
    years_experience: int,
    word_count: int,
    contact: dict
) -> Resume:
    try:
        resume = Resume(
            id=resume_id,
            filename=filename,
            raw_text=raw_text,
            skills=skills,
            education=education,
            years_experience=years_experience,
            word_count=word_count,
            contact=contact
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
        db_logger.info(f"Resume saved: {resume_id}")
        return resume
    except Exception as e:
        db.rollback()
        db_logger.error(f"Failed to save resume: {e}")
        raise DatabaseOperationError(f"Resume save failed: {e}") from e


def get_resume(db: Session, resume_id: str) -> Resume | None:
    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if resume:
            db_logger.debug(f"Resume found: {resume_id}")
        else:
            db_logger.warning(f"Resume not found: {resume_id}")
        return resume
    except Exception as e:
        db_logger.error(f"Failed to get resume: {e}")
        raise DatabaseOperationError(f"Resume fetch failed: {e}") from e


def save_match_result(
    db: Session,
    resume_id: str,
    job_title: str,
    company: str,
    scores: dict,
    matched_skills: list,
    missing_skills: list,
    recommendations: list,
    roadmap: list
) -> MatchResult:
    try:
        result = MatchResult(
            id=str(uuid.uuid4()),
            resume_id=resume_id,
            job_title=job_title,
            company=company,
            overall_score=scores.get("overall", 0.0),
            skills_score=scores.get("skills_match", 0.0),
            experience_score=scores.get("experience_match", 0.0),
            education_score=scores.get("education_match", 0.0),
            ats_score=scores.get("ats_score", 0.0),
            final_score=scores.get("final_score", 0.0),
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            recommendations=recommendations,
            roadmap=roadmap
        )
        db.add(result)
        db.commit()
        db.refresh(result)
        db_logger.info(
            f"Match saved: {result.id} | "
            f"Score: {result.final_score}%"
        )
        return result
    except Exception as e:
        db.rollback()
        db_logger.error(f"Failed to save match: {e}")
        raise DatabaseOperationError(f"Match save failed: {e}") from e


def get_match_history(
    db: Session,
    resume_id: str = None,
    limit: int = 10
) -> list[MatchResult]:
    try:
        query = db.query(MatchResult)
        if resume_id:
            query = query.filter(MatchResult.resume_id == resume_id)
        results = (
            query
            .order_by(MatchResult.created_at.desc())
            .limit(limit)
            .all()
        )
        db_logger.debug(f"Fetched {len(results)} match results")
        return results
    except Exception as e:
        db_logger.error(f"Failed to get history: {e}")
        raise DatabaseOperationError(f"History fetch failed: {e}") from e


def get_best_score(db: Session, resume_id: str = None) -> float:
    try:
        query = db.query(MatchResult.final_score)
        if resume_id:
            query = query.filter(MatchResult.resume_id == resume_id)
        best = query.order_by(MatchResult.final_score.desc()).first()
        score = best[0] if best else 0.0
        db_logger.debug(f"Best score: {score}%")
        return score
    except Exception as e:
        db_logger.error(f"Failed to get best score: {e}")
        return 0.0