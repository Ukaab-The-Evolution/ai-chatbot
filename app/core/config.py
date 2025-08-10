"""
Core configuration and settings.
Following Single Responsibility Principle - handles only configuration.
"""

import os
from dotenv import load_dotenv
from typing import Dict

# Load environment variables
load_dotenv()


class Settings:
    """Application settings and configuration."""
    
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.port = int(os.environ.get("PORT", 8000))
        self.debug = os.environ.get("DEBUG", "false").lower() == "true"
        self.host = os.environ.get("HOST", "0.0.0.0")
        self.gemini_model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
        
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    @property
    def cors_origins(self) -> list:
        """Get CORS allowed origins."""
        origins = os.environ.get("CORS_ORIGINS", "*")
        if origins == "*":
            return ["*"]
        return [origin.strip() for origin in origins.split(",")]


class LanguageConfig:
    """Language-specific configuration and system instructions."""
    
    SYSTEM_INSTRUCTIONS: Dict[str, str] = {
        "english": """You are a helpful assistant for Pakistani truck drivers. Offer practical advice, safety tips, and support for life on the road. Be friendly, concise, and knowledgeable about trucking, logistics, and travel in Pakistan. Don't talk too much and don't be too verbose. Respond in English.""",

        "urdu": """You are a helpful assistant for Pakistani truck drivers. Offer practical advice, safety tips, and support for life on the road. Be friendly, concise, and knowledgeable about trucking, logistics, and travel in Pakistan. Don't talk too much and don't be too verbose. Respond in Urdu.""",

        "punjabi": """You are a helpful assistant for Pakistani truck drivers. Offer practical advice, safety tips, and support for life on the road. Be friendly, concise, and knowledgeable about trucking, logistics, and travel in Pakistan. Don't talk too much and don't be too verbose. Respond in Punjabi.""",

        "balochi": """You are a helpful assistant for Pakistani truck drivers. Offer practical advice, safety tips, and support for life on the road. Be friendly, concise, and knowledgeable about trucking, logistics, and travel in Pakistan. Don't talk too much and don't be too verbose. Respond in Balochi.""",

        "saraiki": """You are a helpful assistant for Pakistani truck drivers. Offer practical advice, safety tips, and support for life on the road. Be friendly, concise, and knowledgeable about trucking, logistics, and travel in Pakistan. Don't talk too much and don't be too verbose. Respond in Saraiki.""",

        "pushto": """You are a helpful assistant for Pakistani truck drivers. Offer practical advice, safety tips, and support for life on the road. Be friendly, concise, and knowledgeable about trucking, logistics, and travel in Pakistan. Don't talk too much and don't be too verbose. Respond in Pushto."""
    }
    
    DEFAULT_LANGUAGE = "english"
    
    @classmethod
    def get_supported_languages(cls) -> list:
        """Get list of supported language codes."""
        return list(cls.SYSTEM_INSTRUCTIONS.keys())
    
    @classmethod
    def get_system_instruction(cls, language: str) -> str:
        """Get system instruction for a specific language."""
        return cls.SYSTEM_INSTRUCTIONS.get(language, cls.SYSTEM_INSTRUCTIONS[cls.DEFAULT_LANGUAGE])
    
    @classmethod
    def is_language_supported(cls, language: str) -> bool:
        """Check if a language is supported."""
        return language in cls.SYSTEM_INSTRUCTIONS


# Global settings instance
settings = Settings()
language_config = LanguageConfig()
