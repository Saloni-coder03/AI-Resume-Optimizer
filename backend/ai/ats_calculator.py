# backend/ai/ats_calculator.py
import re
from core.config import settings
from core.logger import ai_logger


class ATSCalculator:

    def calculate(self, resume_text: str, job_text: str) -> float:
        ai_logger.debug("Calculating ATS score")
        score = 0.0

        # 1. Keyword density (40 points)
        job_words = set(job_text.lower().split())
        resume_words = set(resume_text.lower().split())
        stopwords = {
            "the", "a", "an", "and", "or", "but", "in",
            "on", "at", "to", "for", "of", "with", "is",
            "are", "was", "were", "be", "been", "this",
            "that", "we", "our", "you", "your", "will"
        }
        keywords = job_words - stopwords
        if keywords:
            matches = len(resume_words & keywords)
            score += min(40, matches * 2)

        # 2. Resume length (20 points)
        wc = len(resume_text.split())
        if settings.ATS_MIN_WORD_COUNT <= wc <= settings.ATS_MAX_WORD_COUNT:
            score += 20
        elif 200 <= wc < settings.ATS_MIN_WORD_COUNT:
            score += 10
        elif wc > settings.ATS_MAX_WORD_COUNT:
            score += 15

        # 3. Section headers (20 points)
        sections = ["experience", "education", "skills", "projects", "summary"]
        for s in sections:
            if s in resume_text.lower():
                score += 4

        # 4. Contact info (10 points)
        if "@" in resume_text:
            score += 5
        if re.search(r"\d{10}", re.sub(r"\D", "", resume_text)):
            score += 5

        # 5. Quantified achievements (10 points)
        numbers = re.findall(r"\d+%|\$\d+|\d+\s*years?", resume_text)
        if len(numbers) >= settings.ATS_MIN_NUMBERS:
            score += 10
        elif len(numbers) >= 1:
            score += 5

        final = min(100.0, round(score, 2))
        ai_logger.info(f"ATS score: {final}")
        return final