"""
Gemini AI service implementation.
Following Single Responsibility Principle - handles only Gemini AI interactions.
"""

import logging
from typing import Dict, Optional
from google import genai
from google.genai import types

from ..core.config import settings, language_config
from .interfaces import ChatServiceInterface

# Configure logging
logger = logging.getLogger(__name__)


class GeminiChatService(ChatServiceInterface):
    """Gemini AI chat service implementation."""
    
    def __init__(self):
        """Initialize Gemini client."""
        try:
            self.client = genai.Client(api_key=settings.gemini_api_key)
            self.model = settings.gemini_model
            logger.info("Gemini client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {str(e)}")
            raise
    
    def generate_response(
        self, 
        message: str, 
        language: str, 
        context: Optional[Dict] = None, 
        user_id: str = ""
    ) -> str:
        """
        Generate AI response using Google Gemini.
        
        Args:
            message: The user message
            language: Language code for response
            context: Additional context information
            user_id: User identifier for logging
            
        Returns:
            Generated response text
            
        Raises:
            Exception: If response generation fails
        """
        try:
            # Get system instruction based on language
            system_instruction_text = language_config.get_system_instruction(language)
            
            # Add context information if available
            if context:
                context_info = self._format_context(context)
                system_instruction_text += context_info
            
            # Create system instruction
            system_instruction = types.Content(
                role="system",
                parts=[types.Part(text=system_instruction_text)]
            )
            
            # Create user message
            user_content = types.Content(
                role="user",
                parts=[types.Part(text=message)]
            )
            
            # Generate configuration
            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="text/plain"
            )
            
            # Generate response
            response_text = ""
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=[user_content],
                config=config,
            ):
                response_text += chunk.text or ""
            
            logger.info(f"Generated response for user {user_id} in {language}")
            return response_text.strip()
            
        except Exception as e:
            logger.error(f"Error generating response for user {user_id}: {str(e)}")
            raise Exception(f"Error generating response: {str(e)}")
    
    def _format_context(self, context: Dict) -> str:
        """Format context information for system instruction."""
        context_parts = []
        
        if context.get('screen'):
            context_parts.append(f"Screen: {context['screen']}")
        
        if context.get('entity_id'):
            context_parts.append(f"Entity ID: {context['entity_id']}")
        
        if context_parts:
            return f"\nAdditional context: {', '.join(context_parts)}"
        
        return ""
