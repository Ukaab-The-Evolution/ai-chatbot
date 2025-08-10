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
from ...utils.exceptions import handle_service_error, log_request_error

# Create router
router = APIRouter(prefix="/chat", tags=["chat"])

# Dependency injection functions
def get_chat_service() -> ChatServiceInterface:
    """Dependency injection for chat service."""
    return GeminiChatService()

def get_language_service() -> LanguageServiceInterface:
    """Dependency injection for language service."""
    return LanguageService()


async def _process_chat_request(
    request: ChatRequest,
    language: str,
    chat_service: ChatServiceInterface
) -> ChatResponse:
    """
    Common chat processing logic.
    
    Args:
        request: Chat request
        language: Target language
        chat_service: Chat service instance
        
    Returns:
        Chat response
        
    Raises:
        HTTPException: If processing fails
    """
    try:
        context_dict = request.context.dict() if request.context else None
        
        response_text = chat_service.generate_response(
            message=request.message,
            language=language,
            context=context_dict,
            user_id=request.user_id
        )
        
        return ChatResponse.create(
            response=response_text,
            language=language,
            user_id=request.user_id
        )
        
    except Exception as e:
        log_request_error(f"/chat/{language}", request.user_id, e)
        raise handle_service_error(e, request.user_id)


@router.post("/", response_model=ChatResponse)
async def chat_auto_route(
    request: ChatRequest,
    chat_service: ChatServiceInterface = Depends(get_chat_service),
    language_service: LanguageServiceInterface = Depends(get_language_service)
):
    """Auto-route chat endpoint based on language in context."""
    language = language_service.normalize_language(
        request.context.language if request.context else None
    )
    
    return await _process_chat_request(request, language, chat_service)


@router.post("/english", response_model=ChatResponse)
async def chat_english(
    request: ChatRequest,
    chat_service: ChatServiceInterface = Depends(get_chat_service)
):
    """English chat endpoint."""
    return await _process_chat_request(request, "english", chat_service)


@router.post("/urdu", response_model=ChatResponse)
async def chat_urdu(
    request: ChatRequest,
    chat_service: ChatServiceInterface = Depends(get_chat_service)
):
    """Urdu chat endpoint."""
    return await _process_chat_request(request, "urdu", chat_service)


@router.post("/punjabi", response_model=ChatResponse)
async def chat_punjabi(
    request: ChatRequest,
    chat_service: ChatServiceInterface = Depends(get_chat_service)
):
    """Punjabi chat endpoint."""
    return await _process_chat_request(request, "punjabi", chat_service)


@router.post("/balochi", response_model=ChatResponse)
async def chat_balochi(
    request: ChatRequest,
    chat_service: ChatServiceInterface = Depends(get_chat_service)
):
    """Balochi chat endpoint."""
    return await _process_chat_request(request, "balochi", chat_service)


@router.post("/saraiki", response_model=ChatResponse)
async def chat_saraiki(
    request: ChatRequest,
    chat_service: ChatServiceInterface = Depends(get_chat_service)
):
    """Saraiki chat endpoint."""
    return await _process_chat_request(request, "saraiki", chat_service)


@router.post("/pushto", response_model=ChatResponse)
async def chat_pushto(
    request: ChatRequest,
    chat_service: ChatServiceInterface = Depends(get_chat_service)
):
    """Pushto chat endpoint."""
    return await _process_chat_request(request, "pushto", chat_service)
