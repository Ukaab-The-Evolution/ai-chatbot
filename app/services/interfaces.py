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


class TTSServiceInterface(ABC):
    """Abstract interface for Text-to-Speech services."""
    
    @abstractmethod
    def is_language_supported(self, language: str) -> bool:
        """Check if language is supported for TTS."""
        pass
    
    @abstractmethod
    async def synthesize_speech(
        self, 
        text: str, 
        language: str, 
        format: str = "mp3"
    ) -> Optional[bytes]:
        """
        Synthesize speech from text.
        
        Args:
            text: Text to convert to speech
            language: Language for synthesis
            format: Audio format (mp3, wav)
            
        Returns:
            Audio bytes or None if synthesis fails
        """
        pass
    
    @abstractmethod
    def get_supported_languages(self) -> list:
        """Get list of supported TTS languages."""
        pass
