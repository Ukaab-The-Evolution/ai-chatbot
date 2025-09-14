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


class SpeechRequest(BaseModel):
    """Speech synthesis request parameters."""
    include_speech: bool = Field(False, description="Whether to include speech synthesis")
    speech_language: Optional[str] = Field(None, description="Language for speech synthesis (english, urdu, punjabi)")


class SpeechResponse(BaseModel):
    """Speech synthesis response data."""
    mime_type: str = Field(..., description="MIME type of the audio data")
    data_url: str = Field(..., description="Base64 encoded audio data URL")


class Attachment(BaseModel):
    """Attachment model for file uploads."""
    type: str = Field(..., description="Type of attachment (pdf, image, etc.)")
    url: str = Field(..., description="URL of the attachment")
    filename: str = Field(..., description="Filename of the attachment")


class ChatRequest(BaseModel):
    """Chat request model for incoming messages."""
    user_id: str = Field(..., description="Unique identifier for the user")
    role: str = Field(..., description="Role of the message sender")
    message: Optional[str] = Field(None, description="The chat message (optional if audio_stream provided)")
    audio_stream: Optional[str] = Field(None, description="Base64 encoded audio data for voice input")
    context: Optional[Context] = Field(None, description="Additional context information")
    attachments: Optional[List[Attachment]] = Field(None, description="File attachments")
    location: Optional[Location] = Field(None, description="User location")
    timestamp: str = Field(..., description="Timestamp of the message")
    include_speech: bool = Field(False, description="Whether to include speech synthesis in response")
    speech_language: Optional[str] = Field(None, description="Language for speech synthesis (english, urdu, punjabi)")


class LogisticsData(BaseModel):
    """Structured logistics data extracted from messages."""
    origin: Optional[str] = Field(None, description="Origin location")
    destination: Optional[str] = Field(None, description="Destination location")
    pick_up_time: Optional[str] = Field(None, description="Pickup time/date")
    cargo_type: Optional[str] = Field(None, description="Type of cargo")
    weight: Optional[str] = Field(None, description="Weight of cargo")
    special_requirements: Optional[str] = Field(None, description="Special handling requirements")
    payment_offer: Optional[str] = Field(None, description="Payment amount offered")
    number_of_trucks: Optional[int] = Field(None, description="Number of trucks needed")
    is_pooling: Optional[bool] = Field(None, description="Whether cargo pooling is available")


class ChatResponse(BaseModel):
    """Chat response model for outgoing messages."""
    response: Optional[str] = Field(None, description="AI generated response message")
    language: str = Field(..., description="Language of the response")
    timestamp: str = Field(..., description="Response timestamp")
    user_id: str = Field(..., description="User ID from request")
    speech: Optional[SpeechResponse] = Field(None, description="Speech synthesis data if requested")
    data: Optional[LogisticsData] = Field(None, description="Structured logistics data if parsed from message")
    
    @classmethod
    def create(
        cls, 
        response: Optional[str], 
        language: str, 
        user_id: str, 
        speech: Optional[SpeechResponse] = None,
        data: Optional[LogisticsData] = None
    ) -> "ChatResponse":
        """Factory method to create a ChatResponse with current timestamp."""
        return cls(
            response=response,
            language=language,
            timestamp=datetime.now().isoformat(),
            user_id=user_id,
            speech=speech,
            data=data
        )


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Health status")
    timestamp: str = Field(..., description="Check timestamp")


class LanguagesResponse(BaseModel):
    """Supported languages response model."""
    supported_languages: List[str] = Field(..., description="List of supported language codes")
    default_language: str = Field(..., description="Default language code")
