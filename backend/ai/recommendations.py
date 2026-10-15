# backend/ai/recommendations.py
import json
from pathlib import Path

from core.config import BASE_DIR, settings
from core.logger import ai_logger


class RecommendationsEngine:

    def __init__(self):
        self._load_resources()

    def _load_resources(self):
        path = BASE_DIR / "backend" / "data" / "skills" / "learning_resources.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                self.resources = json.load(f)
        else:
            self.resources = {}

    def generate(self, matched: list[str], missing: list[str], scores: dict = None) -> list[str]:
        ai_logger.info("Generating recommendations")
        recs = []

        if matched:
            recs.append(
                "Highlight your matched skills prominently: "
                + ", ".join(matched[:5]) + "."
            )

        if missing:
            top = missing[:settings.MAX_MISSING_SKILLS]
            recs.append(
                "Consider learning these missing skills: "
                + ", ".join(top) + "."
            )

        if len(matched) < 3:
            recs.append(
                "Add more relevant technical skills and projects "
                "that match the job description."
            )

        recs.append(
            "Use measurable achievements: percent improvements, "
            "users served, revenue generated."
        )

        recs.append(
            "Mirror keywords from the job description "
            "naturally throughout your resume."
        )

        return recs[:settings.MAX_RECOMMENDATIONS]

    def roadmap(self, missing: list[str]) -> list[str]:
        if not missing:
            return [
                "Continue strengthening your current skills.",
                "Build projects with your strongest technologies.",
                "Prepare examples for technical interviews."
            ]

        steps = []
        for skill in missing[:settings.MAX_ROADMAP_ITEMS]:
            key = skill.lower()
            if key in self.resources:
                r = self.resources[key]
                steps.append(
                    f"Learn {skill.title()}: {r['course']} "
                    f"({r['duration']}) - {r['link']}"
                )
            else:
                steps.append(
                    f"Learn {skill.title()} fundamentals and "
                    f"build a small practical project using it."
                )
        return steps


# Wrapper functions for friend's match_routes.py compatibility
def generate_recommendations(matched_skills: list[str], missing_skills: list[str]) -> list[str]:
    engine = RecommendationsEngine()
    return engine.generate(matched_skills, missing_skills)


def generate_learning_roadmap(missing_skills: list[str]) -> list[str]:
    engine = RecommendationsEngine()
    return engine.roadmap(missing_skills) 