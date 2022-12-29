import logging

from utils.constants import LOGS_FORMAT


def get_logger():
    logging.basicConfig(
        level=logging.INFO,
        encoding='utf-8',
        format=LOGS_FORMAT,
        # handlers=(logging.StreamHandler(),)
    )
    logger = logging.getLogger(__file__)
    return logger
