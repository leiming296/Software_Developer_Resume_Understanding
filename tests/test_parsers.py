"""
Unit tests for file parsers (PDFParser and WordParser).
"""

import pytest
from pathlib import Path
from resume_parser.parsers import PDFParser, WordParser


class TestPDFParser:
    """Test cases for PDFParser."""

    def test_pdf_parser_exists(self):
        """Test that PDFParser can be instantiated."""
        parser = PDFParser()
        assert parser is not None

    def test_pdf_parser_parse_nonexistent_file(self):
        """Test that PDFParser raises error for non-existent files."""
        parser = PDFParser()
        with pytest.raises(FileNotFoundError):
            parser.parse("nonexistent_file.pdf")

    def test_pdf_parser_parse_wrong_extension(self):
        """Test that PDFParser raises error for non-PDF files."""
        import tempfile
        import os

        parser = PDFParser()

        # Create a temporary file with wrong extension
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            f.write(b"This is not a PDF file")
            temp_path = f.name

        try:
            with pytest.raises(ValueError):
                parser.parse(temp_path)
        finally:
            os.unlink(temp_path)


class TestWordParser:
    """Test cases for WordParser."""

    def test_word_parser_exists(self):
        """Test that WordParser can be instantiated."""
        parser = WordParser()
        assert parser is not None

    def test_word_parser_parse_nonexistent_file(self):
        """Test that WordParser raises error for non-existent files."""
        parser = WordParser()
        with pytest.raises(FileNotFoundError):
            parser.parse("nonexistent_file.docx")

    def test_word_parser_parse_wrong_extension(self):
        """Test that WordParser raises error for non-Word files."""
        import tempfile
        import os

        parser = WordParser()

        # Create a temporary file with wrong extension
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            f.write(b"This is not a Word document")
            temp_path = f.name

        try:
            with pytest.raises(ValueError):
                parser.parse(temp_path)
        finally:
            os.unlink(temp_path)
