# backend/evaluation/evaluate_parser.py
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from core.config import BASE_DIR
from core.logger import ai_logger
from ai.resume_parser import ResumeParser

EVAL_DIR = BASE_DIR / "backend" / "data" / "evaluation"


def evaluate_parser():
    ai_logger.info("=" * 50)
    ai_logger.info("STARTING PARSER EVALUATION")
    ai_logger.info("=" * 50)

    parser = ResumeParser()
    resume_dir = EVAL_DIR / "sample_resumes"

    if not resume_dir.exists():
        ai_logger.warning("No sample_resumes folder found. Skipping.")
        return []

    pdf_files = list(resume_dir.glob("*.pdf"))
    docx_files = list(resume_dir.glob("*.docx"))
    all_files = pdf_files + docx_files

    if not all_files:
        ai_logger.warning("No resume files found in sample_resumes/")
        return []

    results = []

    for file_path in all_files:
        ai_logger.info(f"Testing: {file_path.name}")

        try:
            text = parser.parse(str(file_path))
            word_count = len(text.split())
            has_email = "@" in text
            has_phone = any(c.isdigit() for c in text)

            status = "PASS" if word_count > 20 else "WARN"

            result = {
                "file": file_path.name,
                "status": status,
                "words": word_count,
                "has_email": has_email,
                "has_phone": has_phone
            }
            results.append(result)

            ai_logger.info(
                f"  {status} | Words: {word_count} | "
                f"Email: {has_email} | Phone: {has_phone}"
            )

        except Exception as e:
            result = {
                "file": file_path.name,
                "status": "FAIL",
                "error": str(e)
            }
            results.append(result)
            ai_logger.error(f"  FAIL | Error: {e}")

    passed = sum(1 for r in results if r["status"] != "FAIL")
    total = len(results)
    ai_logger.info(f"Parser Evaluation: {passed}/{total} passed")
    ai_logger.info("=" * 50)

    return results


if __name__ == "__main__":
    evaluate_parser()