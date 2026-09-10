import sys

from loguru import logger

from src.common.config import settings
from src.common.paths import LOGS_DIR

LOG_FILE = LOGS_DIR / "app.log"

logger.remove()

logger.add(
    sys.stdout,
    level=settings.log_level.upper(),
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>",
    colorize=True,
)

logger.add(
    LOG_FILE,
    level=settings.log_level.upper(),
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
)