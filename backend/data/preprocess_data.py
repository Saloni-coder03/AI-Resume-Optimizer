# backend/data/preprocess_data.py
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import pandas as pd
from core.config import BASE_DIR
from core.logger import ai_logger

RAW_DIR = BASE_DIR / "backend" / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "backend" / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def preprocess_resumes():
    input_path = RAW_DIR / "resumes_dataset.csv"
    output_path = PROCESSED_DIR / "clean_resumes.csv"

    if not input_path.exists():
        ai_logger.warning("No resumes dataset found. Run download_data.py first.")
        return

    ai_logger.info("Preprocessing resumes...")
    df = pd.read_csv(input_path)

    # Remove empty rows
    df = df.dropna(subset=[df.columns[-1]])

    # Remove duplicates
    df = df.drop_duplicates()

    # Clean text
    text_col = df.columns[-1]
    df[text_col] = df[text_col].astype(str).str.strip()
    df = df[df[text_col].str.len() > 50]

    df.to_csv(output_path, index=False)
    ai_logger.info(f"Cleaned resumes saved: {len(df)} rows → {output_path}")


def preprocess_jobs():
    input_path = RAW_DIR / "jobs_dataset.csv"
    output_path = PROCESSED_DIR / "clean_jobs.csv"

    if not input_path.exists():
        ai_logger.warning("No jobs dataset found. Run download_data.py first.")
        return

    ai_logger.info("Preprocessing jobs...")
    df = pd.read_csv(input_path)

    # Remove empty rows
    df = df.dropna()

    # Remove duplicates
    df = df.drop_duplicates()

    # Clean text columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    df.to_csv(output_path, index=False)
    ai_logger.info(f"Cleaned jobs saved: {len(df)} rows → {output_path}")


if __name__ == "__main__":
    preprocess_resumes()
    preprocess_jobs()
    ai_logger.info("Preprocessing complete!")