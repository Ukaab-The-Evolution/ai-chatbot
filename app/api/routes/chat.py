"""
Chat endpoints.
Following Single Responsibility Principle - handles only chat-related routes.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Optional

from ...models.schemas import ChatRequest, ChatResponse
from ...services.interfaces import ChatServiceInterface, LanguageServiceInterface
from ...services.gemini_service import GeminiChatService
from ...services.language_service import LanguageService
from ...services.enhanced_chat_service import EnhancedChatService
from ...utils.exceptions import handle_service_error, log_request_error

# Create router
router = APIRouter(prefix="/chat", tags=["chat"])

# Dependency injection functions
def get_enhanced_chat_service() -> EnhancedChatService:
    """Dependency injection for enhanced chat service."""
    return EnhancedChatService()

def get_language_service() -> LanguageServiceInterface:
    """Dependency injection for language service."""
    return LanguageService()


async def _process_chat_request(
    request: ChatRequest,
    language: str,
    enhanced_chat_service: EnhancedChatService
) -> ChatResponse:
    """
    Common chat processing logic with optional TTS support.
    
    Args:
        request: Chat request
        language: Target language
        enhanced_chat_service: Enhanced chat service instance
        
    Returns:
        Chat response with optional speech
        
    Raises:
        HTTPException: If processing fails
    """
    try:
        context_dict = request.context.dict() if request.context else None
        
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
    enhanced_chat_service: EnhancedChatService = Depends(get_enhanced_chat_service),
    language_service: LanguageServiceInterface = Depends(get_language_service)
):
    """Auto-route chat endpoint based on language in context."""
    language = language_service.normalize_language(
        request.context.language if request.context else None
    )
    
    return await _process_chat_request(request, language, enhanced_chat_service)


@router.post("/english", response_model=ChatResponse)
async def chat_english(
    request: ChatRequest,
    enhanced_chat_service: EnhancedChatService = Depends(get_enhanced_chat_service)
):
    """English chat endpoint with optional TTS support."""
    return await _process_chat_request(request, "english", enhanced_chat_service)


@router.post("/urdu", response_model=ChatResponse)
async def chat_urdu(
    request: ChatRequest,
    enhanced_chat_service: EnhancedChatService = Depends(get_enhanced_chat_service)
):
    """Urdu chat endpoint with optional TTS support."""
    return await _process_chat_request(request, "urdu", enhanced_chat_service)


@router.post("/punjabi", response_model=ChatResponse)
async def chat_punjabi(
    request: ChatRequest,
    enhanced_chat_service: EnhancedChatService = Depends(get_enhanced_chat_service)
):
    """Punjabi chat endpoint with optional TTS support."""
    return await _process_chat_request(request, "punjabi", enhanced_chat_service)


@router.post("/balochi", response_model=ChatResponse)
async def chat_balochi(
    request: ChatRequest,
    enhanced_chat_service: EnhancedChatService = Depends(get_enhanced_chat_service)
):
    """Balochi chat endpoint."""
    return await _process_chat_request(request, "balochi", enhanced_chat_service)


@router.post("/saraiki", response_model=ChatResponse)
async def chat_saraiki(
    request: ChatRequest,
    enhanced_chat_service: EnhancedChatService = Depends(get_enhanced_chat_service)
):
    """Saraiki chat endpoint."""
    return await _process_chat_request(request, "saraiki", enhanced_chat_service)


@router.post("/pushto", response_model=ChatResponse)
async def chat_pushto(
    request: ChatRequest,
    enhanced_chat_service: EnhancedChatService = Depends(get_enhanced_chat_service)
):
    """Pushto chat endpoint with optional TTS support."""
    return await _process_chat_request(request, "pushto", enhanced_chat_service)


@router.get("/tts/languages")
async def get_tts_supported_languages(
    enhanced_chat_service: EnhancedChatService = Depends(get_enhanced_chat_service)
):
    """Get list of languages supported for Text-to-Speech."""
    return {
        "supported_tts_languages": enhanced_chat_service.tts_service.get_supported_languages(),
        "description": "Languages that support speech synthesis in chat responses"
    }
