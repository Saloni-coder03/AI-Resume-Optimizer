# backend/tests/test_extractor.py
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import pytest
from ai.section_extractor import SectionExtractor


@pytest.fixture
def extractor():
    return SectionExtractor()


SAMPLE_RESUME = """
John Doe
Email: john.doe@gmail.com
Phone: +91 9876543210
LinkedIn: linkedin.com/in/johndoe
GitHub: github.com/johndoe

Software Engineer with 3 years of experience in Python,
Django, FastAPI, PostgreSQL, and Docker.

Education: B.Tech in Computer Science

Improved API response time by 40%.
Managed database serving 1M users.
"""


def test_extract_skills(extractor):
    skills = extractor.extract_skills(SAMPLE_RESUME)
    assert "Python" in skills
    assert "Docker" in skills
    assert "PostgreSQL" in skills


def test_extract_email(extractor):
    contact = extractor.extract_contact(SAMPLE_RESUME)
    assert contact["email"] == "john.doe@gmail.com"


def test_extract_phone(extractor):
    contact = extractor.extract_contact(SAMPLE_RESUME)
    assert contact["phone"] is not None


def test_extract_linkedin(extractor):
    contact = extractor.extract_contact(SAMPLE_RESUME)
    assert "linkedin" in contact["linkedin"].lower()


def test_extract_github(extractor):
    contact = extractor.extract_contact(SAMPLE_RESUME)
    assert "github" in contact["github"].lower()


def test_extract_education(extractor):
    education = extractor.extract_education(SAMPLE_RESUME)
    assert any("B.Tech" in e for e in education)


def test_extract_experience_years(extractor):
    years = extractor.extract_years(SAMPLE_RESUME)
    assert years == 3


def test_has_numbers(extractor):
    assert extractor.has_numbers(SAMPLE_RESUME) is True


def test_no_numbers():
    ext = SectionExtractor()
    text = "Just a plain text resume with no numbers at all."
    assert ext.has_numbers(text) is False


def test_extract_all(extractor):
    result = extractor.extract_all(SAMPLE_RESUME)
    assert "skills" in result
    assert "contact" in result
    assert "education" in result
    assert "years_experience" in result
    assert "word_count" in result
    assert result["word_count"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
    