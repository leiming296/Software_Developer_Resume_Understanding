"""
Email extractor implementation.

This module provides a regex-based implementation of FieldExtractor for
extracting email addresses from resume text.
"""

import re
from .base import FieldExtractor


class EmailExtractor(FieldExtractor):
    """
    Regex-based extractor for email addresses.

    Strategy: Use standard email regex pattern to find email addresses
    in the resume text. Returns the first valid email found.
    """

    # Standard email regex pattern
    EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    def extract(self, text: str) -> str:
        """
        Extract the candidate's email address from resume text.
        Args:text: Resume text content
        Returns:Extracted email address as a string
        """
        if not text or not text.strip():
            return "unknown@example.com"

        # Search for email pattern in the text
        matches = re.findall(self.EMAIL_PATTERN, text)

        if matches:
            # Return the first email found
            return matches[0]

        # No email found
        return "unknown@example.com"
