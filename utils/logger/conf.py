import logging

from src.config import DEBUG

LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO


def set_logger():
    logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(relativeCreated)6d %(threadName)s %(message)s')

    logger = logging.getLogger()
    for lgr in ["asyncio", "watchfiles", "urllib3", "logging", "threading", "paramiko", "fastapi", "uvicorn",
                'uvicorn.error', "starlette", "sqlalchemy.engine", "sqlalchemy", "httpx", "celery", "passlib"]:
        logging.getLogger(lgr).setLevel(logging.CRITICAL)

    return logger


LOGGER = set_logger()
