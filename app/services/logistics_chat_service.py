"""
Enhanced logistics chat service with STT and structured data parsing.
Following Single Responsibility Principle - orchestrates STT, chat, and TTS services.
"""

import logging
import base64
import json
from typing import Dict, Optional, Tuple

from .interfaces import ChatServiceInterface, TTSServiceInterface, STTServiceInterface
from .gemini_service import GeminiChatService
from .tts_service import AzureTTSService
from .stt_service import WhisperSTTService
from ..models.schemas import ChatRequest, ChatResponse, SpeechResponse, LogisticsData
from ..models.response_schemas import LogisticsResponseSchema
from ..core.config import Settings, LanguageConfig

logger = logging.getLogger(__name__)


class LogisticsChatService:
    """
    Enhanced logistics chat service that combines STT, text generation, structured parsing, and TTS.
    Follows Single Responsibility Principle by orchestrating services.
    """
    
    def __init__(
        self, 
        chat_service: ChatServiceInterface = None,
        tts_service: TTSServiceInterface = None,
        stt_service: STTServiceInterface = None,
        settings: Settings = None
    ):
        """
        Initialize enhanced logistics chat service.
        
        Args:
            chat_service: Chat service for text generation
            tts_service: TTS service for speech synthesis
            stt_service: STT service for audio transcription
            settings: Application settings
        """
        self.settings = settings or Settings()
        self.chat_service = chat_service or GeminiChatService()
        self.tts_service = tts_service or AzureTTSService(self.settings)
        self.stt_service = stt_service or WhisperSTTService(self.settings)
        logger.info("Enhanced logistics chat service initialized")
    
    async def process_request(self, request: ChatRequest, language: str) -> ChatResponse:
        """
        Process a chat request with optional audio input and structured data parsing.
        
        Args:
            request: The chat request
            language: Language for processing
            
        Returns:
            Enhanced chat response with optional speech and structured data
        """
        try:
            # Step 1: Extract text message (from text or audio)
            message_text = await self._extract_message_text(request, language)
            if not message_text:
                return ChatResponse.create(
                    response="Sorry, I couldn't understand your message. Please try again.",
                    language=language,
                    user_id=request.user_id
                )
            
            # Step 2: Generate AI response with structured data parsing
            ai_response, logistics_data = await self._generate_structured_response(
                message_text, language, request
            )
            
            # Step 3: Optional speech synthesis
            speech_data = None
            if request.include_speech and ai_response:
                speech_language = request.speech_language or language
                speech_data = await self._synthesize_speech(ai_response, speech_language)
            
            # Step 4: Create enhanced response
            return ChatResponse.create(
                response=ai_response,
                language=language,
                user_id=request.user_id,
                speech=speech_data,
                data=logistics_data
            )
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return ChatResponse.create(
                response="Sorry, there was an error processing your request. Please try again.",
                language=language,
                user_id=request.user_id
            )
    
    async def _extract_message_text(self, request: ChatRequest, language: str) -> Optional[str]:
        """
        Extract message text from either text field or audio transcription.
        
        Args:
            request: Chat request
            language: Language for transcription
            
        Returns:
            Message text or None if extraction fails
        """
        # If text message is provided, use it
        if request.message and request.message.strip():
            logger.info("Using provided text message")
            return request.message.strip()
        
        # If audio stream is provided, transcribe it
        if request.audio_stream and request.audio_stream.strip():
            logger.info("Transcribing audio stream")
            transcribed_text = await self.stt_service.transcribe_audio(
                request.audio_stream, language
            )
            if transcribed_text:
                logger.info(f"Audio transcription successful: '{transcribed_text[:100]}...'")
                return transcribed_text
            else:
                logger.warning("Audio transcription failed")
                return None
        
        logger.warning("No text message or audio stream provided")
        return None
    
    async def _generate_structured_response(
        self, 
        message: str, 
        language: str, 
        request: ChatRequest
    ) -> Tuple[Optional[str], Optional[LogisticsData]]:
        """
        Generate AI response with structured logistics data parsing.
        
        Args:
            message: Message text to process
            language: Language for response
            request: Original request for context
            
        Returns:
            Tuple of (response_text, logistics_data)
        """
        try:
            # Build enhanced prompt for structured data extraction
            structured_prompt = self._build_structured_prompt(message, language)
            
            # Generate response using Gemini
            ai_response = self.chat_service.generate_response(
                structured_prompt,
                language,
                context=self._build_context(request),
                user_id=request.user_id
            )
            
            # Parse JSON response
            return self._parse_structured_response(ai_response)
            
        except Exception as e:
            logger.error(f"Error generating structured response: {str(e)}")
            # Fallback to simple response
            simple_response = self.chat_service.generate_response(
                message, language, user_id=request.user_id
            )
            return simple_response, None
    
    def _build_structured_prompt(self, message: str, language: str) -> str:
        """
        Build a prompt that instructs the AI to return structured logistics data.
        
        Args:
            message: User message
            language: Response language
            
        Returns:
            Enhanced prompt for structured data extraction
        """
        # Get base instruction from config
        base_instruction = LanguageConfig.get_system_instruction(language)
        
        # Get JSON instructions from schema module
        json_instruction = LogisticsResponseSchema.get_json_instructions(language)
        
        return f"{base_instruction}\n\n{json_instruction}\n\nUser message: {message}"
    
    def _parse_structured_response(self, ai_response: str) -> Tuple[Optional[str], Optional[LogisticsData]]:
        """
        Parse JSON response from AI to extract response text and logistics data.
        
        Args:
            ai_response: Raw AI response
            
        Returns:
            Tuple of (response_text, logistics_data)
        """
        try:
            # Try to parse as JSON
            parsed = json.loads(ai_response)
            
            # Extract response message
            response_text = parsed.get("response")
            
            # Extract and validate logistics data
            data_dict = parsed.get("data")
            logistics_data = None
            
            if data_dict and isinstance(data_dict, dict):
                # Filter out None/empty values and validate
                filtered_data = {
                    k: v for k, v in data_dict.items() 
                    if v is not None and str(v).strip()
                }
                
                if filtered_data:
                    logistics_data = LogisticsData(**filtered_data)
                    logger.info(f"Extracted logistics data: {filtered_data}")
            
            return response_text, logistics_data
            
        except json.JSONDecodeError:
            logger.warning("AI response is not valid JSON, treating as plain text")
            return ai_response, None
        except Exception as e:
            logger.error(f"Error parsing structured response: {str(e)}")
            return ai_response, None
    
    def _build_context(self, request: ChatRequest) -> Dict:
        """Build context dictionary from request."""
        context = {}
        if request.context:
            context.update({
                "screen": request.context.screen,
                "entity_id": request.context.entity_id,
                "language": request.context.language
            })
        if request.location:
            context["location"] = {
                "latitude": request.location.latitude,
                "longitude": request.location.longitude
            }
        return context
    
    async def _synthesize_speech(self, text: str, language: str) -> Optional[SpeechResponse]:
        """
        Synthesize speech for the given text.
        
        Args:
            text: Text to synthesize
            language: Language for synthesis
            
        Returns:
            SpeechResponse object or None if synthesis fails
        """
        try:
            audio_bytes = await self.tts_service.synthesize_speech(text, language)
            if audio_bytes:
                # Encode to base64 data URL
                audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
                data_url = f"data:audio/mpeg;base64,{audio_base64}"
                
                return SpeechResponse(
                    mime_type="audio/mpeg",
                    data_url=data_url
                )
            else:
                logger.warning("TTS synthesis failed")
                return None
                
        except Exception as e:
            logger.error(f"Error during speech synthesis: {str(e)}")
            return None
