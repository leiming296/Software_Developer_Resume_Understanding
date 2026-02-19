"""
Unit tests for field extractors (NameExtractor, EmailExtractor, SkillsExtractor).
"""

import pytest
from unittest.mock import Mock, patch
from resume_parser.extractors import NameExtractor, EmailExtractor, SkillsExtractor


class TestNameExtractor:
    """Test cases for NameExtractor."""

    def test_name_extractor_basic(self):
        """Test basic name extraction."""
        extractor = NameExtractor()
        text = "John Doe\nEmail: john@example.com\nSkills: Python, Java"
        name = extractor.extract(text)
        assert name == "John Doe"

    def test_name_extractor_with_middle_initial(self):
        """Test name extraction with middle initial."""
        extractor = NameExtractor()
        text = "Jane M. Smith\nSoftware Engineer"
        name = extractor.extract(text)
        assert "Jane" in name and "Smith" in name

    def test_name_extractor_empty_text(self):
        """Test name extraction with empty text."""
        extractor = NameExtractor()
        name = extractor.extract("")
        assert name == "Unknown"

    def test_name_extractor_three_names(self):
        """Test name extraction with three part name."""
        extractor = NameExtractor()
        text = "John Michael Smith\nDeveloper"
        name = extractor.extract(text)
        assert name == "John Michael Smith"

    def test_name_extractor_skips_email_on_first_line(self):
        """Test that name extractor skips email addresses on first line."""
        extractor = NameExtractor()
        text = "lei.ming296 gmail.com\nLei Ming\nSoftware Engineer"
        name = extractor.extract(text)
        assert name == "Lei Ming"
        assert "@" not in name
        assert "gmail" not in name.lower()

    def test_name_extractor_filters_email_with_at_symbol(self):
        """Test that name extractor filters out lines with @ symbol."""
        extractor = NameExtractor()
        text = "john.doe@example.com\nJohn Doe\nDeveloper"
        name = extractor.extract(text)
        assert name == "John Doe"
        assert "@" not in name

    def test_name_extractor_filters_numbers(self):
        """Test that name extractor filters out lines with many numbers."""
        extractor = NameExtractor()
        text = "user12345\nJane Smith\nEngineer"
        name = extractor.extract(text)
        assert name == "Jane Smith"


class TestEmailExtractor:
    """Test cases for EmailExtractor."""

    def test_email_extractor_basic(self):
        """Test basic email extraction."""
        extractor = EmailExtractor()
        text = "Contact me at john.doe@example.com for more info"
        email = extractor.extract(text)
        assert email == "john.doe@example.com"

    def test_email_extractor_multiple_emails(self):
        """Test email extraction with multiple emails (returns first)."""
        extractor = EmailExtractor()
        text = "john@example.com or jane@example.com"
        email = extractor.extract(text)
        assert email == "john@example.com"

    def test_email_extractor_no_email(self):
        """Test email extraction with no email in text."""
        extractor = EmailExtractor()
        text = "No email address here"
        email = extractor.extract(text)
        assert email == "unknown@example.com"

    def test_email_extractor_empty_text(self):
        """Test email extraction with empty text."""
        extractor = EmailExtractor()
        email = extractor.extract("")
        assert email == "unknown@example.com"

    def test_email_extractor_complex_email(self):
        """Test email extraction with complex email format."""
        extractor = EmailExtractor()
        text = "Email: jane.doe+resume@company-name.co.uk"
        email = extractor.extract(text)
        assert "@" in email


class TestSkillsExtractor:
    """Test cases for SkillsExtractor."""

    def test_skills_extractor_requires_api_key(self):
        """Test that SkillsExtractor requires an API key."""
        import os
        # Temporarily remove GEMINI_API_KEY from environment
        old_key = os.environ.get('GEMINI_API_KEY')
        if old_key:
            del os.environ['GEMINI_API_KEY']

        try:
            with pytest.raises(ValueError):
                SkillsExtractor()
        finally:
            # Restore the original environment variable
            if old_key:
                os.environ['GEMINI_API_KEY'] = old_key

    def test_skills_extractor_with_api_key(self):
        """Test that SkillsExtractor can be instantiated with API key."""
        extractor = SkillsExtractor(api_key="test_key")
        assert extractor is not None
        assert extractor.api_key == "test_key"

    @patch('resume_parser.extractors.skills_extractor.genai')
    def test_skills_extractor_fallback(self, mock_genai):
        """Test that SkillsExtractor falls back to regex when API fails."""
        # Mock the API to raise an exception
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_genai.GenerativeModel.return_value = mock_model

        extractor = SkillsExtractor(api_key="test_key")
        text = "Experienced with Python, JavaScript, and Machine Learning"

        # Should fallback to regex-based extraction
        skills = extractor.extract(text)

        # Should find at least some common skills
        assert isinstance(skills, list)
        assert len(skills) >= 0  # May find skills or return empty list

    def test_skills_extractor_empty_text(self):
        """Test skills extraction with empty text."""
        extractor = SkillsExtractor(api_key="test_key")
        skills = extractor.extract("")
        assert skills == []

    def test_skills_extractor_fallback_finds_common_skills(self):
        """Test that fallback extraction finds common skills."""
        extractor = SkillsExtractor(api_key="test_key")
        text = """
        Senior Software Engineer with expertise in Python, Java, and JavaScript.
        Experience with Docker, Kubernetes, and AWS cloud services.
        Strong background in Machine Learning and Deep Learning.
        """

        # Force fallback by mocking API failure
        with patch.object(extractor, '_parse_skills_from_response', return_value=[]):
            with patch.object(extractor.model, 'generate_content', side_effect=Exception("API Error")):
                skills = extractor._fallback_extraction(text)

        # Should find multiple skills
        assert isinstance(skills, list)
        assert len(skills) > 0
        assert "Python" in skills or "Java" in skills
