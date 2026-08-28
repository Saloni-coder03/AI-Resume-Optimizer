import re


SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "react",
    "angular",
    "vue",
    "node.js",
    "express",
    "fastapi",
    "django",
    "flask",

    "html",
    "css",
    "tailwind",
    "bootstrap",

    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "redis",

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "natural language processing",
    "nlp",
    "computer vision",

    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",

    "docker",
    "kubernetes",

    "aws",
    "azure",
    "gcp",

    "git",
    "github",
    "linux",

    "rest api",
    "microservices",

    "power bi",
    "tableau",
    "excel",

    "c",
    "c++",
    "c#",

    "spring boot",
    "firebase",

    "agile",
    "scrum",

    "communication",
    "leadership",
    "problem solving",
    "teamwork",
]


def normalize_text(text: str) -> str:
    """
    Convert text to lowercase and remove extra whitespace.
    """

    text = text.lower()

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def contains_skill(text: str, skill: str) -> bool:
    """
    Check whether a skill exists in the given text.
    """

    text = normalize_text(text)
    skill = skill.lower()

    # Skills containing special characters
    special_skills = [
        "c++",
        "c#",
        "node.js",
    ]

    if skill in special_skills:
        return skill in text

    pattern = r"\b" + re.escape(skill) + r"\b"

    return bool(
        re.search(pattern, text)
    )


def extract_skills(text: str) -> list[str]:
    """
    Extract known skills from resume or job description text.
    """

    detected_skills = []

    for skill in SKILLS:

        if contains_skill(text, skill):
            detected_skills.append(skill)

    return sorted(
        set(detected_skills)
    )


def compare_resume_to_job(
    resume_text: str,
    job_description: str
) -> dict:
    """
    Compare resume skills with job-description skills.
    """

    resume_skills = set(
        extract_skills(resume_text)
    )

    job_skills = set(
        extract_skills(job_description)
    )


    matched_skills = sorted(
        resume_skills.intersection(
            job_skills
        )
    )


    missing_skills = sorted(
        job_skills.difference(
            resume_skills
        )
    )


    # Calculate score
    if len(job_skills) == 0:

        score = 0.0

    else:

        score = (
            len(matched_skills)
            / len(job_skills)
        ) * 100


    return {

        "score": round(score, 2),

        "resume_skills":
            sorted(resume_skills),

        "job_skills":
            sorted(job_skills),

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,
    }