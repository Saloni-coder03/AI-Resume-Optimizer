
from pathlib import Path
import shutil
import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException,
)

from api.models.response_models import MatchResponse

from ai.resume_parser import extract_resume_text
from ai.matcher import compare_resume_to_job
from ai.recommendations import (
    generate_recommendations,
    generate_learning_roadmap,
)

from database.db_queries import save_analysis
from core.logger import api_logger


router = APIRouter(
    prefix="/api",
    tags=["Matching"],
)


# --------------------------------------------------
# TEMPORARY UPLOAD DIRECTORY
# --------------------------------------------------

UPLOAD_DIRECTORY = Path(__file__).resolve().parents[2] / "uploads"

UPLOAD_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


# --------------------------------------------------
# MATCH RESUME WITH JOB DESCRIPTION
# --------------------------------------------------

@router.post(
    "/match",
    response_model=MatchResponse,
)
async def match_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
):

    # --------------------------------------------------
    # VALIDATE FILE
    # --------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please upload a resume.",
        )

    extension = Path(file.filename).suffix.lower()

    allowed_extensions = [
        ".pdf",
        ".docx",
    ]

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=(
                "Only PDF and DOCX files "
                "are supported."
            ),
        )

    # --------------------------------------------------
    # VALIDATE JOB DESCRIPTION
    # --------------------------------------------------

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty.",
        )

    # --------------------------------------------------
    # CREATE TEMPORARY FILE
    # --------------------------------------------------

    temporary_filename = f"{uuid.uuid4()}{extension}"

    file_path = UPLOAD_DIRECTORY / temporary_filename

    try:

        # --------------------------------------------------
        # STEP 1: SAVE RESUME TEMPORARILY
        # --------------------------------------------------

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        # --------------------------------------------------
        # STEP 2: EXTRACT RESUME TEXT
        # --------------------------------------------------

        resume_text = extract_resume_text(
            str(file_path)
        )

        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text was found "
                    "in the resume. Please try "
                    "another PDF or DOCX file."
                ),
            )

        # --------------------------------------------------
        # STEP 3: COMPARE RESUME WITH JOB
        # --------------------------------------------------

        match_result = compare_resume_to_job(
            resume_text,
            job_description,
        )

        matched_skills = match_result["matched_skills"]
        missing_skills = match_result["missing_skills"]

        # --------------------------------------------------
        # STEP 4: GENERATE RECOMMENDATIONS
        # --------------------------------------------------

        recommendations = generate_recommendations(
            matched_skills,
            missing_skills,
        )

        # --------------------------------------------------
        # STEP 5: GENERATE LEARNING ROADMAP
        # --------------------------------------------------

        roadmap = generate_learning_roadmap(
            missing_skills
        )

        # --------------------------------------------------
        # STEP 6: CREATE JOB LABEL FOR HISTORY
        # --------------------------------------------------

        job_label = next(
            (
                line.strip()
                for line in job_description.splitlines()
                if line.strip()
            ),
            "Job Description",
        )

        # Keep dashboard label short
        job_label = job_label[:120]

        # --------------------------------------------------
        # STEP 7: SAVE ANALYSIS TO DATABASE
        # --------------------------------------------------

        save_analysis(
            filename=file.filename,
            job_label=job_label,
            match_score=match_result["score"],
            matched_skills=matched_skills,
            missing_skills=missing_skills,
        )

        # --------------------------------------------------
        # STEP 8: RETURN RESULTS TO REACT
        # --------------------------------------------------

        return MatchResponse(
            match_score=match_result["score"],
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            recommendations=recommendations,
            roadmap=roadmap,
            resume_skills=match_result["resume_skills"],
            job_skills=match_result["job_skills"],
        )

    # --------------------------------------------------
    # HANDLE VALIDATION ERRORS
    # --------------------------------------------------

    except HTTPException:
        raise

    # --------------------------------------------------
    # HANDLE UNEXPECTED ERRORS WITH CENTRAL LOGGING
    # --------------------------------------------------

    except Exception:
        api_logger.exception(
            "Resume analysis failed"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to analyze the resume. "
                "Please try again."
            ),
        ) from None

    # --------------------------------------------------
    # ALWAYS DELETE TEMPORARY RESUME
    # --------------------------------------------------

    finally:
        try:
            if file_path.exists():
                file_path.unlink()
        except OSError:
            api_logger.exception(
                "Failed to delete temporary resume file"
            )

        await file.close()
