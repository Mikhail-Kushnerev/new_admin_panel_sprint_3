import logging
from logging.handlers import RotatingFileHandler


from utils import LOGS_FORMAT


def logger():
    rotating_handler: RotatingFileHandler = RotatingFileHandler(
        'config/logs.log', maxBytes=pow(10, 6), backupCount=5
    )
    logging.basicConfig(
        level=logging.INFO,
        encoding='utf-8',
        format=LOGS_FORMAT,
        handlers=(rotating_handler, logging.StreamHandler())
    )
    logger = logging.getLogger(__file__)
    return logger

