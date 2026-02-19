"""
Configuration management for the resume parser framework.

This module handles loading and validating configuration values,
particularly API keys and environment variables.
"""

import os
from typing import Optional
from pathlib import Path


class Config:
    """
    Configuration manager for the resume parser framework.

    Handles loading configuration from environment variables and .env files.
    """

    def __init__(self):
        """Initialize configuration by loading environment variables."""
        self._load_env_file()

    def _load_env_file(self) -> None:
        """
        Load environment variables from .env file if it exists.

        Uses python-dotenv to load variables from .env file in the project root.
        """
        try:
            from dotenv import load_dotenv

            # Try to find .env file in current directory or parent directories
            current_dir = Path.cwd()
            env_file = current_dir / '.env'

            if env_file.exists():
                load_dotenv(env_file)
            else:
                # Try parent directories
                for parent in current_dir.parents:
                    env_file = parent / '.env'
                    if env_file.exists():
                        load_dotenv(env_file)
                        break

        except ImportError:
            # python-dotenv not installed, skip loading from file
            pass

    @property
    def gemini_api_key(self) -> Optional[str]:
        """
        Get the Gemini API key from environment variables.

        Returns:
            Gemini API key if set, None otherwise
        """
        return os.getenv('GEMINI_API_KEY')

    def validate_gemini_api_key(self) -> bool:
        """
        Validate that Gemini API key is configured.

        Returns:
            True if API key is set and not empty, False otherwise
        """
        api_key = self.gemini_api_key
        return api_key is not None and api_key.strip() != ''

    def get_gemini_api_key(self) -> str:
        """
        Get the Gemini API key, raising an error if not configured.

        Returns:
            Gemini API key

        Raises:
            ValueError: If API key is not configured
        """
        if not self.validate_gemini_api_key():
            raise ValueError(
                "Gemini API key not configured. "
                "Set GEMINI_API_KEY environment variable or add it to .env file."
            )

        return self.gemini_api_key


# Global configuration instance
config = Config()
