import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = 'logs'
LOG_FILE = 'app.log'
os.makedirs(LOG_DIR, exist_ok=True) 

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)


    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        file_handler = RotatingFileHandler(
            os.path.join(LOG_DIR, LOG_FILE),
            maxBytes=5 * 1024 * 1024,
            backupCount=3
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
