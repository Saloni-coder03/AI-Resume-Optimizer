
# backend/api/routes/resume_routes.py

from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
)

from core.config import settings
from core.logger import api_logger


router = APIRouter(
    prefix="/api/resume",
    tags=["Resume"],
)


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    # Validate filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please select a resume.",
        )

    extension = Path(file.filename).suffix.lower()

    # Keep consistent with the matching endpoint
    allowed_types = {".pdf", ".docx"}

    if (
        extension not in allowed_types
        or extension not in settings.ALLOWED_EXTENSIONS_LIST
    ):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported.",
        )

    upload_dir = settings.UPLOAD_PATH

    # Never trust the submitted filename as a storage path
    stored_filename = f"{uuid4().hex}{extension}"
    file_path = upload_dir / stored_filename

    total_size = 0

    try:
        # Save in chunks to enforce the file-size limit
        with file_path.open("wb") as buffer:

            while True:
                chunk = await file.read(1024 * 1024)

                if not chunk:
                    break

                total_size += len(chunk)

                if total_size > settings.MAX_FILE_SIZE_BYTES:
                    raise HTTPException(
                        status_code=413,
                        detail=(
                            "Resume exceeds the maximum "
                            f"size of {settings.MAX_FILE_SIZE_MB} MB."
                        ),
                    )

                buffer.write(chunk)

        if total_size == 0:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty.",
            )

        api_logger.info(
            "Resume uploaded successfully: %s bytes",
            total_size,
        )

        return {
            "message": "Resume uploaded successfully",
            "filename": file.filename,
            "stored_filename": stored_filename,
        }

    except HTTPException:
        # Remove incomplete or rejected uploads
        file_path.unlink(missing_ok=True)
        raise

    except Exception as error:
        file_path.unlink(missing_ok=True)

        api_logger.exception(
            "Unexpected resume upload error"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to upload resume.",
        ) from error

    finally:
        await file.close()
