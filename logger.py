import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    logger = logging.getLogger("PersonalLibrary")

    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler("app.log", maxBytes=10000, backupCount=5)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(module)s:%(lineno)d - %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)