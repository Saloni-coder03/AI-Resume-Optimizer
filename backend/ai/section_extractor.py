# backend/ai/section_extractor.py
import re
import json
from typing import Any
import spacy

from core.config import BASE_DIR, settings
from core.logger import ai_logger
from core.exceptions import ModelLoadError


class SectionExtractor:

    def __init__(self):
        self._load_spacy()
        self._load_taxonomy()

        self.email_re = re.compile(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        )
        self.phone_re = re.compile(
            r"(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}"
        )
        self.linkedin_re = re.compile(
            r"(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+/?",
            re.IGNORECASE
        )
        self.github_re = re.compile(
            r"(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+/?",
            re.IGNORECASE
        )
        self.degree_patterns = [
            r"\b(Ph\.?D\.?|Doctorate)\b",
            r"\b(M\.?S\.?|M\.?Tech|MBA|MCA|Master of Science|Master of Technology)\b",
            r"\b(B\.?S\.?|B\.?Sc\.?|B\.?Tech|B\.?E\.?|BCA|Bachelor of Technology|Bachelor of Engineering)\b",
            r"\b(Diploma|Associate Degree)\b"
        ]

    def _load_spacy(self):
        ai_logger.info(f"Loading spaCy: {settings.SPACY_MODEL_NAME}")
        try:
            self.nlp = spacy.load(settings.SPACY_MODEL_NAME)
        except Exception as e:
            ai_logger.error(f"spaCy load failed: {e}")
            raise ModelLoadError(settings.SPACY_MODEL_NAME) from e

    def _load_taxonomy(self):
        path = BASE_DIR / "backend" / "data" / "skills" / "skills_taxonomy.json"
        if not path.exists():
            ai_logger.warning("Taxonomy missing, using fallback")
            self.skills_list = ["Python", "Java", "SQL", "Docker", "AWS", "Git"]
            return
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        all_skills = []
        for skills in data.values():
            all_skills.extend(skills)
        self.skills_list = sorted(set(all_skills), key=len, reverse=True)
        ai_logger.info(f"Loaded {len(self.skills_list)} skills from taxonomy")

    def extract_all(self, text: str) -> dict[str, Any]:
        ai_logger.info("Extracting sections from resume")
        result = {
            "contact": self.extract_contact(text),
            "skills": self.extract_skills(text),
            "education": self.extract_education(text),
            "organizations": self.extract_organizations(text),
            "years_experience": self.extract_years(text),
            "word_count": len(text.split()),
            "has_numbers": self.has_numbers(text),
            "full_text": text
        }
        ai_logger.info(
            f"Extracted {len(result['skills'])} skills, "
            f"{result['years_experience']} yrs exp"
        )
        return result

    def extract_skills(self, text: str) -> list[str]:
        found = set()
        for skill in self.skills_list:
            pattern = rf"(?i)\b{re.escape(skill)}\b"
            if re.search(pattern, text):
                found.add(skill)
        return sorted(found)

    def extract_contact(self, text: str) -> dict:
        emails = self.email_re.findall(text)
        phones = self.phone_re.findall(text)
        linkedin = self.linkedin_re.findall(text)
        github = self.github_re.findall(text)

        phone = None
        if phones:
            raw = "".join(phones[0]) if isinstance(phones[0], tuple) else phones[0]
            phone = re.sub(r"[^\d+]", "", raw)

        return {
            "email": emails[0] if emails else None,
            "phone": phone,
            "linkedin": linkedin[0] if linkedin else None,
            "github": github[0] if github else None
        }

    def extract_education(self, text: str) -> list[str]:
        degrees = set()
        for p in self.degree_patterns:
            for m in re.findall(p, text, re.IGNORECASE):
                degrees.add(m.strip())
        return sorted(degrees)

    def extract_organizations(self, text: str) -> list[str]:
        doc = self.nlp(text[:2500])
        orgs = {e.text.strip() for e in doc.ents if e.label_ == "ORG" and len(e.text.strip()) > 2}
        return sorted(orgs)[:10]

    def extract_years(self, text: str) -> int:
        patterns = [
            r"(\d{1,2})\+?\s*(?:years?|yrs?)(?:\s*of)?\s*(?:experience|exp)",
            r"(?:experience|exp)\s*(?:of)?\s*(\d{1,2})\+?\s*(?:years?|yrs?)",
        ]
        max_y = 0
        for p in patterns:
            for m in re.findall(p, text, re.IGNORECASE):
                try:
                    v = int(m)
                    if 0 < v <= 40:
                        max_y = max(max_y, v)
                except ValueError:
                    pass
        return max_y
    
    
    @staticmethod
    def has_numbers(text: str) -> bool:
        """Check for measurable achievements in resume text."""

        import re

        patterns = [
            # Percentages: 40%, 12.5%
            r"\b\d+(?:\.\d+)?\s*%",

            # Money: $500, $2.5M
            r"\$\s*\d[\d,]*(?:\.\d+)?\s*[kKmMbB]?",

            # Metrics: 1M users, 250 clients
            r"\b\d+(?:\.\d+)?\s*[kKmMbB]?\s*"
            r"(?:users|clients|customers|requests|transactions)\b",
        ]

        return any(
            re.search(pattern, text, re.IGNORECASE)
            for pattern in patterns
        )
