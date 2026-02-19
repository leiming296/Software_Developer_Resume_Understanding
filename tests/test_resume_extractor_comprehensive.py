"""
Comprehensive unit tests for ResumeExtractor (coordinator).

This file contains additional test cases beyond the basic tests in test_resume_extractor.py
"""

import pytest
from unittest.mock import Mock
from resume_parser.core import ResumeExtractor
from resume_parser.extractors import NameExtractor, EmailExtractor, SkillsExtractor
from resume_parser.models import ResumeData


class TestResumeExtractorInitializationEdgeCases:
    """Edge case tests for ResumeExtractor initialization."""

    def test_missing_only_name_extractor(self):
        """Test error when only name extractor is missing."""
        extractors = {
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key="test_key")
        }
        with pytest.raises(ValueError) as exc_info:
            ResumeExtractor(extractors)
        assert "name" in str(exc_info.value)

    def test_missing_only_email_extractor(self):
        """Test error when only email extractor is missing."""
        extractors = {
            'name': NameExtractor(),
            'skills': SkillsExtractor(api_key="test_key")
        }
        with pytest.raises(ValueError) as exc_info:
            ResumeExtractor(extractors)
        assert "email" in str(exc_info.value)

    def test_missing_only_skills_extractor(self):
        """Test error when only skills extractor is missing."""
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor()
        }
        with pytest.raises(ValueError) as exc_info:
            ResumeExtractor(extractors)
        assert "skills" in str(exc_info.value)

    def test_with_extra_custom_fields(self):
        """Test initialization with custom additional fields."""
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key="test_key"),
            'phone': Mock(),
            'address': Mock(),
            'education': Mock()
        }
        extractor = ResumeExtractor(extractors)
        assert len(extractor.field_extractors) == 6


class TestResumeExtractorExtractEdgeCases:
    """Edge case tests for extract method."""

    def test_extract_with_whitespace_only_text(self):
        """Test extraction fails with whitespace-only text."""
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key="test_key")
        }
        extractor = ResumeExtractor(extractors)

        with pytest.raises(ValueError):
            extractor.extract("   \n\t\r   ")

    def test_extract_with_special_characters(self):
        """Test extraction with special characters."""
        mock_name = Mock()
        mock_name.extract.return_value = "José García-O'Brien"

        mock_email = Mock()
        mock_email.extract.return_value = "jose.garcia+resume@example.com"

        mock_skills = Mock()
        mock_skills.extract.return_value = ["C++", "C#", ".NET", "Node.js"]

        extractors = {
            'name': mock_name,
            'email': mock_email,
            'skills': mock_skills
        }
        extractor = ResumeExtractor(extractors)

        text = "José García-O'Brien\njose.garcia+resume@example.com"
        result = extractor.extract(text)

        assert result.name == "José García-O'Brien"
        assert result.email == "jose.garcia+resume@example.com"
        assert "C++" in result.skills

    def test_extract_with_unicode_characters(self):
        """Test extraction with Unicode characters (Chinese, Arabic, etc.)."""
        mock_name = Mock()
        mock_name.extract.return_value = "李明 (Lei Ming)"

        mock_email = Mock()
        mock_email.extract.return_value = "leiming@example.com"

        mock_skills = Mock()
        mock_skills.extract.return_value = ["Python", "机器学习"]

        extractors = {
            'name': mock_name,
            'email': mock_email,
            'skills': mock_skills
        }
        extractor = ResumeExtractor(extractors)

        text = "李明\nleiming@example.com\n擅长Python和机器学习"
        result = extractor.extract(text)

        assert "李明" in result.name
        assert "机器学习" in result.skills

    def test_extract_with_very_long_text(self):
        """Test extraction with very long resume text."""
        mock_name = Mock()
        mock_name.extract.return_value = "John Smith"

        mock_email = Mock()
        mock_email.extract.return_value = "john@example.com"

        mock_skills = Mock()
        mock_skills.extract.return_value = ["Python", "Java"]

        extractors = {
            'name': mock_name,
            'email': mock_email,
            'skills': mock_skills
        }
        extractor = ResumeExtractor(extractors)

        # Create very long text (simulate large resume)
        long_text = "John Smith\njohn@example.com\n" + ("Experience description. " * 5000)
        result = extractor.extract(long_text)

        assert result.name == "John Smith"
        mock_name.extract.assert_called_once_with(long_text)

    def test_extract_with_empty_skills_list(self):
        """Test extraction when skills extractor returns empty list."""
        mock_name = Mock()
        mock_name.extract.return_value = "Jane Doe"

        mock_email = Mock()
        mock_email.extract.return_value = "jane@example.com"

        mock_skills = Mock()
        mock_skills.extract.return_value = []

        extractors = {
            'name': mock_name,
            'email': mock_email,
            'skills': mock_skills
        }
        extractor = ResumeExtractor(extractors)

        result = extractor.extract("Some text")

        assert result.skills == []
        assert isinstance(result.skills, list)

    def test_extract_calls_all_extractors(self):
        """Test that extract calls all three required extractors."""
        mock_name = Mock()
        mock_name.extract.return_value = "John Doe"

        mock_email = Mock()
        mock_email.extract.return_value = "john@example.com"

        mock_skills = Mock()
        mock_skills.extract.return_value = ["Python"]

        extractors = {
            'name': mock_name,
            'email': mock_email,
            'skills': mock_skills
        }
        extractor = ResumeExtractor(extractors)

        text = "Test resume text"
        extractor.extract(text)

        # Verify each extractor was called with the text
        mock_name.extract.assert_called_once_with(text)
        mock_email.extract.assert_called_once_with(text)
        mock_skills.extract.assert_called_once_with(text)


