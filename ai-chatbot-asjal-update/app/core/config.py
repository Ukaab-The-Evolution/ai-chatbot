"""
Core configuration and settings.
A cleaned, working version for local development and fallback behavior.
"""

import os
from dotenv import load_dotenv
from typing import Dict, List, Optional

# Load environment variables from .env or chatbot.env
load_dotenv()

class Settings:
    """Application settings and configuration."""
    def __init__(self):
        self.host: str = os.environ.get("HOST", "0.0.0.0")
        self.port: int = int(os.environ.get("PORT", 8000))
        self.debug: bool = str(os.environ.get("DEBUG", "false")).lower() in ("1","true","yes")
        self.gemini_api_key: Optional[str] = os.environ.get("GEMINI_API_KEY") or None
        # default model name -- can be overridden via env
        self.gemini_model: str = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    
    @classmethod
    def get_system_instruction(cls, language: str) -> str:
        """Return a short system instruction based on language."""
        # Basic mapping; can be extended
        instructions = {
            "english": "You are a helpful assistant that replies concisely in English.",
            "urdu": "You are a helpful assistant that replies concisely in Urdu.",
            "punjabi": "You are a helpful assistant that replies concisely in Punjabi.",
            "balochi": "You are a helpful assistant that replies concisely in Balochi.",
            "saraiki": "You are a helpful assistant that replies concisely in Saraiki.",
            "pushto": "You are a helpful assistant that replies concisely in Pushto.",
        }
        return instructions.get(language, instructions["english"])
    
    @classmethod
    def is_language_supported(cls, language: str) -> bool:
        return language in {"english","urdu","punjabi","balochi","saraiki","pushto"}

class LanguageConfig:
    """Language helper functions used by the app."""
    SUPPORTED: List[str] = ["english","urdu","punjabi","balochi","saraiki","pushto"]
    DEFAULT_LANGUAGE: str = "english"

    def get_supported_languages(self) -> List[str]:
        return self.SUPPORTED.copy()
    
    def get_default_language(self) -> str:
        return self.DEFAULT_LANGUAGE

    def normalize_language(self, language: Optional[str]) -> str:
        if not language:
            return self.DEFAULT_LANGUAGE
        language = language.strip().lower()
        if language in self.SUPPORTED:
            return language
        # try to map common names
        mapping = {
            "en": "english",
            "ur": "urdu",
            "pa": "punjabi",
            "ps": "pushto",
            "sd": "saraiki",
            "bal": "balochi"
        }
        return mapping.get(language, self.DEFAULT_LANGUAGE)

# Global settings instance
settings = Settings()
language_config = LanguageConfig()
