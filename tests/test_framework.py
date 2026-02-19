"""
Unit tests for ResumeParserFramework (main orchestrator).
"""

import pytest
from unittest.mock import Mock, patch
from resume_parser.core import ResumeParserFramework, ResumeExtractor
from resume_parser.parsers import PDFParser, WordParser
from resume_parser.extractors import NameExtractor, EmailExtractor, SkillsExtractor
from resume_parser.models import ResumeData


class TestResumeParserFramework:
    """Test cases for ResumeParserFramework."""

    def test_framework_initialization(self):
        """Test that framework can be initialized."""
        parser = PDFParser()
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key="test_key")
        }
        extractor = ResumeExtractor(extractors)
        framework = ResumeParserFramework(parser, extractor)

        assert framework is not None
        assert framework.file_parser == parser
        assert framework.resume_extractor == extractor


    def test_framework_parse_nonexistent_file(self):
        """Test that framework raises error for non-existent files."""
        parser = PDFParser()
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key="test_key")
        }
        extractor = ResumeExtractor(extractors)
        framework = ResumeParserFramework(parser, extractor)

        with pytest.raises(FileNotFoundError):
            framework.parse_resume("nonexistent.pdf")


    def test_framework_set_parser(self):
        """Test setting a new parser."""
        parser = PDFParser()
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key="test_key")
        }
        extractor = ResumeExtractor(extractors)
        framework = ResumeParserFramework(parser, extractor)

        new_parser = WordParser()
        framework.set_parser(new_parser)

        assert framework.file_parser == new_parser


    def test_framework_set_extractor(self):
        """Test setting a new extractor."""
        parser = PDFParser()
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key="test_key")
        }
        extractor = ResumeExtractor(extractors)
        framework = ResumeParserFramework(parser, extractor)

        new_extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key="new_key")
        }
        new_extractor = ResumeExtractor(new_extractors)
        framework.set_extractor(new_extractor)

        assert framework.resume_extractor == new_extractor


    @patch('resume_parser.parsers.pdf_parser.pdfplumber')
    def test_framework_parse_resume_mocked(self, mock_pdfplumber):
        """Test framework with mocked PDF parser."""
        # Mock PDF parsing
        mock_pdf = Mock()
        mock_page = Mock()
        mock_page.extract_text.return_value = """
        Jane Doe
        jane.doe@example.com
        Skills: Python, Machine Learning, Docker
        """
        mock_pdf.pages = [mock_page]
        mock_pdfplumber.open.return_value.__enter__.return_value = mock_pdf

        # Create framework
        parser = PDFParser()
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key="test_key")
        }

        # Mock skills extractor to avoid API call
        mock_skills = Mock()
        mock_skills.extract.return_value = ["Python", "Machine Learning", "Docker"]
        extractors['skills'] = mock_skills

        extractor = ResumeExtractor(extractors)
        framework = ResumeParserFramework(parser, extractor)

        # Create a temporary file to test with
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            temp_path = f.name

        try:
            result = framework.parse_resume(temp_path)

            assert isinstance(result, ResumeData)
            assert result.name == "Jane Doe"
            assert result.email == "jane.doe@example.com"
            assert isinstance(result.skills, list)
            assert len(result.skills) > 0
        finally:
            import os
            os.unlink(temp_path)
