"""Playwright automation package"""
from src.base import BasePage, BaseTest
from src.utils import WaitUtils, FileUtils, StringUtils

__version__ = "1.0.0"
__all__ = [
    "BasePage",
    "BaseTest",
    "WaitUtils",
    "FileUtils",
    "StringUtils",
]
