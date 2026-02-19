"""
Example: Advanced usage of the Resume Parser Framework.

This example demonstrates:
1. Dynamic parser switching based on file extension
2. Custom extractor configuration
3. Error handling and validation
4. Processing multiple resumes
"""

import os
from pathlib import Path
from typing import List, Dict
from resume_parser.parsers import PDFParser, WordParser
from resume_parser.extractors import NameExtractor, EmailExtractor, SkillsExtractor
from resume_parser.core import ResumeExtractor, ResumeParserFramework
from resume_parser.models import ResumeData
from resume_parser.config import config


class ResumeParserFactory:
    """Factory class to create appropriate parser based on file type."""

    @staticmethod
    def create_framework(api_key: str) -> Dict[str, ResumeParserFramework]:
        """
        Create framework instances for different file types.
        Args:api_key: Gemini API key for skills extraction
        Returns:Dictionary mapping file extensions to framework instances
        """
        # Create extractors (shared across all parsers)
        extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key=api_key)
        }

        # Create PDF framework
        pdf_extractor = ResumeExtractor(extractors.copy())
        pdf_framework = ResumeParserFramework(PDFParser(), pdf_extractor)

        # Create Word framework
        word_extractors = {
            'name': NameExtractor(),
            'email': EmailExtractor(),
            'skills': SkillsExtractor(api_key=api_key)
        }
        word_extractor = ResumeExtractor(word_extractors)
        word_framework = ResumeParserFramework(WordParser(), word_extractor)

        return {
            '.pdf': pdf_framework,
            '.docx': word_framework,
            '.doc': word_framework
        }


def parse_resume_auto(file_path: str, frameworks: Dict[str, ResumeParserFramework]) -> ResumeData:
    """
    Automatically parse a resume using the appropriate parser based on file extension.
    Args: file_path: Path to the resume file, frameworks: Dictionary of framework instances
    Returns: ResumeData instance with extracted information
    """
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension not in frameworks:
        raise ValueError(f"Unsupported file type: {extension}. Supported types: {list(frameworks.keys())}")

    framework = frameworks[extension]
    return framework.parse_resume(file_path)


def process_resume_directory(directory: str, frameworks: Dict[str, ResumeParserFramework]) -> List[Dict]:
    """
    Process all resume files in a directory.
    Args:directory: Path to directory containing resume files, frameworks: Dictionary of framework instances
    Returns: List of dictionaries with resume data and metadata
    """
    results = []
    supported_extensions = {'.pdf', '.docx', '.doc'}

    dir_path = Path(directory)
    if not dir_path.exists():
        print(f"Directory not found: {directory}")
        return results

    for file_path in dir_path.iterdir():
        if file_path.suffix.lower() in supported_extensions:
            try:
                print(f"Processing: {file_path.name}...")
                resume_data = parse_resume_auto(str(file_path), frameworks)

                results.append({
                    'file_name': file_path.name,
                    'file_path': str(file_path),
                    'status': 'success',
                    'data': resume_data.to_dict()
                })

                print(f"  ✓ Successfully parsed {file_path.name}")

            except Exception as e:
                print(f"  ✗ Error parsing {file_path.name}: {str(e)}")
                results.append({
                    'file_name': file_path.name,
                    'file_path': str(file_path),
                    'status': 'error',
                    'error': str(e)
                })

    return results


def main():
    """Main function demonstrating advanced usage."""
    # Get API key
    try:
        api_key = config.get_gemini_api_key()
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Create framework instances
    print("Initializing framework instances...")
    frameworks = ResumeParserFactory.create_framework(api_key)

    print("\n" + "="*60)
    print("EXAMPLE 1: Parse Single Resume with Auto-Detection")
    print("="*60)

    # Parse a single resume (auto-detect file type)
    # resume_file = "path/to/resume.pdf"  # or .docx
    resume_file = "C:\\Users\\...\\Resumes\\Resume_2026_ML_AI_new.pdf"

    try:
        resume_data = parse_resume_auto(resume_file, frameworks)
        print(f"\nName: {resume_data.name}")
        print(f"Email: {resume_data.email}")
        print(f"Skills: {', '.join(resume_data.skills)}")
    except FileNotFoundError:
        print(f"\nFile not found: {resume_file}")
        print("Update the resume_file variable with a valid path.")
    except Exception as e:
        print(f"\nError: {str(e)}")

    print("\n" + "="*60)
    print("EXAMPLE 2: Process Multiple Resumes from Directory")
    print("="*60)

    # Process all resumes in a directory
    resume_directory = "C:\\Users\\...\\2026\\Resumes"

    results = process_resume_directory(resume_directory, frameworks)

    print(f"\n\nProcessed {len(results)} resumes")
    print(f"Successful: {sum(1 for r in results if r['status'] == 'success')}")
    print(f"Failed: {sum(1 for r in results if r['status'] == 'error')}")

    # Show summary of successful parses
    successful_results = [r for r in results if r['status'] == 'success']
    if successful_results:
        print("\n" + "="*60)
        print("SUCCESSFUL PARSES")
        print("="*60)
        for result in successful_results:
            data = result['data']
            print(f"\nFile: {result['file_name']}")
            print(f"  Name: {data['name']}")
            print(f"  Email: {data['email']}")
            print(f"  Skills: {', '.join(data['skills'][:5])}...")  # Show first 5 skills


if __name__ == "__main__":
    main()
