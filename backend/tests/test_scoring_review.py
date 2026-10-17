
from ai.ats_calculator import ATSCalculator
from ai.matcher import BERTMatcher


def test_education_score_is_not_automatically_perfect():
    """Education should not always receive 100 points."""

    class FakeExtractor:
        def extract_all(self, text):
            return {
                "skills": ["Python"],
                "years_experience": 2,
                "education": [],
            }

        def extract_skills(self, text):
            return ["Python"]

    # Bypass model initialization for this unit test.
    matcher = BERTMatcher.__new__(BERTMatcher)
    matcher.extractor = FakeExtractor()
    matcher.ats = ATSCalculator()
    matcher.similarity = lambda a, b: 80.0

    result = matcher.full_analysis(
        "Python developer with 2 years of experience.",
        "Python developer requiring a bachelor's degree "
        "in Computer Science and 2 years of experience.",
    )

    assert result["education_match"] != 100.0, (
        "Education score is hardcoded to 100."
    )


def test_ats_keyword_coverage():
    """More relevant keywords should improve the score."""

    calculator = ATSCalculator()

    job_description = (
        "Python SQL Docker Kubernetes AWS FastAPI"
    )

    resume_fewer_skills = (
        "Skills: Python SQL"
    )

    resume_more_skills = (
        "Skills: Python SQL Docker Kubernetes AWS FastAPI"
    )

    fewer_score = calculator.calculate(
        resume_fewer_skills,
        job_description,
    )

    more_score = calculator.calculate(
        resume_more_skills,
        job_description,
    )

    assert more_score > fewer_score, (
        "Matching additional required skills "
        "should improve the ATS score."
    )
