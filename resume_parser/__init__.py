"""
Resume Parser Framework

A pluggable framework for extracting structured information from resumes
in multiple file formats (PDF, Word) using configurable extraction strategies.
"""

from .models.resume_data import ResumeData
from .core.framework import ResumeParserFramework
from .core.resume_extractor import ResumeExtractor
from .config import config

__version__ = "1.0.0"
__all__ = [
    "ResumeData",
    "ResumeParserFramework",
    "ResumeExtractor",
    "config",
]
