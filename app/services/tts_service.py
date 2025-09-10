"""
Text-to-Speech service implementation.
Following Single Responsibility Principle - handles only TTS operations.
"""

import logging
from typing import Optional

from .interfaces import TTSServiceInterface
from ..core.config import Settings

# Configure logging
logger = logging.getLogger(__name__)


class AzureTTSService(TTSServiceInterface):
    """Azure Speech Service TTS implementation for truck driver assistant."""
    
    SUPPORTED_LANGUAGES = ["english", "urdu", "punjabi", "pushto"]
    TIMEOUT_SECONDS = 60
    
    def __init__(self, settings: Settings):
        """Initialize Azure TTS service."""
        self.settings = settings
        
        # Voice mapping for Azure Neural Voices
        self.voice_mapping = {
            "english": "en-US-AndrewMultilingualNeural",
            "urdu": "ur-PK-AsadNeural", 
            "punjabi": "pa-IN-OjasNeural",
            "pushto": "ps-AF-GulNawazNeural"
        }
        
        # Check if Azure credentials are available
        self.enabled = bool(settings.azure_speech_key and settings.azure_speech_region)
        if not self.enabled:
            logger.warning("Azure Speech Service credentials not available - TTS disabled")
        else:
            logger.info("Azure TTS service initialized")
    
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
        Synthesize speech from text using Azure Speech Service.
        
        Args:
            text: Text to convert to speech
            language: Language for synthesis
            format: Audio format (mp3, wav) - Azure will use MP3
            
        Returns:
            Audio bytes or None if synthesis fails
        """
        if not self.enabled:
            logger.warning("Azure TTS service is disabled due to missing credentials")
            return None
            
        if not self.is_language_supported(language):
            logger.warning(f"Language '{language}' not supported for TTS")
            return None
        
        if not text or not text.strip():
            logger.warning("Empty text provided for TTS")
            return None
        
        try:
            # Import Azure SDK (only when needed to avoid import errors)
            try:
                import azure.cognitiveservices.speech as speechsdk
            except ImportError:
                logger.error("Azure Speech SDK not installed. Install with: pip install azure-cognitiveservices-speech")
                return None
            
            # Get the appropriate voice for the language
            voice_name = self.voice_mapping[language.lower()]
            
            logger.info(f"Calling Azure TTS service for language '{language}' with voice '{voice_name}' and {len(text)} characters")
            
            # Configure Azure Speech Service
            speech_config = speechsdk.SpeechConfig(
                subscription=self.settings.azure_speech_key,
                region=self.settings.azure_speech_region
            )
            
            # Set the voice
            speech_config.speech_synthesis_voice_name = voice_name
            
            # Set audio format to MP3 for better compatibility and smaller size
            speech_config.set_speech_synthesis_output_format(
                speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
            )
            
            # Create synthesizer with no audio output (we want the raw data)
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
            
            # Synthesize speech
            result = synthesizer.speak_text_async(text.strip()).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logger.info(f"TTS synthesis successful using voice '{voice_name}', received {len(result.audio_data)} bytes")
                return result.audio_data
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                logger.error(f"Speech synthesis canceled: {cancellation.reason}")
                if cancellation.reason == speechsdk.CancellationReason.Error:
                    logger.error(f"Error details: {cancellation.error_details}")
                return None
            else:
                logger.error(f"Unexpected result reason: {result.reason}")
                return None
                
        except Exception as e:
            logger.error(f"Unexpected error during Azure TTS synthesis: {str(e)}")
            return None
    
    def get_supported_languages(self) -> list:
        """
        Get list of supported TTS languages.
        
        Returns:
            List of supported language codes
        """
        return self.SUPPORTED_LANGUAGES.copy()


class MockTTSService(TTSServiceInterface):
    """Mock TTS service for testing."""
    
    SUPPORTED_LANGUAGES = ["english", "urdu", "punjabi", "pushto"]
    
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
