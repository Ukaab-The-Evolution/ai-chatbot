"""
Pydantic models for request and response schemas.
Following Single Responsibility Principle - each model has one clear purpose.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Location(BaseModel):
    """Location model for GPS coordinates."""
    latitude: Optional[float] = Field(None, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, description="Longitude coordinate")


class Context(BaseModel):
    """Context model for additional request information."""
    screen: Optional[str] = Field(None, description="Current screen/page identifier")
    entity_id: Optional[str] = Field(None, description="Entity identifier")
    language: Optional[str] = Field(None, description="Preferred language code")


class Attachment(BaseModel):
    """Attachment model for file uploads."""
    type: str = Field(..., description="Type of attachment (pdf, image, etc.)")
    url: str = Field(..., description="URL of the attachment")
    filename: str = Field(..., description="Filename of the attachment")


class ChatRequest(BaseModel):
    """Chat request model for incoming messages."""
    user_id: str = Field(..., description="Unique identifier for the user")
    role: str = Field(..., description="Role of the message sender")
    message: str = Field(..., description="The chat message")
    context: Optional[Context] = Field(None, description="Additional context information")
    attachments: Optional[List[Attachment]] = Field(None, description="File attachments")
    location: Optional[Location] = Field(None, description="User location")
    timestamp: str = Field(..., description="Timestamp of the message")


class ChatResponse(BaseModel):
    """Chat response model for outgoing messages."""
    response: str = Field(..., description="AI generated response")
    language: str = Field(..., description="Language of the response")
    timestamp: str = Field(..., description="Response timestamp")
    user_id: str = Field(..., description="User ID from request")
    
    @classmethod
    def create(cls, response: str, language: str, user_id: str) -> "ChatResponse":
        """Factory method to create a ChatResponse with current timestamp."""
        return cls(
            response=response,
            language=language,
            timestamp=datetime.now().isoformat(),
            user_id=user_id
        )


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Health status")
    timestamp: str = Field(..., description="Check timestamp")


class LanguagesResponse(BaseModel):
    """Supported languages response model."""
    supported_languages: List[str] = Field(..., description="List of supported language codes")
    default_language: str = Field(..., description="Default language code")
