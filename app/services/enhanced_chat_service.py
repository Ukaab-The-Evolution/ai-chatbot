"""
Enhanced chat service with TTS support.
Following Single Responsibility Principle - orchestrates chat and TTS services.
"""

import logging
import base64
from typing import Dict, Optional

from .interfaces import ChatServiceInterface, TTSServiceInterface
from .gemini_service import GeminiChatService
from .tts_service import AzureTTSService
from ..models.schemas import SpeechResponse
from ..core.config import Settings

# Configure logging
logger = logging.getLogger(__name__)


class EnhancedChatService:
    """
    Enhanced chat service that combines text generation and TTS.
    Follows Single Responsibility Principle by orchestrating services.
    """
    
    def __init__(
        self, 
        chat_service: ChatServiceInterface = None,
        tts_service: TTSServiceInterface = None,
        settings: Settings = None
    ):
        """
        Initialize enhanced chat service.
        
        Args:
            chat_service: Chat service for text generation
            tts_service: TTS service for speech synthesis
            settings: Application settings
        """
        self.settings = settings or Settings()
        self.chat_service = chat_service or GeminiChatService()
        self.tts_service = tts_service or AzureTTSService(self.settings)
        logger.info("Enhanced chat service initialized")
    
    async def generate_response(
        self,
        message: str,
        language: str,
        context: Optional[Dict] = None,
        user_id: str = "",
        include_speech: bool = False,
        speech_language: Optional[str] = None
    ) -> tuple[str, Optional[SpeechResponse]]:
        """
        Generate chat response with optional speech synthesis.
        
        Args:
            message: User message
            language: Response language
            context: Additional context
            user_id: User identifier
            include_speech: Whether to include speech synthesis
            speech_language: Language for speech synthesis
            
        Returns:
            Tuple of (text_response, speech_response)
        """
        # Generate text response
        text_response = self.chat_service.generate_response(
            message=message,
            language=language,
            context=context,
            user_id=user_id
        )
        
        speech_response = None
        
        # Generate speech if requested
        if include_speech and text_response:
            speech_response = await self._synthesize_speech(
                text=text_response,
                language=speech_language or language,
                user_id=user_id
            )
        
        return text_response, speech_response
    
    async def _synthesize_speech(
        self,
        text: str,
        language: str,
        user_id: str
    ) -> Optional[SpeechResponse]:
        """
        Synthesize speech from text.
        
        Args:
            text: Text to synthesize
            language: Language for synthesis
            user_id: User identifier for logging
            
        Returns:
            SpeechResponse or None if synthesis fails
        """
        try:
            # Check if language is supported for TTS
            if not self.tts_service.is_language_supported(language):
                logger.warning(f"TTS not supported for language '{language}' for user {user_id}")
                return None
            
            # Synthesize speech
            audio_bytes = await self.tts_service.synthesize_speech(
                text=text,
                language=language,
                format="mp3"
            )
            
            if audio_bytes:
                # Encode audio as base64 data URL
                audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
                data_url = f"data:audio/mpeg;base64,{audio_b64}"
                
                logger.info(f"Speech synthesis successful for user {user_id}")
                return SpeechResponse(
                    mime_type="audio/mpeg",
                    data_url=data_url
                )
            else:
                logger.warning(f"TTS synthesis failed for user {user_id}")
                return None
                
        except Exception as e:
            logger.error(f"Error in speech synthesis for user {user_id}: {str(e)}")
            return None
    
    async def close(self):
        """Close service resources."""
        if hasattr(self.tts_service, 'close'):
            await self.tts_service.close()
        logger.info("Enhanced chat service closed")
