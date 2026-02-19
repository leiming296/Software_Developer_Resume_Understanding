"""
File parsers for different document formats.

This package provides concrete implementations of the FileParser interface
for various file formats like PDF and Word documents.
"""

from .base import FileParser
from .pdf_parser import PDFParser
from .word_parser import WordParser

__all__ = [
    "FileParser",
    "PDFParser",
    "WordParser",
]
