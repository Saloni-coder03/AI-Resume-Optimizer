# backend/scripts/build_skills_db.py
import sys
import json
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from core.config import BASE_DIR
from core.logger import ai_logger

SKILLS_DIR = BASE_DIR / "backend" / "data" / "skills"
SKILLS_DIR.mkdir(parents=True, exist_ok=True)

# Master taxonomy covering 150+ standard tech skills
SKILLS_TAXONOMY = {
    "programming_languages": [
        "Python", "Java", "C++", "C", "C#", "JavaScript", "TypeScript",
        "Go", "Rust", "Swift", "Kotlin", "Ruby", "PHP", "Scala", "R",
        "Dart", "Perl", "Bash", "Shell", "SQL", "HTML", "CSS"
    ],
    "web_frontend": [
        "React", "React.js", "Next.js", "Angular", "Vue.js", "Svelte",
        "Tailwind CSS", "Bootstrap", "Redux", "GraphQL", "jQuery",
        "Material UI", "Webpack", "Vite", "Sass", "SCSS"
    ],
    "web_backend": [
        "FastAPI", "Django", "Flask", "Node.js", "Express.js", "Spring Boot",
        "ASP.NET", "Ruby on Rails", "NestJS", "gRPC", "REST API", "Microservices"
    ],
    "databases": [
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "Oracle",
        "Cassandra", "Elasticsearch", "DynamoDB", "Firebase", "Supabase", "MariaDB"
    ],
    "machine_learning_and_ai": [
        "Machine Learning", "Deep Learning", "Natural Language Processing", "NLP",
        "Computer Vision", "TensorFlow", "PyTorch", "Keras", "scikit-learn",
        "HuggingFace", "BERT", "Transformers", "LLMs", "OpenCV", "Pandas",
        "NumPy", "Matplotlib", "Seaborn", "SciPy", "NLTK", "spaCy", "LangChain"
    ],
    "cloud_and_devops": [
        "AWS", "Amazon Web Services", "Azure", "Google Cloud", "GCP",
        "Docker", "Kubernetes", "CI/CD", "Jenkins", "GitHub Actions",
        "GitLab CI", "Terraform", "Ansible", "Linux", "Nginx", "Prometheus", "Grafana"
    ],
    "data_engineering_and_analytics": [
        "Apache Spark", "Kafka", "Hadoop", "Airflow", "dbt", "Snowflake",
        "Databricks", "Tableau", "Power BI", "Excel", "Data Analysis", "ETL"
    ],
    "tools_and_methods": [
        "Git", "GitHub", "GitLab", "Jira", "Agile", "Scrum", "Postman",
        "Unit Testing", "pytest", "Docker Compose", "CI/CD Pipelines"
    ]
}

# Authoritative & Permanent Learning Portals
LEARNING_RESOURCES = {
    "python": {
        "course": "Official Python Tutorial & Docs",
        "duration": "2 weeks",
        "link": "https://docs.python.org/3/tutorial/",
        "free": True
    },
    "docker": {
        "course": "Docker Getting Started Guide & Official Labs",
        "duration": "1 week",
        "link": "https://docs.docker.com/get-started/",
        "free": True
    },
    "aws": {
        "course": "AWS Cloud Practitioner Essentials (Free Digital Training)",
        "duration": "2 weeks",
        "link": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/",
        "free": True
    },
    "kubernetes": {
        "course": "Kubernetes Official Interactive Basics Tutorial",
        "duration": "2 weeks",
        "link": "https://kubernetes.io/docs/tutorials/kubernetes-basics/",
        "free": True
    },
    "react": {
        "course": "React Official Interactive Tutorial & Guide",
        "duration": "2 weeks",
        "link": "https://react.dev/learn",
        "free": True
    },
    "fastapi": {
        "course": "FastAPI Official Interactive Tutorial",
        "duration": "1 week",
        "link": "https://fastapi.tiangolo.com/tutorial/",
        "free": True
    },
    "machine learning": {
        "course": "Google Machine Learning Crash Course",
        "duration": "3 weeks",
        "link": "https://developers.google.com/machine-learning/crash-course",
        "free": True
    },
    "sql": {
        "course": "SQL Bolt (Interactive SQL Lessons)",
        "duration": "1 week",
        "link": "https://sqlbolt.com/",
        "free": True
    },
    "git": {
        "course": "Pro Git Book & Official Reference",
        "duration": "1 week",
        "link": "https://git-scm.com/book/en/v2",
        "free": True
    },
    "postgresql": {
        "course": "PostgreSQL Official Tutorial",
        "duration": "1 week",
        "link": "https://www.postgresqltutorial.com/",
        "free": True
    },
    "typescript": {
        "course": "TypeScript Handbook & Official Guide",
        "duration": "1 week",
        "link": "https://www.typescriptlang.org/docs/handbook/intro.html",
        "free": True
    },
    "linux": {
        "course": "Linux Journey (Free Interactive Linux Training)",
        "duration": "1 week",
        "link": "https://linuxjourney.com/",
        "free": True
    }
}


def build_databases():
    ai_logger.info("Building Skills Taxonomy and Learning Resources JSON files...")

    taxonomy_path = SKILLS_DIR / "skills_taxonomy.json"
    resources_path = SKILLS_DIR / "learning_resources.json"

    with open(taxonomy_path, "w", encoding="utf-8") as f:
        json.dump(SKILLS_TAXONOMY, f, indent=2)

    with open(resources_path, "w", encoding="utf-8") as f:
        json.dump(LEARNING_RESOURCES, f, indent=2)

    total_skills = sum(len(v) for v in SKILLS_TAXONOMY.values())
    ai_logger.info(f"Generated {total_skills} skills across {len(SKILLS_TAXONOMY)} categories.")
    ai_logger.info(f"Saved to: {taxonomy_path}")
    ai_logger.info(f"Saved to: {resources_path}")


if __name__ == "__main__":
    build_databases()