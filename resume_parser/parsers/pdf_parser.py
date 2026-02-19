"""
PDF file parser implementation.
This module provides a concrete implementation of FileParser for PDF files
using the pdfplumber library.
"""

import pdfplumber
from pathlib import Path
from .base import FileParser


class PDFParser(FileParser):
    """
    Concrete implementation of FileParser for PDF files.
    Uses pdfplumber library to extract text from PDF documents.
    Handles multi-page documents and concatenates all text.
    """

    def parse(self, file_path: str) -> str:
        """
        Parse a PDF file and extract its text content.
        Args: file_path: Path to the PDF file
        Returns: Extracted text content from all pages of the PDF
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        if not path.suffix.lower() == '.pdf':
            raise ValueError(f"File is not a PDF: {file_path}")

        try:
            text_content = []

            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)

            # Join all pages with newlines
            full_text = '\n'.join(text_content)

            if not full_text.strip():
                raise ValueError("PDF appears to be empty or contains no extractable text")

            return full_text

        except Exception as e:
            raise Exception(f"Failed to parse PDF file: {str(e)}")
