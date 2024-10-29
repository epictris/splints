import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logfile = os.getenv("SPLINTS_LOGS")
if logfile is not None:
    logger.addHandler(logging.FileHandler(logfile))
