"""
Text-to-Speech service implementation.
Following Single Responsibility Principle - handles only TTS operations.
"""

import asyncio
import aiohttp
import logging
import base64
from typing import Optional

from .interfaces import TTSServiceInterface

# Configure logging
logger = logging.getLogger(__name__)


class MasAITTSService(TTSServiceInterface):
    """MAS AI TTS service implementation."""
    
    TTS_ENDPOINT = "https://mas-ai-0000-tts.hf.space/tts"
    SUPPORTED_LANGUAGES = ["english", "urdu", "punjabi"]
    TIMEOUT_SECONDS = 60
    
    def __init__(self):
        """Initialize TTS service."""
        self.session = None
        logger.info("MAS AI TTS service initialized")
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=self.TIMEOUT_SECONDS)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    def is_language_supported(self, language: str) -> bool:
        """
        Check if language is supported for TTS.
        
        Args:
            language: Language code to check
            
        Returns:
            True if language is supported, False otherwise
        """
        return language.lower() in self.SUPPORTED_LANGUAGES
    
    async def synthesize_speech(
        self, 
        text: str, 
        language: str, 
        format: str = "mp3"
    ) -> Optional[bytes]:
        """
        Synthesize speech from text using MAS AI TTS service.
        
        Args:
            text: Text to convert to speech
            language: Language for synthesis
            format: Audio format (mp3, wav)
            
        Returns:
            Audio bytes or None if synthesis fails
        """
        if not self.is_language_supported(language):
            logger.warning(f"Language '{language}' not supported for TTS")
            return None
        
        if not text or not text.strip():
            logger.warning("Empty text provided for TTS")
            return None
        
        try:
            session = await self._get_session()
            
            # Prepare request payload
            payload = {
                "text": text.strip(),
                "language": language.lower(),
                "format": format.lower()
            }
            
            logger.info(f"Calling TTS service for language '{language}' with {len(text)} characters")
            
            async with session.post(self.TTS_ENDPOINT, json=payload) as response:
                if response.status == 200:
                    audio_data = await response.read()
                    logger.info(f"TTS synthesis successful, received {len(audio_data)} bytes")
                    return audio_data
                else:
                    logger.error(f"TTS service returned status {response.status}: {await response.text()}")
                    return None
                    
        except asyncio.TimeoutError:
            logger.error("TTS service request timed out")
            return None
        except aiohttp.ClientError as e:
            logger.error(f"TTS service client error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in TTS synthesis: {str(e)}")
            return None
    
    def get_supported_languages(self) -> list:
        """
        Get list of supported TTS languages.
        
        Returns:
            List of supported language codes
        """
        return self.SUPPORTED_LANGUAGES.copy()
    
    async def close(self):
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()
            logger.info("TTS service session closed")
    
    def __del__(self):
        """Cleanup on object destruction."""
        if self.session and not self.session.closed:
            # Schedule cleanup in background
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(self.close())
            except RuntimeError:
                # Event loop not running, can't clean up
                pass


class MockTTSService(TTSServiceInterface):
    """Mock TTS service for testing."""
    
    SUPPORTED_LANGUAGES = ["english", "urdu", "punjabi"]
    
    def is_language_supported(self, language: str) -> bool:
        """Check if language is supported for TTS."""
        return language.lower() in self.SUPPORTED_LANGUAGES
    
    async def synthesize_speech(
        self, 
        text: str, 
        language: str, 
        format: str = "mp3"
    ) -> Optional[bytes]:
        """Mock speech synthesis."""
        if not self.is_language_supported(language):
            return None
        
        # Return mock audio data (empty MP3 header)
        mock_audio = b"ID3\x04\x00\x00\x00\x00\x00\x00"
        logger.info(f"Mock TTS synthesis for '{text[:50]}...' in {language}")
        return mock_audio
    
    def get_supported_languages(self) -> list:
        """Get list of supported TTS languages."""
        return self.SUPPORTED_LANGUAGES.copy()
