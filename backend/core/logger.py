import logging
import logging.handlers
from core.config import settings

FORMATTER = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(name)-12s | %(filename)s:%(lineno)d | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

_error_handler = logging.handlers.RotatingFileHandler(
    filename=settings.LOG_PATH / settings.LOG_FILE_ERROR,
    maxBytes=settings.LOG_MAX_BYTES,
    backupCount=settings.LOG_BACKUP_COUNT,
    encoding="utf-8"
)
_error_handler.setLevel(logging.ERROR)
_error_handler.setFormatter(FORMATTER)

def setup_logger(name: str, log_file: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)
    logger.propagate = False

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(settings.LOG_LEVEL)
        console_handler.setFormatter(FORMATTER)

        file_handler = logging.handlers.RotatingFileHandler(
            filename=settings.LOG_PATH / log_file,
            maxBytes=settings.LOG_MAX_BYTES,
            backupCount=settings.LOG_BACKUP_COUNT,
            encoding="utf-8"
        )
        file_handler.setLevel(settings.LOG_LEVEL)
        file_handler.setFormatter(FORMATTER)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.addHandler(_error_handler)

    return logger

ai_logger = setup_logger("AI_ENGINE", settings.LOG_FILE_AI)
api_logger = setup_logger("API_GATEWAY", settings.LOG_FILE_API)
db_logger = setup_logger("DATABASE", settings.LOG_FILE_DB)
app_logger = setup_logger("APP_CORE", settings.LOG_FILE_APP)