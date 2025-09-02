"""
Exception handling utilities.
Following Single Responsibility Principle - handles only error management.
"""

from fastapi import HTTPException
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ChatServiceError(Exception):
    """Custom exception for chat service errors."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class LanguageNotSupportedError(Exception):
    """Exception raised when an unsupported language is requested."""
    
    def __init__(self, language: str):
        self.language = language
        super().__init__(f"Language '{language}' is not supported")


def handle_service_error(error: Exception, user_id: str = "") -> HTTPException:
    """
    Convert service errors to HTTP exceptions.
    
    Args:
        error: The exception to handle
        user_id: User ID for logging context
        
    Returns:
        HTTPException with appropriate status code and message
    """
    logger.error(f"Service error for user {user_id}: {str(error)}")
    
    if isinstance(error, ChatServiceError):
        return HTTPException(
            status_code=500,
            detail={
                "message": error.message,
                "details": error.details,
                "type": "chat_service_error"
            }
        )
    
    if isinstance(error, LanguageNotSupportedError):
        return HTTPException(
            status_code=400,
            detail={
                "message": str(error),
                "type": "language_not_supported"
            }
        )
    
    # Generic error handling
    return HTTPException(
        status_code=500,
        detail={
            "message": "An unexpected error occurred",
            "type": "internal_server_error"
        }
    )


def log_request_error(endpoint: str, user_id: str, error: Exception) -> None:
    """
    Log request errors with context.
    
    Args:
        endpoint: API endpoint where error occurred
        user_id: User ID for context
        error: The exception that occurred
    """
    logger.error(
        f"Error in {endpoint} for user {user_id}: {str(error)}",
        extra={
            "endpoint": endpoint,
            "user_id": user_id,
            "error_type": type(error).__name__
        }
    )
