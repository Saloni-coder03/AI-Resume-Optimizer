# backend/data/download_data.py
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import pandas as pd
from core.config import BASE_DIR
from core.logger import ai_logger

RAW_DIR = BASE_DIR / "backend" / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def download_from_kaggle():
    ai_logger.info("Downloading datasets from Kaggle...")

    try:
        import kaggle
    except Exception:
        ai_logger.error(
            "Kaggle package not configured. "
            "Run: pip install kaggle and setup ~/.kaggle/kaggle.json"
        )
        return

    datasets = [
        {
            "name": "snehaanbhawal/resume-dataset",
            "file": "resumes_dataset.csv"
        },
        {
            "name": "ravindrasinghrana/job-description-dataset",
            "file": "jobs_dataset.csv"
        }
    ]

    for ds in datasets:
        output_path = RAW_DIR / ds["file"]
        if output_path.exists():
            ai_logger.info(f"Already exists: {ds['file']}")
            continue

        try:
            ai_logger.info(f"Downloading: {ds['name']}")
            kaggle.api.dataset_download_files(
                ds["name"],
                path=str(RAW_DIR),
                unzip=True,
                quiet=True
            )
            ai_logger.info(f"Downloaded: {ds['file']}")
        except Exception as e:
            ai_logger.error(f"Failed to download {ds['name']}: {e}")


def create_sample_data():
    ai_logger.info("Creating sample data for testing...")

    resumes_path = RAW_DIR / "resumes_dataset.csv"
    jobs_path = RAW_DIR / "jobs_dataset.csv"

    if not resumes_path.exists():
        sample_resumes = pd.DataFrame({
            "Category": [
                "Software Engineer", "Data Scientist",
                "Frontend Developer", "DevOps Engineer"
            ],
            "Resume": [
                "Python developer with 3 years experience in Django, FastAPI, PostgreSQL. B.Tech CSE. Improved API response time by 40%.",
                "Data scientist with 5 years experience in Machine Learning, TensorFlow, Pandas, NumPy. M.Tech AI. Built recommendation engine serving 1M users.",
                "Frontend developer with 2 years experience in React, TypeScript, Tailwind CSS. B.Tech IT. Reduced page load time by 35%.",
                "DevOps engineer with 4 years experience in Docker, Kubernetes, AWS, CI/CD. B.Tech CSE. Managed 50+ microservices."
            ]
        })
        sample_resumes.to_csv(resumes_path, index=False)
        ai_logger.info("Created sample resumes dataset")

    if not jobs_path.exists():
        sample_jobs = pd.DataFrame({
            "Job_Title": [
                "Python Developer", "Data Scientist",
                "Frontend Developer", "DevOps Engineer"
            ],
            "Description": [
                "Looking for Python developer with experience in Django, FastAPI, REST API, PostgreSQL, Docker. 2+ years experience required.",
                "Seeking data scientist with Machine Learning, Deep Learning, TensorFlow, Python, SQL skills. 3+ years experience.",
                "Hiring frontend developer with React, TypeScript, CSS, HTML experience. 1+ years experience required.",
                "Need DevOps engineer with Docker, Kubernetes, AWS, CI/CD, Linux experience. 3+ years experience."
            ],
            "Required_Skills": [
                "Python,Django,FastAPI,PostgreSQL,Docker",
                "Machine Learning,TensorFlow,Python,SQL,Pandas",
                "React,TypeScript,CSS,HTML",
                "Docker,Kubernetes,AWS,CI/CD,Linux"
            ]
        })
        sample_jobs.to_csv(jobs_path, index=False)
        ai_logger.info("Created sample jobs dataset")


if __name__ == "__main__":
    create_sample_data()
    ai_logger.info("Data download complete!")