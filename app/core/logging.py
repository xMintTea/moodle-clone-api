from loguru import logger
from sys import stderr

logger.add(stderr, level="INFO")