"""
Utility endpoints.
Following Single Responsibility Principle - handles only utility routes.
"""

from fastapi import APIRouter, Depends
from datetime import datetime

from ...models.schemas import HealthResponse, LanguagesResponse
from ...services.interfaces import LanguageServiceInterface
from ...services.language_service import LanguageService

# Create router
router = APIRouter(tags=["utilities"])


def get_language_service() -> LanguageServiceInterface:
    """Dependency injection for language service."""
    return LanguageService()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat()
    )


@router.get("/languages", response_model=LanguagesResponse)
async def get_supported_languages(
    language_service: LanguageServiceInterface = Depends(get_language_service)
):
    """Get list of supported languages."""
    return LanguagesResponse(
        supported_languages=language_service.get_supported_languages(),
        default_language=language_service.get_default_language()
    )
