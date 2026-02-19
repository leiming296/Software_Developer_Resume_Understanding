"""
Base abstract class for file parsers.
This module defines the FileParser interface that all concrete file parsers
must implement. It follows the Template Method pattern.
"""

from abc import ABC, abstractmethod

class FileParser(ABC):
    """
    Abstract base class for file parsers.
    All concrete file parsers (PDF, Word, etc.) must inherit from this class
    and implement the parse method.
    """
    @abstractmethod
    def parse(self, file_path: str) -> str:
        """
        Parse a file and extract its text content.
        Args: file_path: Path to the file to be parsed
        Returns:Extracted text content from the file
        """
        pass
