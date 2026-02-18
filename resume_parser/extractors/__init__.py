"""
Field extractors for different resume fields.
This package provides concrete implementations of the FieldExtractor interface
using various extraction strategies (regex, LLM-based, etc.).
"""

from .base import FieldExtractor
from .name_extractor import NameExtractor
from .email_extractor import EmailExtractor
from .skills_extractor import SkillsExtractor

__all__ = [
    "FieldExtractor",
    "NameExtractor",
    "EmailExtractor",
    "SkillsExtractor",
]
