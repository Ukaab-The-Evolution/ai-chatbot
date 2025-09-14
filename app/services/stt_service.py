"""
Whisper speech-to-text service implementation.
Following Single Responsibility Principle - handles only audio transcription.
"""

import base64
import io
import logging
from typing import Optional
import tempfile
import os

from .interfaces import STTServiceInterface
from ..core.config import Settings

logger = logging.getLogger(__name__)


class WhisperSTTService(STTServiceInterface):
    """OpenAI Whisper local service for speech-to-text conversion."""
    
    SUPPORTED_LANGUAGES = ["english", "urdu", "punjabi", "pushto", "balochi", "saraiki"]
    
    def __init__(self, settings: Settings):
        """Initialize Whisper STT service."""
        self.settings = settings
        self.model = None
        
        # Load Whisper model on initialization
        self._load_model()
    
    def _load_model(self):
        """Load Whisper model."""
        try:
            # Import whisper library (only when needed)
            import whisper
            
            # Load the base model (you can change to 'small', 'medium', 'large' for better accuracy)
            self.model = whisper.load_model("base")
            self.enabled = True
            logger.info("Whisper model loaded successfully")
            
        except ImportError:
            logger.error("OpenAI Whisper library not installed. Install with: pip install openai-whisper")
            self.enabled = False
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {str(e)}")
            self.enabled = False
    
    def is_language_supported(self, language: str) -> bool:
        """
        Check if language is supported for STT.
        
        Args:
            language: Language code to check
            
        Returns:
            True if language is supported, False otherwise
        """
        return language.lower() in self.SUPPORTED_LANGUAGES
    
    async def transcribe_audio(
        self, 
        audio_data: str, 
        language: str = "auto"
    ) -> Optional[str]:
        """
        Transcribe audio from base64 encoded data using Whisper.
        
        Args:
            audio_data: Base64 encoded audio data
            language: Language hint for transcription
            
        Returns:
            Transcribed text or None if transcription fails
        """
        if not self.enabled:
            logger.warning("Whisper STT service is disabled due to model loading failure")
            return None
        
        if not audio_data or not audio_data.strip():
            logger.warning("Empty audio data provided for transcription")
            return None
        
        try:
            # Decode base64 audio data
            try:
                audio_bytes = base64.b64decode(audio_data)
            except Exception as e:
                logger.error(f"Failed to decode base64 audio data: {str(e)}")
                return None
            
            # Create temporary file for audio data
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file.write(audio_bytes)
                temp_file_path = temp_file.name
            
            try:
                logger.info(f"Transcribing audio for language '{language}' with {len(audio_bytes)} bytes")
                
                # Prepare language parameter for Whisper
                whisper_language = None
                if language != "auto" and self.is_language_supported(language):
                    # Map our language codes to Whisper language codes
                    language_mapping = {
                        "english": "en",
                        "urdu": "ur",
                        "punjabi": "pa",
                        "pushto": "ps",
                        "balochi": "bal",  # Balochi support depends on Whisper model
                        "saraiki": "sd"    # Use Sindhi as closest match for Saraiki
                    }
                    whisper_language = language_mapping.get(language.lower())
                
                # Transcribe audio using Whisper
                if whisper_language:
                    result = self.model.transcribe(temp_file_path, language=whisper_language)
                else:
                    result = self.model.transcribe(temp_file_path)
                
                transcript = result["text"].strip()
                logger.info(f"Transcription successful: '{transcript[:100]}...'")
                return transcript
                
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_file_path)
                except OSError:
                    logger.warning(f"Failed to delete temporary file: {temp_file_path}")
                    
        except Exception as e:
            logger.error(f"Unexpected error during audio transcription: {str(e)}")
            return None
    
    def get_supported_languages(self) -> list:
        """
        Get list of supported STT languages.
        
        Returns:
            List of supported language codes
        """
        return self.SUPPORTED_LANGUAGES.copy()


class MockSTTService(STTServiceInterface):
    """Mock STT service for testing."""
    
    SUPPORTED_LANGUAGES = ["english", "urdu", "punjabi", "pushto", "balochi", "saraiki"]
    
    def is_language_supported(self, language: str) -> bool:
        """Check if language is supported for STT."""
        return language.lower() in self.SUPPORTED_LANGUAGES
    
    async def transcribe_audio(
        self, 
        audio_data: str, 
        language: str = "auto"
    ) -> Optional[str]:
        """Mock audio transcription."""
        if not self.is_language_supported(language):
            return None
        
        # Return mock transcription
        mock_transcriptions = {
            "english": "I need to transport cargo from Karachi to Lahore",
            "urdu": "مجھے کراچی سے لاہور تک سامان لے جانا ہے",
            "punjabi": "میں کراچی توں لاہور تک سامان لے جانا چاہندا ہاں",
            "pushto": "زه غواړم د کراچۍ څخه لاهور ته سامان ولیږدوم"
        }
        
        mock_text = mock_transcriptions.get(language, "Mock transcription text")
        logger.info(f"Mock STT transcription for '{language}': '{mock_text}'")
        return mock_text
    
    def get_supported_languages(self) -> list:
        """Get list of supported STT languages."""
        return self.SUPPORTED_LANGUAGES.copy()
