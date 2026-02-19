"""
Unit tests for ResumeExtractor (coordinator).
"""

import pytest
from resume_parser.core import ResumeExtractor
from resume_parser.extractors import NameExtractor, EmailExtractor, SkillsExtractor
from resume_parser.models import ResumeData


class TestResumeExtractor:
    """Test cases for ResumeExtractor."""

    def test_resume_extractor_requires_all_fields(self):
        """Test that ResumeExtractor requires all three extractors."""
        with pytest.raises(ValueError):
            ResumeExtractor({})

        with pytest.raises(ValueError):
            ResumeExtractor({'name': NameExtractor()})

    def test_resume_extractor_initialization(self):
        """Test that ResumeExtractor can be initialized with all extractors."""
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key="test_key")
        }
        extractor = ResumeExtractor(extractors)
        assert extractor is not None

    def test_resume_extractor_extract(self):
        """Test basic extraction with all fields."""
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key="test_key")
        }
        extractor = ResumeExtractor(extractors)

        text = """
        Jane Doe
        Email: jane.doe@example.com
        Skills: Python, JavaScript, Machine Learning, Docker
        """

        # Mock the skills extractor to avoid API call
        with pytest.MonkeyPatch.context() as m:
            m.setattr(extractors['skills'], 'extract', lambda x: ["Python", "JavaScript", "Machine Learning"])
            result = extractor.extract(text)

        assert isinstance(result, ResumeData)
        assert result.name == "Jane Doe"
        assert result.email == "jane.doe@example.com"
        assert isinstance(result.skills, list)

    def test_resume_extractor_empty_text(self):
        """Test that extractor raises error on empty text."""
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key="test_key")
        }
        extractor = ResumeExtractor(extractors)

        with pytest.raises(ValueError):
            extractor.extract("")

    def test_resume_extractor_add_extractor(self):
        """Test adding a new extractor."""
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key="test_key")
        }
        extractor = ResumeExtractor(extractors)

        # Add a new extractor
        new_name_extractor = NameExtractor()
        extractor.add_extractor('name', new_name_extractor)

        assert extractor.get_extractor('name') == new_name_extractor

    def test_resume_extractor_remove_extractor(self):
        """Test removing an extractor."""
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key="test_key"),
            'extra': NameExtractor()
        }
        extractor = ResumeExtractor(extractors)
        extractor.remove_extractor('extra')
        with pytest.raises(KeyError):
            extractor.get_extractor('extra')
