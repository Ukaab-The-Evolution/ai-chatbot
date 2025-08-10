"""
Language service implementation.
Following Single Responsibility Principle - handles only language operations.
"""

from typing import Optional
from ..core.config import language_config
from .interfaces import LanguageServiceInterface


class LanguageService(LanguageServiceInterface):
    """Language service for handling language operations."""
    
    def get_supported_languages(self) -> list:
        """Get list of supported language codes."""
        return language_config.get_supported_languages()
    
    def get_default_language(self) -> str:
        """Get default language code."""
        return language_config.DEFAULT_LANGUAGE
    
    def normalize_language(self, language: Optional[str]) -> str:
        """
        Normalize language code to supported language.
        
        Args:
            language: Language code from request
            
        Returns:
            Normalized language code (defaults to English if invalid)
        """
        if not language:
            return self.get_default_language()
        
        normalized = language.lower().strip()
        
        if language_config.is_language_supported(normalized):
            return normalized
        
        return self.get_default_language()
