import logging
from .settings import LOG_FORMAT, LOG_LEVEL

def setup_logging():
    """
    Configure basic logging format and level.
    """
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT
    )
    logging.info("Logging is configured.")
