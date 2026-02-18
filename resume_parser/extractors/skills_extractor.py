"""
Skills extractor implementation.  This module provides an LLM-based implementation of FieldExtractor for
extracting technical skills from resume text using Google Gemini API.
"""
import os
import re
import json
from typing import List, Optional
from .base import FieldExtractor
try:
    import google.generativeai as genai
except ImportError:
    genai = None


class SkillsExtractor(FieldExtractor):
    """
    LLM-based extractor for technical skills using Google Gemini API.

    Strategy: Use Gemini's language understanding to identify and extract
    technical skills from resume text. This approach handles various skill
    formats, abbreviations, and context better than regex.
    """

    # def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-1.5-flash"):
    #     """
    #     Initialize the SkillsExtractor with Gemini API credentials.
    #
    #     Args:
    #         api_key: Google Gemini API key (if None, will try to load from config)
    #         model_name: Gemini model to use (default: gemini-pro)
    #
    #     Raises:
    #         ImportError: If google-generativeai is not installed
    #         ValueError: If API key is not provided
    #     """
    #     if genai is None:
    #         raise ImportError(
    #             "google-generativeai library is not installed. "
    #             "Install it with: pip install google-generativeai"
    #         )
    #
    #     if not api_key:
    #         raise ValueError(
    #             "API key is required for SkillsExtractor. "
    #             "Provide it via the api_key parameter or set GEMINI_API_KEY environment variable."
    #         )
    #
    #     self.api_key = api_key
    #     self.model_name = model_name
    #
    #     # Configure Gemini API
    #     genai.configure(api_key=self.api_key)
    #     self.model = genai.GenerativeModel(self.model_name)

    def __init__(self, api_key: Optional[str] = None, model_name: str = "models/gemini-3-flash-preview"):
        """
        Args:
            api_key: Google API key. Defaults to GEMINI_API_KEY env var.
            model_name: Model identifier (e.g., 'gemini-1.5-flash' or 'gemini-1.5-pro').
        """
        # 1. Handle API Key resolution
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError("API key must be provided or set in GEMINI_API_KEY environment variable.")

        # 2. Configure and Initialize
        genai.configure(api_key=self.api_key)
        self.model_name = model_name
        self.model = genai.GenerativeModel(self.model_name)

    def extract(self, text: str) -> List[str]:
        """
        Extract technical skills from resume text using LLM.
        Args:  text: Resume text content
        Returns:  List of extracted technical skills
        """

        # print("当前账号支持生成内容（generateContent）的模型列表：")
        # for m in genai.list_models():
        #     if 'generateContent' in m.supported_generation_methods:
        #         print(f"模型名称: {m.name}")

        if not text or not text.strip(): return []

        try:
            # Craft a prompt for skill extraction
            prompt = f"""
                You are a resume parser. Extract all technical skills from the following resume text.
                
                Instructions:
                1. Identify programming languages, frameworks, tools, technologies, and technical methodologies
                2. Return ONLY a valid JSON array of skills as strings
                3. Each skill should be a concise term or phrase
                4. Remove duplicates and normalize similar terms
                5. Include only technical skills, not soft skills
                6. Do not include any explanation, just the JSON array
                
                Resume Text:
                {text}
                
                Return format (example):
                ["Python", "Machine Learning", "TensorFlow", "Docker", "AWS", "SQL"]
                
                JSON Array of Skills:
                """
            # Call Gemini API
            response = self.model.generate_content(prompt)
            if not response or not response.text: return []
            # Extract skills from response
            skills = self._parse_skills_from_response(response.text)
            return skills

        except Exception as e:
            # Log the error but don't fail completely
            print(f"Warning: Gemini API call failed: {str(e)}")
            # Fallback to regex-based extraction
            return self._fallback_extraction(text)

    def _parse_skills_from_response(self, response_text: str) -> List[str]:
        """
        Parse skills from Gemini API response.  Args:response_text: Raw response text from Gemini
        Returns: List of extracted skills
        """
        try:
            json_match = re.search(r'\[.*?\]', response_text, re.DOTALL)

            if json_match:
                json_str = json_match.group(0)
                skills = json.loads(json_str)
                if isinstance(skills, list):
                    # Clean up and validate skills
                    return [str(skill).strip() for skill in skills if skill]
            return []
        except (json.JSONDecodeError, ValueError):
            # If parsing fails, return empty list
            return []

    def _fallback_extraction(self, text: str) -> List[str]:
        """
        Fallback regex-based skill extraction if LLM fails.
        Args:text: Resume text content
        Returns:List of extracted skills using simple heuristics
        """
        # Common technical skills patterns
        common_skills = [
            "Python", "Java", "JavaScript", "C++", "C#", "Ruby", "Go", "Rust",
            "SQL", "NoSQL", "MongoDB", "PostgreSQL", "MySQL",
            "React", "Angular", "Vue", "Node.js", "Django", "Flask", "Spring",
            "Docker", "Kubernetes", "AWS", "Azure", "GCP",
            "Git", "CI/CD", "Jenkins", "Linux", "Unix",
            "Machine Learning", "Deep Learning", "AI", "NLP", "Computer Vision",
            "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy",
            "REST API", "GraphQL", "Microservices", "Agile", "Scrum"
        ]

        # Find skills mentioned in the text (case-insensitive)
        found_skills = []
        text_lower = text.lower()

        for skill in common_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)

        return found_skills
