"""
CloudMind AI - Open Source Cloud Resource Management Platform

Automated management and optimization of cloud resources across
AWS, Azure, Google Cloud, and on-premises infrastructure using AI.
"""

__version__ = "0.1.0"
__author__ = "CloudMind AI Contributors"
__license__ = "MIT"

from .core.config import settings
from .core.logger import logger

__all__ = ["settings", "logger", "__version__"]
