"""
Robust Gemini service wrapper with an offline fallback.
If the google-genai package and GEMINI_API_KEY are present, it will use Gemini.
Otherwise it runs a lightweight local fallback responder so the chatbot works offline.
"""

import logging
from typing import Dict, Optional

from ..core.config import settings, language_config
from .interfaces import ChatServiceInterface

logger = logging.getLogger(__name__)

# Try to import google-genai lazily
try:
    from google import genai
    from google.genai import types  # type: ignore
    HAVE_GENAI = True
except Exception as e:
    HAVE_GENAI = False
    logger.info("google.genai not available; running in offline fallback mode.")

class GeminiChatService(ChatServiceInterface):
    """
    Chat service that uses the Google Gemini client when available and configured,
    otherwise falls back to a simple local responder.
    """
    def __init__(self):
        self.model = getattr(settings, "gemini_model", "gemini-2.5-flash")
        self.api_key = getattr(settings, "gemini_api_key", None)
        self.client = None
        self.use_fallback = not (HAVE_GENAI and self.api_key)
        if not self.use_fallback:
            try:
                # configure the genai client
                genai.configure(api_key=self.api_key)
                self.client = genai
                logger.info("Gemini client initialized")
            except Exception as e:
                logger.exception("Failed to initialize gemini client, switching to fallback: %s", e)
                self.use_fallback = True
        else:
            logger.info("Using local fallback chat service (no gemini client configured)")

    def generate_response(
        self, 
        message: str, 
        language: str, 
        context: Optional[Dict] = None, 
        user_id: str = ""
    ) -> str:
        """
        Generate a response. If Gemini is available, call it; otherwise produce a simple fallback reply.
        """
        # Sanitize inputs
        message = (message or "").strip()
        language = (language or "english").lower()

        if self.use_fallback:
            # very small rule-based fallback to keep the app functional offline
            if not message:
                return "Please send a message."
            lower = message.lower()
            if any(g in lower for g in ["hello","hi","assalam","سلام"]):
                return f"Hello! I am running in offline mode and received your message: '{message}'"
            if "time" in lower or "date" in lower:
                from datetime import datetime
                return f"Current server time is {datetime.now().isoformat()} (offline response)"
            # default echo
            return f"(Offline fallback) Echo: {message}"
        
        # If we get here, gemini client is available
        try:
            system_instruction = language_config.get_system_instruction(language)
            # Build content
            user_content = types.TextInput(text=message)
            config = types.GenerateTextConfig(max_tokens=512) if hasattr(types, "GenerateTextConfig") else None
            
            # Different genai versions have different APIs; try a few safe calls
            try:
                # try `models.generate` if available
                resp = self.client.models.generate(
                    model=self.model,
                    prompt=message
                )
                # resp may be complex; try to extract text
                if hasattr(resp, "text"):
                    out = getattr(resp, "text")
                    return str(out).strip()
                # fallback: string representation
                return str(resp)
            except Exception:
                # try generate_content_stream style (older/newer clients)
                try:
                    response_text = ""
                    for chunk in self.client.models.generate_content_stream(
                        model=self.model,
                        contents=[user_content],
                        config=config,
                    ):
                        response_text += getattr(chunk, "text", "") or ""
                    return response_text.strip()
                except Exception as e2:
                    logger.exception("Failed to call gemini client: %s", e2)
                    return f"(Gemini error) {e2}"
        except Exception as e:
            logger.exception("Unexpected error in generate_response: %s", e)
            return f"(Error) {e}"

    def get_supported_languages(self) -> list:
        return language_config.get_supported_languages()

    def get_default_language(self) -> str:
        return language_config.get_default_language()

    def normalize_language(self, language: Optional[str]) -> str:
        return language_config.normalize_language(language)
