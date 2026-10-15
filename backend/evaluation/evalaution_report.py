# backend/evaluation/evaluation_report.py
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from core.logger import ai_logger
from evaluation.evaluate_parser import evaluate_parser
from evaluation.evaluate_matcher import evaluate_matcher


def generate_report():
    ai_logger.info("=" * 60)
    ai_logger.info("GENERATING FULL EVALUATION REPORT")
    ai_logger.info("=" * 60)

    # Run parser evaluation
    parser_results = evaluate_parser()

    # Run matcher evaluation
    matcher_results = evaluate_matcher()

    # Summary
    ai_logger.info("")
    ai_logger.info("=" * 60)
    ai_logger.info("FINAL REPORT SUMMARY")
    ai_logger.info("=" * 60)

    parser_pass = sum(1 for r in parser_results if r.get("status") != "FAIL")
    parser_total = len(parser_results)

    matcher_pass = sum(1 for r in matcher_results if r.get("status") == "PASS")
    matcher_total = sum(1 for r in matcher_results if r.get("status") in ["PASS", "FAIL"])

    ai_logger.info(f"Parser:  {parser_pass}/{parser_total} files parsed successfully")
    ai_logger.info(f"Matcher: {matcher_pass}/{matcher_total} test cases passed")

    if parser_total > 0 and matcher_total > 0:
        overall = round((parser_pass + matcher_pass) / (parser_total + matcher_total) * 100, 1)
        ai_logger.info(f"Overall: {overall}% success rate")

    ai_logger.info("=" * 60)
    ai_logger.info("EVALUATION COMPLETE")
    ai_logger.info("=" * 60)


if __name__ == "__main__":
    generate_report()