class TestResumeExtractorErrorHandling:
    """Test error handling scenarios."""

    def test_extract_when_name_extractor_fails(self):
        """Test extraction failure when name extractor throws error."""
        mock_name = Mock()
        mock_name.extract.side_effect = Exception("Name extraction failed")

        mock_email = Mock()
        mock_email.extract.return_value = "jane@example.com"

        mock_skills = Mock()
        mock_skills.extract.return_value = ["Python"]

        extractors = {
            'name': mock_name,
            'email': mock_email,
            'skills': mock_skills
        }
        extractor = ResumeExtractor(extractors)

        with pytest.raises(Exception) as exc_info:
            extractor.extract("Some text")
        assert "Failed to extract resume data" in str(exc_info.value)

    def test_extract_when_email_extractor_fails(self):
        """Test extraction failure when email extractor throws error."""
        mock_name = Mock()
        mock_name.extract.return_value = "Jane Doe"

        mock_email = Mock()
        mock_email.extract.side_effect = RuntimeError("Email API timeout")

        mock_skills = Mock()
        mock_skills.extract.return_value = ["Python"]

        extractors = {
            'name': mock_name,
            'email': mock_email,
            'skills': mock_skills
        }
        extractor = ResumeExtractor(extractors)

        with pytest.raises(Exception) as exc_info:
            extractor.extract("Some text")
        assert "Failed to extract resume data" in str(exc_info.value)

    def test_extract_when_skills_extractor_fails(self):
        """Test extraction failure when skills extractor throws error."""
        mock_name = Mock()
        mock_name.extract.return_value = "Jane Doe"

        mock_email = Mock()
        mock_email.extract.return_value = "jane@example.com"

        mock_skills = Mock()
        mock_skills.extract.side_effect = ValueError("Invalid skills format")

        extractors = {
            'name': mock_name,
            'email': mock_email,
            'skills': mock_skills
        }
        extractor = ResumeExtractor(extractors)

        with pytest.raises(Exception) as exc_info:
            extractor.extract("Some text")
        assert "Failed to extract resume data" in str(exc_info.value)

    def test_extract_when_multiple_extractors_fail(self):
        """Test extraction failure when multiple extractors fail."""
        mock_name = Mock()
        mock_name.extract.side_effect = Exception("Failed")

        mock_email = Mock()
        mock_email.extract.side_effect = Exception("Failed")

        mock_skills = Mock()
        mock_skills.extract.return_value = ["Python"]

        extractors = {
            'name': mock_name,
            'email': mock_email,
            'skills': mock_skills
        }
        extractor = ResumeExtractor(extractors)

        with pytest.raises(Exception):
            extractor.extract("Some text")


class TestResumeExtractorDynamicConfiguration:
    """Test dynamic extractor configuration."""

    def test_add_new_custom_extractor(self):
        """Test adding a new custom field extractor."""
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key="test_key")
        }
        extractor = ResumeExtractor(extractors)

        phone_extractor = Mock()
        extractor.add_extractor('phone', phone_extractor)

        assert extractor.get_extractor('phone') == phone_extractor
        assert len(extractor.field_extractors) == 4

    def test_update_existing_extractor(self):
        """Test replacing an existing extractor."""
        old_name = NameExtractor()
        extractors = {
            'name': old_name,
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key="test_key")
        }
        extractor = ResumeExtractor(extractors)

        new_name = NameExtractor()
        extractor.add_extractor('name', new_name)

        assert extractor.get_extractor('name') != old_name
        assert extractor.get_extractor('name') == new_name

    def test_remove_custom_extractor(self):
        """Test removing a custom (non-required) extractor."""
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key="test_key"),
            'phone': Mock()
        }
        extractor = ResumeExtractor(extractors)

        extractor.remove_extractor('phone')

        with pytest.raises(KeyError):
            extractor.get_extractor('phone')

    def test_remove_nonexistent_extractor(self):
        """Test that removing non-existent extractor raises KeyError."""
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key="test_key")
        }
        extractor = ResumeExtractor(extractors)

        with pytest.raises(KeyError) as exc_info:
            extractor.remove_extractor('nonexistent')
        assert "not found" in str(exc_info.value)

    def test_get_nonexistent_extractor(self):
        """Test that getting non-existent extractor raises KeyError."""
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key="test_key")
        }
        extractor = ResumeExtractor(extractors)

        with pytest.raises(KeyError) as exc_info:
            extractor.get_extractor('address')
        assert "not found" in str(exc_info.value)


