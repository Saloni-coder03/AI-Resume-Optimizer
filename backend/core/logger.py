
# backend/core/logger.py

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

api_logger = logging.getLogger("resume_optimizer.api")
