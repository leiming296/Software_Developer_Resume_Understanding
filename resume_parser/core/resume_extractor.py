"""
Resume extraction coordinator.

This module provides the ResumeExtractor class that orchestrates the extraction
of all fields from resume text using field-specific extractors.
"""

from typing import Dict
from ..extractors.base import FieldExtractor
from ..models.resume_data import ResumeData


class ResumeExtractor:
    """
    Coordinator class that orchestrates field extraction.
    This class takes a dictionary of field extractors and uses them to
    extract structured information from resume text. It follows the
    Coordinator pattern to manage multiple extraction strategies.
    """

    def __init__(self, field_extractors: Dict[str, FieldExtractor]):
        """
        Initialize the ResumeExtractor with field-specific extractors.
        Args: field_extractors: Dictionary mapping field names to their extractors
        Expected keys: 'name', 'email', 'skills'
        """
        required_fields = {'name', 'email', 'skills'}
        provided_fields = set(field_extractors.keys())

        if not required_fields.issubset(provided_fields):
            missing = required_fields - provided_fields
            raise ValueError(f"Missing required field extractors: {missing}")

        self.field_extractors = field_extractors

    def extract(self, text: str) -> ResumeData:
        """
        Extract all fields from resume text and create a ResumeData instance.
        Args:text: Resume text content to extract information from
        Returns:ResumeData instance with extracted information
        """
        if not text or not text.strip():
            raise ValueError("Cannot extract from empty text")

        try:
            # Extract each field using its corresponding extractor
            name = self.field_extractors['name'].extract(text)
            email = self.field_extractors['email'].extract(text)
            skills = self.field_extractors['skills'].extract(text)

            # Create and return ResumeData instance
            return ResumeData(
                name=name,
                email=email,
                skills=skills
            )

        except Exception as e:
            raise Exception(f"Failed to extract resume data: {str(e)}")

    def add_extractor(self, field_name: str, extractor: FieldExtractor) -> None:
        """
        Add or update a field extractor. This allows for dynamic configuration of extraction strategies.
        Args:
            field_name: Name of the field (e.g., 'name', 'email', 'skills')
            extractor: FieldExtractor instance for this field
        """
        self.field_extractors[field_name] = extractor

    def remove_extractor(self, field_name: str) -> None:
        """
        Remove a field extractor.
        Args: field_name: Name of the field to remove
        """
        if field_name in self.field_extractors:
            del self.field_extractors[field_name]
        else:
            raise KeyError(f"Field extractor '{field_name}' not found")

    def get_extractor(self, field_name: str) -> FieldExtractor:
        """
        Get a specific field extractor.
        Args: field_name: Name of the field
        Returns:FieldExtractor instance for the specified field
        """
        if field_name in self.field_extractors:
            return self.field_extractors[field_name]
        else:
            raise KeyError(f"Field extractor '{field_name}' not found")
