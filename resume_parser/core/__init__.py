"""
Core framework components.

This package contains the main orchestration classes that coordinate
file parsing and field extraction.
"""

from .resume_extractor import ResumeExtractor
from .framework import ResumeParserFramework

__all__ = [
    "ResumeExtractor",
    "ResumeParserFramework",
]
