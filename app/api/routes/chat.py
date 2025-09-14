"""
Chat endpoints with STT and structured data parsing.
Following Single Responsibility Principle - handles only chat-related routes.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Optional

from ...models.schemas import ChatRequest, ChatResponse
from ...services.interfaces import ChatServiceInterface, LanguageServiceInterface
from ...services.gemini_service import GeminiChatService
from ...services.language_service import LanguageService
from ...services.logistics_chat_service import LogisticsChatService
from ...utils.exceptions import handle_service_error, log_request_error

# Create router
router = APIRouter(prefix="/chat", tags=["chat"])

# Dependency injection functions
def get_logistics_chat_service() -> LogisticsChatService:
    """Dependency injection for logistics chat service."""
    return LogisticsChatService()

def get_language_service() -> LanguageServiceInterface:
    """Dependency injection for language service."""
    return LanguageService()


async def _process_chat_request(
    request: ChatRequest,
    language: str,
    logistics_chat_service: LogisticsChatService
) -> ChatResponse:
    """
    Common chat processing logic with STT, structured parsing, and optional TTS support.
    
    Args:
        request: Chat request
        language: Target language
        logistics_chat_service: Logistics chat service instance
        
    Returns:
        Chat response with optional speech and structured data
        
    Raises:
        HTTPException: If processing fails
    """
    try:
        # Validate that either message or audio_stream is provided
        if not request.message and not request.audio_stream:
            raise HTTPException(
                status_code=400, 
                detail="Either 'message' or 'audio_stream' must be provided"
            )
        
        # Process request with enhanced logistics service
        return await logistics_chat_service.process_request(request, language)
        
        # Determine speech language (use request speech_language or fallback to response language)
        speech_language = request.speech_language or language if request.include_speech else None
        
        # Generate response with optional speech
        response_text, speech_response = await enhanced_chat_service.generate_response(
            message=request.message,
            language=language,
            context=context_dict,
            user_id=request.user_id,
            include_speech=request.include_speech,
            speech_language=speech_language
        )
        
        return ChatResponse.create(
            response=response_text,
            language=language,
            user_id=request.user_id,
            speech=speech_response
        )
        
    except Exception as e:
        log_request_error(f"/chat/{language}", request.user_id, e)
        raise handle_service_error(e, request.user_id)


@router.post("/", response_model=ChatResponse)
async def chat_auto_route(
    request: ChatRequest,
    logistics_chat_service: LogisticsChatService = Depends(get_logistics_chat_service),
    language_service: LanguageServiceInterface = Depends(get_language_service)
):
    """Auto-route chat endpoint based on language in context."""
    language = language_service.normalize_language(
        request.context.language if request.context else None
    )
    
    return await _process_chat_request(request, language, logistics_chat_service)


@router.post("/english", response_model=ChatResponse)
async def chat_english(
    request: ChatRequest,
    logistics_chat_service: LogisticsChatService = Depends(get_logistics_chat_service)
):
    """English chat endpoint with STT and structured data parsing."""
    return await _process_chat_request(request, "english", logistics_chat_service)


@router.post("/urdu", response_model=ChatResponse)
async def chat_urdu(
    request: ChatRequest,
    logistics_chat_service: LogisticsChatService = Depends(get_logistics_chat_service)
):
    """Urdu chat endpoint with STT and structured data parsing."""
    return await _process_chat_request(request, "urdu", logistics_chat_service)


@router.post("/punjabi", response_model=ChatResponse)
async def chat_punjabi(
    request: ChatRequest,
    logistics_chat_service: LogisticsChatService = Depends(get_logistics_chat_service)
):
    """Punjabi chat endpoint with STT and structured data parsing."""
    return await _process_chat_request(request, "punjabi", logistics_chat_service)


@router.post("/balochi", response_model=ChatResponse)
async def chat_balochi(
    request: ChatRequest,
    logistics_chat_service: LogisticsChatService = Depends(get_logistics_chat_service)
):
    """Balochi chat endpoint with STT and structured data parsing."""
    return await _process_chat_request(request, "balochi", logistics_chat_service)


@router.post("/saraiki", response_model=ChatResponse)
async def chat_saraiki(
    request: ChatRequest,
    logistics_chat_service: LogisticsChatService = Depends(get_logistics_chat_service)
):
    """Saraiki chat endpoint with STT and structured data parsing."""
    return await _process_chat_request(request, "saraiki", logistics_chat_service)


@router.post("/pushto", response_model=ChatResponse)
async def chat_pushto(
    request: ChatRequest,
    logistics_chat_service: LogisticsChatService = Depends(get_logistics_chat_service)
):
    """Pushto chat endpoint with STT and structured data parsing."""
    return await _process_chat_request(request, "pushto", logistics_chat_service)


@router.get("/tts/languages")
async def get_tts_supported_languages(
    logistics_chat_service: LogisticsChatService = Depends(get_logistics_chat_service)
):
    """Get list of languages supported for Text-to-Speech."""
    return {
        "supported_tts_languages": logistics_chat_service.tts_service.get_supported_languages(),
        "description": "Languages that support speech synthesis in chat responses"
    }
