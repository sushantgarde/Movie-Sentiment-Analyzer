"""
app_logger.py
-------------
Shared logging setup for the CineScope / Sentiment_Analyzer project.

Creates a 'logs/' directory at the project root and writes:
    - Console  : INFO and above
    - File     : DEBUG and above  (logs/app_YYYY-MM-DD.log)

Lives in: Sentiment_Analyzer/app_logger.py
"""

import logging
import os
from datetime import datetime

# ── Log directory ─────────────────────────────────────────────────────────────
# __file__ resolves to Sentiment_Analyzer/app_logger.py
# so the logs folder is placed at Sentiment_Analyzer/logs/
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, f"app_{datetime.now().strftime('%Y-%m-%d')}.log")

# ── Format ────────────────────────────────────────────────────────────────────
LOG_FORMAT  = "%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str) -> logging.Logger:
    """
    Return a named logger configured to write to console (INFO+) and
    a daily rotating log file (DEBUG+).

    Calling get_logger() multiple times with the same name is safe —
    handlers are only added once.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # Already configured — avoid duplicate handlers

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # Console handler — INFO and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # File handler — DEBUG and above
    try:
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except OSError as e:
        # If we can't write a log file, console-only is fine
        print(f"[app_logger] WARNING: Could not create log file: {e}")

    logger.addHandler(console_handler)

    return logger