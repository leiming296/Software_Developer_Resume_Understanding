"""
Example: Parse a PDF resume using the Resume Parser Framework.

This example demonstrates how to:
1. Initialize the file parser for PDF documents
2. Configure field extractors with different strategies
3. Create the framework and parse a resume
4. Access the extracted data
"""

from resume_parser.parsers import PDFParser
from resume_parser.extractors import NameExtractor, EmailExtractor, SkillsExtractor
from resume_parser.core import ResumeExtractor, ResumeParserFramework
from resume_parser.config import config


def main():
    """Main function to demonstrate PDF resume parsing."""
    # Step 1: Get API key from configuration
    # Make sure to set GEMINI_API_KEY in your .env file
    try:
        api_key = config.get_gemini_api_key()
    except ValueError as e:
        print(f"Error: {e}")
        print("GEMINI_API_KEY=your_api_key_here")
        return

    # Step 2: Initialize field extractors with their strategies
    extractors = {
        'name': NameExtractor(),           # Regex-based strategy
        'email': EmailExtractor(),         # Regex-based strategy
        'skills': SkillsExtractor(api_key=api_key)  # LLM-based strategy (Gemini)
    }

    # Step 3: Create the file parser for PDF documents
    pdf_parser = PDFParser()

    # Step 4: Create the resume extractor coordinator
    resume_extractor = ResumeExtractor(extractors)

    # Step 5: Create the framework by combining parser and extractor
    framework = ResumeParserFramework(pdf_parser, resume_extractor)

    # Step 6: Parse a PDF resume
    # Replace with the actual path to your PDF resume
    pdf_file_path = "C:\\Users\\Lei_Ming\\Interviews\\2026\\Resumes\\Ming Lei - Resume_2026_ML_AI_new.pdf"
    print(f"\nParsing PDF resume: {pdf_file_path}")

    try:
        # Parse the resume and extract structured data
        resume_data = framework.parse_resume(pdf_file_path)

        # Step 7: Access the extracted data
        print("\n" + "="*60)
        print("EXTRACTED RESUME DATA")
        print("="*60)

        print(f"\nName: {resume_data.name}")
        print(f"Email: {resume_data.email}")
        print(f"Skills: {', '.join(resume_data.skills)}")

        # Step 8: Output as JSON
        print("\n" + "="*60)
        print("JSON OUTPUT")
        print("="*60)
        print(resume_data.to_json())

        # Step 9: Output as dictionary
        print("\n" + "="*60)
        print("DICTIONARY OUTPUT")
        print("="*60)
        print(resume_data.to_dict())

    except FileNotFoundError:
        print(f"\nError: File not found: {pdf_file_path}")
        print("Please update the pdf_file_path variable with a valid PDF resume path.")
    except Exception as e:
        print(f"\nError parsing resume: {str(e)}")


if __name__ == "__main__":
    main()
