
from pathlib import Path
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

# Person 1's centralized configuration and logging
from core.config import settings
from core.logger import api_logger
from core.exceptions import (
    ResumeOptimizerException,
    ResumeParserError,
    InvalidFileTypeError,
    FileTooLargeError,
)


router = APIRouter(
    prefix="/api",
    tags=["Matching"],
)


# --------------------------------------------------
# UPLOAD CONFIGURATION
# --------------------------------------------------

UPLOAD_DIRECTORY = settings.UPLOAD_PATH

MAX_FILE_SIZE = settings.MAX_FILE_SIZE_BYTES

ALLOWED_EXTENSIONS = settings.ALLOWED_EXTENSIONS_LIST


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

    # The current frontend supports PDF and DOCX.
    allowed_upload_types = (".pdf", ".docx")

    if (
        extension not in allowed_upload_types
        or extension not in ALLOWED_EXTENSIONS
    ):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported.",
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
    # CREATE UNIQUE TEMPORARY FILE
    # --------------------------------------------------

    temporary_filename = f"{uuid.uuid4().hex}{extension}"

    file_path = UPLOAD_DIRECTORY / temporary_filename

    try:

        # --------------------------------------------------
        # STEP 1: SAVE UPLOAD WITH SIZE LIMIT
        # --------------------------------------------------

        total_size = 0

        with file_path.open("wb") as buffer:

            while chunk := await file.read(1024 * 1024):

                total_size += len(chunk)

                if total_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail=(
                            f"Resume exceeds the maximum "
                            f"file size of "
                            f"{settings.MAX_FILE_SIZE_MB} MB."
                        ),
                    )

                buffer.write(chunk)

        if total_size == 0:
            raise HTTPException(
                status_code=400,
                detail="The uploaded resume is empty.",
            )

        api_logger.info(
            "Resume uploaded for analysis"
        )

        # --------------------------------------------------
        # STEP 2: EXTRACT RESUME TEXT
        # --------------------------------------------------

        resume_text = extract_resume_text(
            str(file_path)
        )

        if not resume_text.strip():
            raise HTTPException(
                status_code=422,
                detail=(
                    "No readable text was found in the "
                    "resume. Please upload another file."
                ),
            )

        # --------------------------------------------------
        # STEP 3: AI RESUME MATCHING
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
        # STEP 6: PREPARE DASHBOARD LABEL
        # --------------------------------------------------

        job_label = next(
            (
                line.strip()
                for line in job_description.splitlines()
                if line.strip()
            ),
            "Job Description",
        )

        job_label = job_label[:120]

        # --------------------------------------------------
        # STEP 7: SAVE ANALYSIS
        # --------------------------------------------------

        save_analysis(
            filename=file.filename,
            job_label=job_label,
            match_score=match_result["score"],
            matched_skills=matched_skills,
            missing_skills=missing_skills,
        )

        api_logger.info(
            "Resume analysis completed successfully"
        )

        # --------------------------------------------------
        # STEP 8: RETURN RESULTS TO FRONTEND
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
    # FASTAPI VALIDATION ERRORS
    # --------------------------------------------------

    except HTTPException:
        raise

    # --------------------------------------------------
    # PERSON 1'S AI EXCEPTIONS
    # --------------------------------------------------

    except (
        InvalidFileTypeError,
        FileTooLargeError,
        ResumeParserError,
    ) as error:

        api_logger.warning(
            "Resume validation or parsing failed: %s",
            type(error).__name__,
        )

        raise HTTPException(
            status_code=error.status_code,
            detail=error.message,
        ) from error

    except ResumeOptimizerException as error:

        api_logger.exception(
            "AI processing failed"
        )

        raise HTTPException(
            status_code=error.status_code,
            detail="Unable to process the resume at this time.",
        ) from error

    # --------------------------------------------------
    # UNEXPECTED SERVER ERRORS
    # --------------------------------------------------

    except Exception as error:

        api_logger.exception(
            "Unexpected resume analysis error"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to analyze the resume. "
                "Please try again."
            ),
        ) from error

    # --------------------------------------------------
    # CLEAN UP TEMPORARY FILES
    # --------------------------------------------------

    finally:

        try:
            if file_path.exists():
                file_path.unlink()

        except OSError:
            api_logger.exception(
                "Failed to delete temporary resume"
            )

        await file.close()
