# backend/tests/test_matcher.py
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import pytest
from ai.matcher import BERTMatcher
from ai.ats_calculator import ATSCalculator
from ai.recommendations import RecommendationsEngine


@pytest.fixture
def matcher():
    return BERTMatcher()


@pytest.fixture
def ats():
    return ATSCalculator()


@pytest.fixture
def engine():
    return RecommendationsEngine()


GOOD_RESUME = """
Senior Python Developer with 5 years of experience.
Skills: Python, Django, FastAPI, PostgreSQL, Docker, AWS, REST API.
B.Tech Computer Science. Improved performance by 40%.
"""

MATCHING_JOB = """
Looking for Python Developer with Django and FastAPI experience.
Skills required: Python, Django, FastAPI, PostgreSQL, Docker, AWS.
2+ years experience required.
"""

UNRELATED_JOB = """
Hiring Marketing Manager with 5 years experience.
Skills: SEO, Digital Marketing, Google Analytics, Content Strategy.
MBA preferred.
"""


def test_similarity_high(matcher):
    score = matcher.similarity(
        "Python developer with Django experience",
        "Looking for Python Django developer"
    )
    assert score > 60


def test_similarity_low(matcher):
    score = matcher.similarity(
        "Python developer with Django experience",
        "Hiring chef for Italian restaurant"
    )
    assert score < 50


def test_full_analysis(matcher):
    result = matcher.full_analysis(GOOD_RESUME, MATCHING_JOB)
    assert "final_score" in result
    assert "matched_skills" in result
    assert "missing_skills" in result
    assert 0 <= result["final_score"] <= 100


def test_good_match_higher_than_bad(matcher):
    good = matcher.full_analysis(GOOD_RESUME, MATCHING_JOB)
    bad = matcher.full_analysis(GOOD_RESUME, UNRELATED_JOB)
    assert good["final_score"] > bad["final_score"]


def test_ats_score(ats):
    score = ats.calculate(GOOD_RESUME, MATCHING_JOB)
    assert 0 <= score <= 100
    assert score > 30


def test_recommendations(engine):
    recs = engine.generate(
        matched=["Python", "Docker"],
        missing=["AWS", "Kubernetes"]
    )
    assert len(recs) > 0
    assert any("AWS" in r or "Kubernetes" in r for r in recs)


def test_roadmap_with_resources(engine):
    roadmap = engine.roadmap(["Python", "Docker"])
    assert len(roadmap) > 0


def test_roadmap_no_missing(engine):
    roadmap = engine.roadmap([])
    assert len(roadmap) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])