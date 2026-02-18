"""
Data model for resume information.
This module defines the ResumeData dataclass that encapsulates the extracted resume fields.
"""

import json
from dataclasses import dataclass, asdict
from typing import List


@dataclass
class ResumeData:
    """
    Data class to encapsulate extracted resume information.
    Attributes:name: The candidate's full name, email: The candidate's email address, skills: List of technical skills
    """
    name: str
    email: str
    skills: List[str]
    def to_dict(self) -> dict:
        """
        Convert the ResumeData instance to a dictionary.
        Returns: Dictionary representation of the resume data
        """
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        """
        Convert the ResumeData instance to a JSON string.
        Args:indent: Number of spaces for JSON indentation (default: 2)
        Returns: JSON string representation of the resume data
        """
        return json.dumps(self.to_dict(), indent=indent)

    def __str__(self) -> str:
        """String representation of ResumeData."""
        return self.to_json()

    def __repr__(self) -> str:
        """Developer-friendly representation of ResumeData."""
        return f"ResumeData(name='{self.name}', email='{self.email}', skills={self.skills})"
