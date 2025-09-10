"""
Abstract base classes for services.
Following Dependency Inversion Principle - depend on abstractions, not concretions.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional


class ChatServiceInterface(ABC):
    """Abstract interface for chat services."""
    
    @abstractmethod
    def generate_response(
        self, 
        message: str, 
        language: str, 
        context: Optional[Dict] = None, 
        user_id: str = ""
    ) -> str:
        """Generate a chat response."""
        pass


class LanguageServiceInterface(ABC):
    """Abstract interface for language services."""
    
    @abstractmethod
    def get_supported_languages(self) -> list:
        """Get list of supported languages."""
        pass
    
    @abstractmethod
    def get_default_language(self) -> str:
        """Get default language."""
        pass
    
    @abstractmethod
    def normalize_language(self, language: Optional[str]) -> str:
        """Normalize language code to supported language."""
        pass
