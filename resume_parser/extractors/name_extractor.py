"""
Name extractor implementation.

This module provides a regex-based implementation of FieldExtractor for
extracting names from resume text.
"""

import re
from .base import FieldExtractor


class NameExtractor(FieldExtractor):
    """
    Regex-based extractor for candidate names.  Extract name from the first few lines of the resume.
    Most resumes start with the candidate's name in the header. Uses regex patterns to identify capitalized name patterns.
    """
    def extract(self, text: str) -> str:
        """
        Extract the candidate's name from resume text.
        Args:text: Resume text content
        Returns:Extracted name as a string
        """
        if not text or not text.strip():return "Unknown"

        # Split text into lines and get first few non-empty lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        if not lines: return "Unknown"

        # Try to find a name in the first 5 lines
        for line in lines[:5]:
            # Pattern: 2-4 capitalized words (typical name pattern)
            # Matches: "John Doe", "Jane Mary Smith", etc.
            name_pattern = r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})$'
            match = re.match(name_pattern, line)

            if match:return match.group(1)

            # Alternative pattern: Words with capital letters (handles middle initials)
            # Matches: "John D. Doe", "Jane M Smith", etc.
            alt_pattern = r'^([A-Z][a-z]+(?:\s+[A-Z]\.?\s*)?(?:\s+[A-Z][a-z]+)+)$'
            match = re.match(alt_pattern, line)

            if match: return match.group(1)

        # Fallback: return the first non-empty line if no pattern matches
        # Many resumes start with the name even if it doesn't match patterns
        first_line = lines[0]

        # Filter out email-like patterns (contains @ or looks like email)
        email_pattern = r'[@]|[a-zA-Z0-9._%+-]+\s*(gmail|yahoo|hotmail|outlook|mail|email)'
        if re.search(email_pattern, first_line, re.IGNORECASE):
            # Skip this line, try the next line
            if len(lines) > 1:
                first_line = lines[1]
            else:
                return "Unknown"

        # Clean up common non-name artifacts
        first_line = re.sub(r'[^\w\s\.]', ' ', first_line)
        first_line = ' '.join(first_line.split())

        # Filter out lines with too many numbers or dots (likely email/phone)
        if re.search(r'\d{3,}|\..*\.', first_line):
            return "Unknown"

        # If the first line is too long (> 50 chars), it's probably not a name
        if len(first_line) <= 50 and len(first_line) > 0:
            return first_line

        return "Unknown"
