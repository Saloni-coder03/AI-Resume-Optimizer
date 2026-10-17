
import pytest

from ai.ats_calculator import ATSCalculator


@pytest.fixture
def calculator():
    return ATSCalculator()


def test_identical_keywords(calculator):
    score = calculator.keyword_score(
        "Python SQL Docker FastAPI",
        "Python SQL Docker FastAPI",
    )

    assert score == 40.0


def test_partial_keyword_coverage(calculator):
    score = calculator.keyword_score(
        "Python SQL",
        "Python SQL Docker AWS",
    )

    assert score == 20.0


def test_punctuation_normalization(calculator):
    score = calculator.keyword_score(
        "Python, SQL. Docker!",
        "Python SQL Docker",
    )

    assert score == 40.0


def test_no_keyword_match(calculator):
    score = calculator.keyword_score(
        "Java Spring",
        "Python SQL Docker",
    )

    assert score == 0.0


def test_quantified_achievements(calculator):
    resume = """
    Improved performance by 40%.
    Served 1M users.
    Reduced costs by $5000.
    """

    assert calculator.achievement_score(resume) == 10.0


def test_experience_years_not_achievement(calculator):
    resume = "Software engineer with 3 years of experience."

    assert calculator.achievement_score(resume) == 0.0


def test_section_headings(calculator):
    resume = """
Experience
Education
Skills
Projects
Summary
"""

    assert calculator.section_score(resume) == 20.0


def test_full_score_within_bounds(calculator):
    resume = """
John Smith
Email: john@example.com
Phone: 9876543210

Skills
Python SQL Docker

Experience
Improved performance by 40%.
Served 1M users.

Education
Bachelor of Technology

Projects
Built Python applications.

Summary
Software developer.
"""

    score = calculator.calculate(
        resume,
        "Python SQL Docker AWS",
    )

    assert 0.0 <= score <= 100.0
