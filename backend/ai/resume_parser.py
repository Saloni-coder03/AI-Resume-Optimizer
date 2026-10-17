# backend/ai/resume_parser.py
import re
from pathlib import Path
from pdfminer.high_level import extract_text as extract_pdf_text
import docx2txt

from core.config import settings
from core.logger import ai_logger
from core.exceptions import (
    ResumeParserError,
    InvalidFileTypeError,
    FileTooLargeError
)


class ResumeParser:

    def __init__(self):
        self.allowed_extensions = settings.ALLOWED_EXTENSIONS_LIST
        self.max_size_bytes = settings.MAX_FILE_SIZE_BYTES

    def parse(self, file_path: str | Path) -> str:
        path = Path(file_path).resolve()
        ai_logger.info(f"Parsing resume: {path.name}")

        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"File not found: {path}")

        ext = path.suffix.lower()
        if ext not in self.allowed_extensions:
            raise InvalidFileTypeError(file_extension=ext)

        file_size = path.stat().st_size
        if file_size > self.max_size_bytes:
            raise FileTooLargeError(
                file_size_bytes=file_size,
                max_mb=settings.MAX_FILE_SIZE_MB
            )

        try:
            if ext == ".pdf":
                raw = self._extract_pdf(path)
            elif ext in [".docx", ".doc"]:
                raw = self._extract_docx(path)
            else:
                raise InvalidFileTypeError(file_extension=ext)
        except (InvalidFileTypeError, FileTooLargeError, FileNotFoundError):
            raise
        except Exception as e:
            ai_logger.error(f"Extraction failed: {e}")
            raise ResumeParserError(str(e)) from e

        cleaned = self._sanitize(raw)
        ai_logger.info(f"Parsed {path.name}: {len(cleaned.split())} words")
        return cleaned

    def _extract_pdf(self, path: Path) -> str:
        text = extract_pdf_text(str(path))
        if not text or not text.strip():
            raise ResumeParserError("No text found in PDF.")
        return text

    def _extract_docx(self, path: Path) -> str:
        text = docx2txt.process(str(path))
        if not text or not text.strip():
            raise ResumeParserError("No text found in Word file.")
        return text

    @staticmethod
    def _sanitize(text: str) -> str:
        if not text:
            return ""
        text = text.replace("\x00", " ")
        text = re.sub(r"[\x01-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]", " ", text)
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
        return "\n".join(line for line in lines if line)


# Wrapper function for friend's match_routes.py compatibility
def extract_resume_text(file_path: str) -> str:
    parser = ResumeParser()
    return parser.parse(file_path)