class TestResumeExtractorIntegration:
    """Integration tests for complete workflows."""

    def test_full_extraction_workflow(self):
        """Test complete workflow from initialization to extraction."""
        # Setup mock extractors
        mock_name = Mock()
        mock_name.extract.return_value = "Alice Johnson"

        mock_email = Mock()
        mock_email.extract.return_value = "alice.johnson@example.com"

        mock_skills = Mock()
        mock_skills.extract.return_value = ["Python", "Docker", "AWS"]

        extractors = {
            'name': mock_name,
            'email': mock_email,
            'skills': mock_skills
        }
        extractor = ResumeExtractor(extractors)

        # Perform extraction
        text = """
        Alice Johnson
        Senior Software Engineer

        Email: alice.johnson@example.com

        Technical Skills:
        - Python, Docker, AWS
        - Machine Learning, Data Science
        """

        result = extractor.extract(text)

        # Verify results
        assert isinstance(result, ResumeData)
        assert result.name == "Alice Johnson"
        assert result.email == "alice.johnson@example.com"
        assert result.skills == ["Python", "Docker", "AWS"]

    def test_workflow_with_extractor_replacement(self):
        """Test workflow with dynamic extractor replacement."""
        # Initial setup
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key="test_key")
        }
        extractor = ResumeExtractor(extractors)

        # Replace with mock extractors
        mock_name = Mock()
        mock_name.extract.return_value = "Bob Smith"
        extractor.add_extractor('name', mock_name)

        mock_email = Mock()
        mock_email.extract.return_value = "bob@example.com"
        extractor.add_extractor('email', mock_email)

        mock_skills = Mock()
        mock_skills.extract.return_value = ["Java", "Spring"]
        extractor.add_extractor('skills', mock_skills)

        # Extract
        result = extractor.extract("Test resume")

        # Verify
        assert result.name == "Bob Smith"
        assert result.email == "bob@example.com"
        assert result.skills == ["Java", "Spring"]

    def test_workflow_with_additional_fields(self):
        """Test workflow with additional custom fields."""
        mock_name = Mock()
        mock_name.extract.return_value = "Carol White"

        mock_email = Mock()
        mock_email.extract.return_value = "carol@example.com"

        mock_skills = Mock()
        mock_skills.extract.return_value = ["Python"]

        mock_phone = Mock()
        mock_phone.extract.return_value = "+1-555-0123"

        extractors = {
            'name': mock_name,
            'email': mock_email,
            'skills': mock_skills,
            'phone': mock_phone
        }
        extractor = ResumeExtractor(extractors)

        # Extract required fields
        result = extractor.extract("Resume text")

        # Verify required fields
        assert result.name == "Carol White"
        assert result.email == "carol@example.com"
        assert result.skills == ["Python"]

        # Verify custom extractor exists
        assert extractor.get_extractor('phone') == mock_phone


class TestResumeExtractorResumeDataCreation:
    """Test ResumeData object creation."""

    def test_resume_data_structure(self):
        """Test that extracted data creates proper ResumeData structure."""
        mock_name = Mock()
        mock_name.extract.return_value = "Test Name"

        mock_email = Mock()
        mock_email.extract.return_value = "test@example.com"

        mock_skills = Mock()
        mock_skills.extract.return_value = ["Skill1", "Skill2", "Skill3"]

        extractors = {
            'name': mock_name,
            'email': mock_email,
            'skills': mock_skills
        }
        extractor = ResumeExtractor(extractors)

        result = extractor.extract("Test text")

        assert isinstance(result, ResumeData)
        assert hasattr(result, 'name')
        assert hasattr(result, 'email')
        assert hasattr(result, 'skills')
        assert result.name == "Test Name"
        assert result.email == "test@example.com"
        assert result.skills == ["Skill1", "Skill2", "Skill3"]

    def test_resume_data_with_empty_skills(self):
        """Test ResumeData creation when skills list is empty."""
        mock_name = Mock()
        mock_name.extract.return_value = "Test Name"

        mock_email = Mock()
        mock_email.extract.return_value = "test@example.com"

        mock_skills = Mock()
        mock_skills.extract.return_value = []

        extractors = {
            'name': mock_name,
            'email': mock_email,
            'skills': mock_skills
        }
        extractor = ResumeExtractor(extractors)

        result = extractor.extract("Test text")

        assert isinstance(result, ResumeData)
        assert result.skills == []
        assert isinstance(result.skills, list)
