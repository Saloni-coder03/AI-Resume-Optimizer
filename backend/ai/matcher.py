
# backend/ai/matcher.py

import re
from functools import lru_cache

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from core.config import settings
from core.logger import ai_logger
from core.exceptions import ModelLoadError, MatchingEngineError

from ai.section_extractor import SectionExtractor
from ai.ats_calculator import ATSCalculator


# --------------------------------------------------
# AI RESUME MATCHER
# --------------------------------------------------

class BERTMatcher:

    def __init__(self):
        ai_logger.info(
            "Loading BERT model: %s",
            settings.BERT_MODEL_NAME,
        )

        try:
            self.model = SentenceTransformer(
                settings.BERT_MODEL_NAME
            )

            ai_logger.info("BERT model loaded")

        except Exception as error:
            ai_logger.exception("BERT model loading failed")

            raise ModelLoadError(
                settings.BERT_MODEL_NAME
            ) from error

        self.extractor = SectionExtractor()
        self.ats = ATSCalculator()

    # --------------------------------------------------
    # SEMANTIC SIMILARITY
    # --------------------------------------------------

    def similarity(
        self,
        text1: str,
        text2: str,
    ) -> float:

        try:
            vector1 = self.model.encode(text1)
            vector2 = self.model.encode(text2)

            score = cosine_similarity(
                [vector1],
                [vector2],
            )[0][0]

            return round(
                max(0.0, min(100.0, float(score * 100))),
                2,
            )

        except Exception as error:
            ai_logger.exception(
                "Semantic similarity calculation failed"
            )

            raise MatchingEngineError(
                str(error)
            ) from error

    # --------------------------------------------------
    # EDUCATION LEVEL DETECTION
    # --------------------------------------------------

    @staticmethod
    def _education_level(text: str) -> int | None:
        """
        Detect the highest degree level mentioned.

        4 = Doctorate
        3 = Master's
        2 = Bachelor's
        1 = Associate / Diploma

        None = No recognized degree
        """

        patterns = [
            (
                4,
                r"\b(?:ph\.?\s?d\.?|doctorate|doctoral degree)\b",
            ),
            (
                3,
                r"\b(?:master'?s?(?:\s+degree)?|master of "
                r"(?:science|technology|engineering|arts)|"
                r"m\.?\s?s\.?|m\.?\s?sc\.?|m\.?\s?tech|"
                r"mba|mca)\b",
            ),
            (
                2,
                r"\b(?:bachelor'?s?(?:\s+degree)?|bachelor of "
                r"(?:science|technology|engineering|arts)|"
                r"b\.?\s?s\.?|b\.?\s?sc\.?|b\.?\s?tech|"
                r"b\.?\s?e\.?|bca)\b",
            ),
            (
                1,
                r"\b(?:associate'?s?(?:\s+degree)?|"
                r"associate degree|diploma)\b",
            ),
        ]

        for level, pattern in patterns:
            if re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            ):
                return level

        return None

    # --------------------------------------------------
    # EDUCATION MATCHING
    # --------------------------------------------------

    def _education_score(
        self,
        resume_education: list[str],
        job_text: str,
    ) -> float | None:
        """
        Compare resume education against job requirements.

        Returns:
            100.0 if degree level meets requirement
            0.0 if it does not
            None if no requirement is detected
        """

        required_level = self._education_level(
            job_text
        )

        # No explicit degree detected in job description
        if required_level is None:
            return None

        achieved_level = self._education_level(
            " ".join(resume_education)
        )

        if achieved_level is None:
            return 0.0

        if achieved_level >= required_level:
            return 100.0

        return 0.0

    # --------------------------------------------------
    # EXPERIENCE MATCHING
    # --------------------------------------------------

    def _exp_score(
        self,
        resume_yrs: int,
        required_yrs: int,
    ) -> float:

        if required_yrs == 0:
            return 100.0

        if resume_yrs >= required_yrs:
            return 100.0

        if resume_yrs >= required_yrs * 0.7:
            return 75.0

        if resume_yrs >= required_yrs * 0.5:
            return 50.0

        if resume_yrs > 0:
            return 25.0

        return 10.0

    # --------------------------------------------------
    # DETECT REQUIRED EXPERIENCE
    # --------------------------------------------------

    @staticmethod
    def _detect_required_years(
        text: str,
    ) -> int:

        match = re.search(
            r"(\d+)\+?\s*(?:years?|yrs?)",
            text,
            re.IGNORECASE,
        )

        return int(match.group(1)) if match else 0

    # --------------------------------------------------
    # COMPLETE AI MATCHING ANALYSIS
    # --------------------------------------------------

    def full_analysis(
        self,
        resume_text: str,
        job_text: str,
        job_skills: list[str] = None,
    ) -> dict:

        ai_logger.info(
            "Running full match analysis"
        )

        # STEP 1: EXTRACT RESUME INFORMATION

        resume_data = self.extractor.extract_all(
            resume_text
        )

        # STEP 2: SEMANTIC SIMILARITY

        overall = self.similarity(
            resume_text,
            job_text,
        )

        # STEP 3: SKILL MATCHING

        resume_skills = {
            skill.lower()
            for skill in resume_data["skills"]
        }

        required_skills = {
            skill.lower()
            for skill in (job_skills or [])
        }

        if not required_skills:
            extracted_skills = (
                self.extractor.extract_skills(job_text)
            )

            required_skills = {
                skill.lower()
                for skill in extracted_skills
            }

        matched_skills = (
            resume_skills & required_skills
        )

        missing_skills = (
            required_skills - resume_skills
        )

        extra_skills = (
            resume_skills - required_skills
        )

        skills_score = (
            round(
                len(matched_skills)
                / len(required_skills)
                * 100,
                2,
            )
            if required_skills
            else 0.0
        )

        # STEP 4: EXPERIENCE MATCHING

        required_years = (
            self._detect_required_years(job_text)
        )

        experience_score = self._exp_score(
            resume_data["years_experience"],
            required_years,
        )

        # STEP 5: EDUCATION MATCHING

        education_score = self._education_score(
            resume_data.get("education", []),
            job_text,
        )

        # STEP 6: ATS SCORE

        ats_score = self.ats.calculate(
            resume_text,
            job_text,
        )

        # STEP 7: WEIGHTED FINAL SCORE

        weighted_total = (
            overall * settings.WEIGHT_OVERALL
            + skills_score * settings.WEIGHT_SKILLS
            + experience_score * settings.WEIGHT_EXPERIENCE
        )

        active_weight = (
            settings.WEIGHT_OVERALL
            + settings.WEIGHT_SKILLS
            + settings.WEIGHT_EXPERIENCE
        )

        # Include education only if required
        if education_score is not None:

            weighted_total += (
                education_score
                * settings.WEIGHT_EDUCATION
            )

            active_weight += (
                settings.WEIGHT_EDUCATION
            )

        final_score = round(
            weighted_total / active_weight,
            2,
        )

        # STEP 8: RETURN DETAILED RESULTS

        result = {
            "overall": overall,
            "skills_match": skills_score,
            "experience_match": experience_score,
            "education_match": education_score,
            "ats_score": ats_score,
            "final_score": final_score,
            "matched_skills": sorted(matched_skills),
            "missing_skills": sorted(missing_skills),
            "extra_skills": sorted(extra_skills),
            "resume_data": resume_data,
        }

        ai_logger.info(
            "Match complete. Final: %s%%",
            final_score,
        )

        return result


# --------------------------------------------------
# MATCHING WRAPPER FOR FASTAPI
# --------------------------------------------------

@lru_cache(maxsize=1)
def get_matcher() -> BERTMatcher:
    """
    Cache the matcher to avoid reloading models
    for every analysis request.
    """
    return BERTMatcher()


def compare_resume_to_job(
    resume_text: str,
    job_description: str,
) -> dict:

    matcher = get_matcher()

    result = matcher.full_analysis(
        resume_text,
        job_description,
    )

    return {
        "score": result["final_score"],
        "resume_skills": [
            skill.lower()
            for skill in result["resume_data"]["skills"]
        ],
        "job_skills": sorted(
            result["matched_skills"]
            + result["missing_skills"]
        ),
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
    }
