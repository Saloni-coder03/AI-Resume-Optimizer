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


router = APIRouter(
    prefix="/api",
    tags=["Matching"],
)


# Folder used temporarily while processing resumes
UPLOAD_DIRECTORY = Path("uploads")

UPLOAD_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


@router.post(
    "/match",
    response_model=MatchResponse,
)
async def match_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
):

    # Check resume file
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please upload a resume.",
        )

    # Check file type
    extension = Path(
        file.filename
    ).suffix.lower()

    allowed_extensions = [
        ".pdf",
        ".docx",
    ]

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported.",
        )

    # Check job description
    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty.",
        )

    # Generate a unique temporary filename
    temporary_filename = (
        f"{uuid.uuid4()}{extension}"
    )

    file_path = (
        UPLOAD_DIRECTORY
        / temporary_filename
    )

    try:

        # Save uploaded resume temporarily
        with open(
            file_path,
            "wb",
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer,
            )

        # -----------------------------------
        # STEP 1: Extract resume text
        # -----------------------------------

        resume_text = extract_resume_text(
            str(file_path)
        )

        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text was found in the resume. "
                    "Please try another PDF or DOCX file."
                ),
            )

        # -----------------------------------
        # STEP 2: Compare resume with job
        # -----------------------------------

        match_result = compare_resume_to_job(
            resume_text,
            job_description,
        )

        matched_skills = (
            match_result["matched_skills"]
        )

        missing_skills = (
            match_result["missing_skills"]
        )

        # -----------------------------------
        # STEP 3: Generate recommendations
        # -----------------------------------

        recommendations = (
            generate_recommendations(
                matched_skills,
                missing_skills,
            )
        )

        # -----------------------------------
        # STEP 4: Generate learning roadmap
        # -----------------------------------

        roadmap = (
            generate_learning_roadmap(
                missing_skills
            )
        )

        # -----------------------------------
        # STEP 5: Send result to React
        # -----------------------------------

        return MatchResponse(

            match_score=match_result[
                "score"
            ],

            matched_skills=matched_skills,

            missing_skills=missing_skills,

            recommendations=recommendations,

            roadmap=roadmap,

            resume_skills=match_result[
                "resume_skills"
            ],

            job_skills=match_result[
                "job_skills"
            ],
        )

    except HTTPException:
        raise

    except Exception as error:

        print(
            "Resume analysis error:",
            error,
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to analyze the resume. "
                "Please try again."
            ),
        )

    finally:

        # Delete temporary resume
        if file_path.exists():
            file_path.unlink()

        await file.close()