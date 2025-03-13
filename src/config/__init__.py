"""
EthicGuard configuration and utilities.
"""
from .settings import *
from .setup import setup_logging

__all__ = [
    'THRESHOLDS', 'REQUIRED_SECTIONS', 'UI_ELEMENTS', 
    'APP_NAME', 'LOG_FORMAT', 'setup_logging'
]
