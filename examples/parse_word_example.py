"""
Example: Parse a Word document resume using the Resume Parser Framework.
This example demonstrates how to:
1. Initialize the file parser for Word documents
2. Configure field extractors with different strategies
3. Create the framework and parse a resume
4. Access the extracted data
"""
from resume_parser.parsers import WordParser
from resume_parser.extractors import NameExtractor, EmailExtractor, SkillsExtractor
from resume_parser.core import ResumeExtractor, ResumeParserFramework
from resume_parser.config import config

def main():
    """Main function to demonstrate Word document resume parsing."""

    # Step 1: Get API key from configuration
    try:
        api_key = config.get_gemini_api_key()
    except ValueError as e:
        print(f"Error: {e}")
        print("GEMINI_API_KEY=your_api_key_here")
        return

    # Step 2: Initialize field extractors with their strategies
    print("Initializing field extractors...")
    extractors = {
        'name': NameExtractor(),           # Regex-based strategy
        'email': EmailExtractor(),         # Regex-based strategy
        'skills': SkillsExtractor(api_key=api_key)  # LLM-based strategy (Gemini)
    }

    # Step 3: Create the file parser for Word documents
    word_parser = WordParser()

    # Step 4: Create the resume extractor coordinator
    resume_extractor = ResumeExtractor(extractors)

    # Step 5: Create the framework by combining parser and extractor
    framework = ResumeParserFramework(word_parser, resume_extractor)

    # Step 6: Parse a Word document resume
    word_file_path = "C:\\Users\\...\\Resumes\\ Resume_2026_ML_AI_new.docx"

    print(f"\nParsing Word resume: {word_file_path}")

    try:
        # Parse the resume and extract structured data
        resume_data = framework.parse_resume(word_file_path)

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
        print(f"\nError: File not found: {word_file_path}")
        print("Please update the word_file_path variable with a valid Word document path.")
    except Exception as e:
        print(f"\nError parsing resume: {str(e)}")


if __name__ == "__main__":
    main()
