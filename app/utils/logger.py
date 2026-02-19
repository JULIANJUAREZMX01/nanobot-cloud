"""Logging configuration"""

import sys
from loguru import logger as _logger


def get_logger(name: str = "nanobot"):
    """Get configured logger instance"""
    _logger.remove()
    _logger.add(
        sys.stdout,
        format="<level>{level: <8}</level> | {name}:{function}:{line} - <level>{message}</level>",
        level="INFO"
    )
    return _logger
