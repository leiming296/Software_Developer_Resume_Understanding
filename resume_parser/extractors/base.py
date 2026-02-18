"""
Base abstract class for field extractors.

This module defines the FieldExtractor interface that all concrete field
extractors must implement. It follows the Strategy pattern.
"""

from abc import ABC, abstractmethod
from typing import Any


class FieldExtractor(ABC):
    """
    Abstract base class for field extractors.

    All concrete field extractors (Name, Email, Skills) must inherit from
    this class and implement the extract method. This allows for different
    extraction strategies (regex, NER, LLM-based, etc.) to be used
    interchangeably.
    """

    @abstractmethod
    def extract(self, text: str) -> Any:
        """
        Extract a specific field from the given text.
        Args:text: The text content to extract information from
        Returns:The extracted field value (type depends on the specific extractor)
        """
        pass
