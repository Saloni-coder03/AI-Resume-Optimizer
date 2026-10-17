
# backend/ai/ats_calculator.py

import re

from core.config import settings
from core.logger import ai_logger


class ATSCalculator:
    """
    Estimates resume quality using five components.

    Keyword coverage:       40 points
    Resume length:          20 points
    Section headings:       20 points
    Contact information:    10 points
    Quantified achievements:10 points

    Total: 100 points
    """

    STOPWORDS = {
        "the", "a", "an", "and", "or", "but", "in",
        "on", "at", "to", "for", "of", "with", "is",
        "are", "was", "were", "be", "been", "this",
        "that", "we", "our", "you", "your", "will",
        "have", "has", "had", "as", "by", "from",
        "it", "its", "their", "who", "which", "must",
        "should", "can", "able", "looking", "seeking",
        "required", "preferred", "candidate",
        "candidates", "position", "role", "work",
        "job", "team", "strong", "good"
    }

    # --------------------------------------------------
    # NORMALIZE TEXT INTO KEYWORDS
    # --------------------------------------------------

    @staticmethod
    def tokenize(text: str) -> set[str]:

        text = text.lower()

        words = re.findall(
            r"[a-z0-9]+(?:[.+#][a-z0-9]+)*(?:\+\+|#)?",
            text,
        )

        return set(words)

    # --------------------------------------------------
    # KEYWORD COVERAGE - 40 POINTS
    # --------------------------------------------------

    def keyword_score(
        self,
        resume_text: str,
        job_text: str,
    ) -> float:

        resume_words = self.tokenize(resume_text)

        job_words = self.tokenize(job_text)

        keywords = {
            word
            for word in job_words
            if word not in self.STOPWORDS
            and len(word) > 1
        }

        if not keywords:
            return 0.0

        matched_keywords = (
            keywords.intersection(resume_words)
        )

        coverage = (
            len(matched_keywords) / len(keywords)
        )

        return round(coverage * 40, 2)

    # --------------------------------------------------
    # RESUME LENGTH - 20 POINTS
    # --------------------------------------------------

    @staticmethod
    def resume_length_score(
        resume_text: str,
    ) -> float:

        word_count = len(resume_text.split())

        if (
            settings.ATS_MIN_WORD_COUNT
            <= word_count
            <= settings.ATS_MAX_WORD_COUNT
        ):
            return 20.0

        if 200 <= word_count < settings.ATS_MIN_WORD_COUNT:
            return 10.0

        if word_count > settings.ATS_MAX_WORD_COUNT:
            return 15.0

        return 0.0

    # --------------------------------------------------
    # SECTION HEADINGS - 20 POINTS
    # --------------------------------------------------

    @staticmethod
    def section_score(resume_text: str) -> float:

        headings = {
            "experience": r"(?:work|professional|employment)?\s*experience",
            "education": r"education|academic background",
            "skills": r"(?:technical|core|professional)?\s*skills",
            "projects": r"projects?|personal projects",
            "summary": r"(?:professional )?summary|profile|objective",
        }

        score = 0.0

        for pattern in headings.values():

            if re.search(
                rf"(?im)^\s*(?:{pattern})\s*:?\s*$",
                resume_text,
            ):
                score += 4.0

        return score

    # --------------------------------------------------
    # CONTACT INFORMATION - 10 POINTS
    # --------------------------------------------------

    @staticmethod
    def contact_score(resume_text: str) -> float:

        score = 0.0

        email_pattern = (
            r"\b[A-Za-z0-9._%+-]+@"
            r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        )

        if re.search(email_pattern, resume_text):
            score += 5.0

        phone_pattern = (
            r"(?<!\d)(?:\+?\d{1,3}[\s.-]?)?"
            r"(?:\(?\d{3}\)?[\s.-]?)?"
            r"\d{3}[\s.-]?\d{4}(?!\d)"
        )

        if re.search(phone_pattern, resume_text):
            score += 5.0

        return score

    # --------------------------------------------------
    # QUANTIFIED ACHIEVEMENTS - 10 POINTS
    # --------------------------------------------------

    @staticmethod
    def achievement_score(
        resume_text: str,
    ) -> float:

        patterns = [
            r"\b\d+(?:\.\d+)?\s*%",
            r"\$\s*\d[\d,]*(?:\.\d+)?\s*[kKmMbB]?",
            (
                r"\b\d+(?:\.\d+)?\s*[kKmMbB]?\s*"
                r"(?:users|clients|customers|requests|"
                r"transactions|sales|downloads)\b"
            ),
        ]

        matches = set()

        for pattern in patterns:

            for match in re.finditer(
                pattern,
                resume_text,
                re.IGNORECASE,
            ):
                matches.add(
                    (match.start(), match.end())
                )

        count = len(matches)

        if count >= settings.ATS_MIN_NUMBERS:
            return 10.0

        if count >= 1:
            return 5.0

        return 0.0

    # --------------------------------------------------
    # CALCULATE FINAL ATS SCORE
    # --------------------------------------------------

    def calculate(
        self,
        resume_text: str,
        job_text: str,
    ) -> float:

        ai_logger.debug("Calculating ATS score")

        keyword_points = self.keyword_score(
            resume_text,
            job_text,
        )

        length_points = self.resume_length_score(
            resume_text
        )

        section_points = self.section_score(
            resume_text
        )

        contact_points = self.contact_score(
            resume_text
        )

        achievement_points = self.achievement_score(
            resume_text
        )

        total_score = (
            keyword_points
            + length_points
            + section_points
            + contact_points
            + achievement_points
        )

        final_score = round(
            max(0.0, min(100.0, total_score)),
            2,
        )

        ai_logger.info(
            "ATS score calculated: %.2f",
            final_score,
        )

        return final_score
