import logging
from logging.handlers import RotatingFileHandler
import os

LOG_FILE = os.path.join(os.getcwd(), "audit.log")

handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5_000_000,   # 5 MB
    backupCount=5
)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

handler.setFormatter(formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[handler]
)

audit_logger = logging.getLogger("audit")