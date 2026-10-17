# backend/evaluation/evaluate_matcher.py
import sys
import json
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from core.config import BASE_DIR
from core.logger import ai_logger
from ai.resume_parser import ResumeParser
from ai.matcher import BERTMatcher

EVAL_DIR = BASE_DIR / "backend" / "data" / "evaluation"


def evaluate_matcher():
    ai_logger.info("=" * 50)
    ai_logger.info("STARTING MATCHER EVALUATION")
    ai_logger.info("=" * 50)

    expected_path = EVAL_DIR / "expected_results.json"
    if not expected_path.exists():
        ai_logger.error("expected_results.json not found. Create it first.")
        return []

    with open(expected_path, "r", encoding="utf-8") as f:
        test_cases = json.load(f)["test_cases"]

    parser = ResumeParser()
    matcher = BERTMatcher()

    results = []
    passed = 0
    failed = 0

    for case in test_cases:
        ai_logger.info(f"Testing: {case['name']}")

        resume_path = EVAL_DIR / case["resume_file"]
        job_path = EVAL_DIR / case["job_file"]

        if not resume_path.exists():
            ai_logger.warning(f"  SKIP | Resume not found: {resume_path.name}")
            results.append({
                "test": case["name"],
                "status": "SKIP",
                "reason": "Resume file missing"
            })
            continue

        if not job_path.exists():
            ai_logger.warning(f"  SKIP | Job not found: {job_path.name}")
            results.append({
                "test": case["name"],
                "status": "SKIP",
                "reason": "Job file missing"
            })
            continue

        try:
            resume_text = parser.parse(str(resume_path))

            with open(job_path, "r", encoding="utf-8") as f:
                job_text = f.read()

            analysis = matcher.full_analysis(resume_text, job_text)
            actual_score = analysis["final_score"]

            is_pass = case["expected_min"] <= actual_score <= case["expected_max"]

            if is_pass:
                passed += 1
                status = "PASS"
            else:
                failed += 1
                status = "FAIL"

            result = {
                "test": case["name"],
                "status": status,
                "expected": f"{case['expected_min']}-{case['expected_max']}%",
                "actual": f"{actual_score}%",
                "reason": case["reason"]
            }
            results.append(result)

            ai_logger.info(
                f"  {status} | Expected: {result['expected']} | "
                f"Got: {actual_score}%"
            )

        except Exception as e:
            failed += 1
            results.append({
                "test": case["name"],
                "status": "ERROR",
                "error": str(e)
            })
            ai_logger.error(f"  ERROR | {e}")

    total = passed + failed
    ai_logger.info(f"Matcher Evaluation: {passed}/{total} passed")
    ai_logger.info("=" * 50)

    return results


if __name__ == "__main__":
    evaluate_matcher()