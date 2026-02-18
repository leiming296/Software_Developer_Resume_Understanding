"""
Resume parser framework orchestration.
This module provides the main ResumeParserFramework class that combines
file parsing and field extraction into a single, easy-to-use interface.
"""

from pathlib import Path
from ..parsers.base import FileParser
from .resume_extractor import ResumeExtractor
from ..models.resume_data import ResumeData


class ResumeParserFramework:
    """
    Main framework class that orchestrates resume parsing.
    This class combines a FileParser and a ResumeExtractor to provide
    a simple, unified interface for parsing resumes of different formats.
    It follows the Facade pattern to simplify the complex subsystem.
    """

    def __init__(self, file_parser: FileParser, resume_extractor: ResumeExtractor):
        """
        Initialize the framework with a parser and extractor.
        Args: file_parser: FileParser instance for parsing files
            resume_extractor: ResumeExtractor instance for extracting fields
        """
        self.file_parser = file_parser
        self.resume_extractor = resume_extractor

    def parse_resume(self, file_path: str) -> ResumeData:
        """
        Parse a resume file and extract structured information.
         This is the main entry point for the framework. It handles the
        entire pipeline: file parsing -> text extraction -> field extraction.

        Args: file_path: Path to the resume file (PDF or Word document)
        Returns: ResumeData instance with extracted information
        """

        # Validate file exists
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Resume file not found: {file_path}")

        # Parse the file to extract text
        try:
            text = self.file_parser.parse(file_path)
        except Exception as e:
            raise Exception(f"Failed to parse file: {str(e)}")

        # Extract structured information from text
        try:
            resume_data = self.resume_extractor.extract(text)
        except Exception as e:
            raise Exception(f"Failed to extract resume data: {str(e)}")

        return resume_data

    def set_parser(self, file_parser: FileParser) -> None:
        """
        Update the file parser.
        Allows switching between different file parsers at runtime.
        Args: file_parser: New FileParser instance
        """
        self.file_parser = file_parser

    def set_extractor(self, resume_extractor: ResumeExtractor) -> None:
        """
        Update the resume extractor.
        Allows switching between different extraction strategies at runtime.
        Args:resume_extractor: New ResumeExtractor instance
        """
        self.resume_extractor = resume_extractor
