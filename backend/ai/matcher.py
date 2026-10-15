# backend/ai/matcher.py
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from core.config import settings
from core.logger import ai_logger
from core.exceptions import ModelLoadError, MatchingEngineError
from ai.section_extractor import SectionExtractor
from ai.ats_calculator import ATSCalculator


class BERTMatcher:

    def __init__(self):
        ai_logger.info(f"Loading BERT model: {settings.BERT_MODEL_NAME}")
        try:
            self.model = SentenceTransformer(settings.BERT_MODEL_NAME)
            ai_logger.info("BERT model loaded")
        except Exception as e:
            ai_logger.error(f"BERT load failed: {e}")
            raise ModelLoadError(settings.BERT_MODEL_NAME) from e

        self.extractor = SectionExtractor()
        self.ats = ATSCalculator()

    def similarity(self, text1: str, text2: str) -> float:
        try:
            v1 = self.model.encode(text1)
            v2 = self.model.encode(text2)
            score = cosine_similarity([v1], [v2])[0][0]
            return round(float(score * 100), 2)
        except Exception as e:
            ai_logger.error(f"Similarity failed: {e}")
            raise MatchingEngineError(str(e)) from e

    def full_analysis(self, resume_text: str, job_text: str, job_skills: list[str] = None) -> dict:
        ai_logger.info("Running full match analysis")

        resume_data = self.extractor.extract_all(resume_text)

        overall = self.similarity(resume_text, job_text)

        # Skills analysis
        r_skills = set(s.lower() for s in resume_data["skills"])
        j_skills = set(s.lower() for s in (job_skills or []))

        if not j_skills:
            j_skills_extracted = self.extractor.extract_skills(job_text)
            j_skills = set(s.lower() for s in j_skills_extracted)

        matched = r_skills & j_skills
        missing = j_skills - r_skills
        extra = r_skills - j_skills

        skills_score = round(len(matched) / len(j_skills) * 100, 2) if j_skills else 0.0

        # Experience
        exp_score = self._exp_score(
            resume_data["years_experience"],
            self._detect_required_years(job_text)
        )

        # Education
        edu_score = 100.0

        # ATS
        ats_score = self.ats.calculate(resume_text, job_text)

        # Final weighted score
        final = round(
            overall * settings.WEIGHT_OVERALL +
            skills_score * settings.WEIGHT_SKILLS +
            exp_score * settings.WEIGHT_EXPERIENCE +
            edu_score * settings.WEIGHT_EDUCATION,
            2
        )

        result = {
            "overall": overall,
            "skills_match": skills_score,
            "experience_match": exp_score,
            "education_match": edu_score,
            "ats_score": ats_score,
            "final_score": final,
            "matched_skills": sorted(matched),
            "missing_skills": sorted(missing),
            "extra_skills": sorted(extra),
            "resume_data": resume_data
        }

        ai_logger.info(f"Match complete. Final: {final}%")
        return result

    def _exp_score(self, resume_yrs: int, required_yrs: int) -> float:
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

    @staticmethod
    def _detect_required_years(text: str) -> int:
        import re
        m = re.search(r"(\d+)\+?\s*(?:years?|yrs?)", text, re.IGNORECASE)
        return int(m.group(1)) if m else 0


# Wrapper for friend's match_routes.py compatibility
def compare_resume_to_job(resume_text: str, job_description: str) -> dict:
    matcher = BERTMatcher()
    result = matcher.full_analysis(resume_text, job_description)
    return {
        "score": result["final_score"],
        "resume_skills": [s.lower() for s in result["resume_data"]["skills"]],
        "job_skills": result["matched_skills"] + result["missing_skills"],
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
    }