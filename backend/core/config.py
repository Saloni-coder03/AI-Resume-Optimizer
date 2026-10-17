
from pathlib import Path
from functools import lru_cache
from urllib.parse import quote_plus

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            str(BASE_DIR / ".env"),
            str(BASE_DIR / "backend" / ".env"),
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --------------------------------------------------
    # REQUIRED ENVIRONMENT VARIABLES
    # --------------------------------------------------

    SECRET_KEY: str
    DATABASE_PASSWORD: str

    # --------------------------------------------------
    # APPLICATION SETTINGS
    # --------------------------------------------------

    APP_NAME: str = "AI Resume Optimizer"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True

    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    FRONTEND_URL: str = "http://localhost:3000"

    # Configurable allowed frontend origins
    CORS_ORIGINS: str = (
        "http://localhost:3000,"
        "http://127.0.0.1:3000"
    )

    # --------------------------------------------------
    # DATABASE SETTINGS
    # --------------------------------------------------

    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "resumedb"
    DATABASE_USER: str = "postgres"

    # --------------------------------------------------
    # AI MODEL SETTINGS
    # --------------------------------------------------

    BERT_MODEL_NAME: str = "all-MiniLM-L6-v2"
    SPACY_MODEL_NAME: str = "en_core_web_lg"

    # --------------------------------------------------
    # FILE UPLOAD SETTINGS
    # --------------------------------------------------

    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 5

    # Preserve Person 1's parser configuration.
    # API upload endpoints currently restrict to PDF/DOCX.
    ALLOWED_EXTENSIONS: str = ".pdf,.doc,.docx"

    # --------------------------------------------------
    # LOGGING SETTINGS
    # --------------------------------------------------

    LOG_LEVEL: str = "DEBUG"
    LOG_DIR: str = "logs"

    LOG_FILE_APP: str = "app.log"
    LOG_FILE_ERROR: str = "error.log"
    LOG_FILE_AI: str = "ai.log"
    LOG_FILE_API: str = "api.log"
    LOG_FILE_DB: str = "db.log"

    LOG_MAX_BYTES: int = 10_485_760
    LOG_BACKUP_COUNT: int = 5

    # --------------------------------------------------
    # AI MATCHING WEIGHTS
    # --------------------------------------------------

    WEIGHT_OVERALL: float = 0.35
    WEIGHT_SKILLS: float = 0.40
    WEIGHT_EXPERIENCE: float = 0.15
    WEIGHT_EDUCATION: float = 0.10

    # --------------------------------------------------
    # SCORE THRESHOLDS
    # --------------------------------------------------

    SCORE_EXCELLENT: int = 80
    SCORE_GOOD: int = 60
    SCORE_AVERAGE: int = 40

    # --------------------------------------------------
    # ATS SETTINGS
    # --------------------------------------------------

    ATS_MIN_WORD_COUNT: int = 300
    ATS_MAX_WORD_COUNT: int = 700
    ATS_MIN_NUMBERS: int = 3

    # --------------------------------------------------
    # RECOMMENDATION SETTINGS
    # --------------------------------------------------

    MAX_RECOMMENDATIONS: int = 10
    MAX_MISSING_SKILLS: int = 5
    MAX_ROADMAP_ITEMS: int = 3

    # --------------------------------------------------
    # VALIDATE SCORING WEIGHTS
    # --------------------------------------------------

    @model_validator(mode="after")
    def validate_scoring_weights(self) -> "Settings":
        total = (
            self.WEIGHT_OVERALL
            + self.WEIGHT_SKILLS
            + self.WEIGHT_EXPERIENCE
            + self.WEIGHT_EDUCATION
        )

        if abs(total - 1.0) > 0.001:
            raise ValueError(
                "Configuration Error: Scoring weights must "
                f"sum to 1.0. Current sum is {total:.4f}"
            )

        return self

    # --------------------------------------------------
    # VALIDATE SCORE THRESHOLDS
    # --------------------------------------------------

    @model_validator(mode="after")
    def validate_threshold_hierarchy(self) -> "Settings":
        if not (
            self.SCORE_EXCELLENT
            > self.SCORE_GOOD
            > self.SCORE_AVERAGE
        ):
            raise ValueError(
                "Configuration Error: Score thresholds must "
                "follow hierarchy: "
                f"SCORE_EXCELLENT ({self.SCORE_EXCELLENT}) > "
                f"SCORE_GOOD ({self.SCORE_GOOD}) > "
                f"SCORE_AVERAGE ({self.SCORE_AVERAGE})"
            )

        return self

    # --------------------------------------------------
    # DATABASE CONNECTION URL
    # --------------------------------------------------

    @property
    def DATABASE_URL(self) -> str:
        encoded_password = quote_plus(
            self.DATABASE_PASSWORD
        )

        return (
            f"postgresql://{self.DATABASE_USER}"
            f":{encoded_password}"
            f"@{self.DATABASE_HOST}"
            f":{self.DATABASE_PORT}"
            f"/{self.DATABASE_NAME}"
        )

    # --------------------------------------------------
    # CORS ORIGINS LIST
    # --------------------------------------------------

    @property
    def CORS_ORIGINS_LIST(self) -> list[str]:
        """
        Convert comma-separated CORS origins into a list.

        Example:
        http://localhost:3000,http://127.0.0.1:3000
        """

        return [
            origin.strip().rstrip("/")
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]

    # --------------------------------------------------
    # ALLOWED FILE EXTENSIONS
    # --------------------------------------------------

    @property
    def ALLOWED_EXTENSIONS_LIST(self) -> list[str]:
        return [
            ext.strip().lower()
            for ext in self.ALLOWED_EXTENSIONS.split(",")
        ]

    # --------------------------------------------------
    # MAXIMUM FILE SIZE IN BYTES
    # --------------------------------------------------

    @property
    def MAX_FILE_SIZE_BYTES(self) -> int:
        return self.MAX_FILE_SIZE_MB * 1024 * 1024

    # --------------------------------------------------
    # UPLOAD DIRECTORY
    # --------------------------------------------------

    @property
    def UPLOAD_PATH(self) -> Path:
        path = (
            BASE_DIR
            / "backend"
            / self.UPLOAD_DIR
        )

        path.mkdir(
            parents=True,
            exist_ok=True,
        )

        return path

    # --------------------------------------------------
    # LOG DIRECTORY
    # --------------------------------------------------

    @property
    def LOG_PATH(self) -> Path:
        path = (
            BASE_DIR
            / "backend"
            / self.LOG_DIR
        )

        path.mkdir(
            parents=True,
            exist_ok=True,
        )

        return path


# --------------------------------------------------
# CACHED SETTINGS INSTANCE
# --------------------------------------------------

@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
