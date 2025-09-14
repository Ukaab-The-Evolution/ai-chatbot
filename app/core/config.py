"""
Core configuration and settings.
Following Single Responsibility Principle - handles only configuration.
"""

import os
import logging
from dotenv import load_dotenv
from typing import Dict

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(".env")


class Settings:
    """Application settings and configuration."""
    
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.port = int(os.environ.get("PORT", 8000))
        self.debug = os.environ.get("DEBUG", "false").lower() == "true"
        self.host = os.environ.get("HOST", "0.0.0.0")
        self.gemini_model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
        
        # Azure Speech Service settings
        self.azure_speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.azure_speech_region = os.getenv("AZURE_SPEECH_REGION")
        
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        if not self.azure_speech_key or not self.azure_speech_region:
            logger.warning("Azure Speech Service credentials not found - TTS will be disabled")
    
    @property
    def cors_origins(self) -> list:
        """Get CORS allowed origins."""
        origins = os.environ.get("CORS_ORIGINS", "*")
        if origins == "*":
            return ["*"]
        return [origin.strip() for origin in origins.split(",")]


class LanguageConfig:
    """Language-specific configuration and system instructions."""
    
    SYSTEM_INSTRUCTIONS: Dict[str, str] = {
        "english": """You are a helpful assistant for Pakistani truck drivers. Offer practical advice, safety tips, and support for life on the road. Be friendly, concise, and knowledgeable about trucking, logistics, and travel in Pakistan. Don't talk too much and don't be too verbose. Respond in English.""",
        
        "urdu": """آپ پاکستانی ٹرک ڈرائیوروں کے لیے ایک مددگار معاون ہیں۔ سڑک پر زندگی کے لیے عملی مشورے، حفاظتی تجاویز، اور مدد فراہم کریں۔ دوستانہ، مختصر، اور پاکستان میں ٹرکنگ، لاجسٹکس، اور سفر کے بارے میں جانکار بنیں۔ زیادہ بات نہ کریں اور زیادہ تفصیل میں نہ جائیں۔ اردو میں جواب دیں۔""",
        
        "punjabi": """ਤੁਸੀਂ ਪਾਕਿਸਤਾਨੀ ਟਰੱਕ ਡਰਾਈਵਰਾਂ ਲਈ ਇੱਕ ਸਹਾਇਕ ਸਹਾਇਕ ਹੋ। ਸੜਕ 'ਤੇ ਜ਼ਿੰਦਗੀ ਲਈ ਵਿਹਾਰਕ ਸਲਾਹ, ਸੁਰੱਖਿਆ ਸੁਝਾਅ, ਅਤੇ ਸਹਾਇਤਾ ਪ੍ਰਦਾਨ ਕਰੋ। ਦੋਸਤਾਨਾ, ਸੰਖੇਪ, ਅਤੇ ਪਾਕਿਸਤਾਨ ਵਿੱਚ ਟਰੱਕਿੰਗ, ਲੌਜਿਸਟਿਕਸ, ਅਤੇ ਯਾਤਰਾ ਬਾਰੇ ਜਾਣਕਾਰ ਬਣੋ। ਬਹੁਤ ਜ਼ਿਆਦਾ ਗੱਲ ਨਾ ਕਰੋ ਅਤੇ ਬਹੁਤ ਜ਼ਿਆਦਾ ਵਿਸਤਾਰ ਵਿੱਚ ਨਾ ਜਾਓ। ਪੰਜਾਬੀ ਵਿੱਚ ਜਵਾਬ ਦਿਓ।""",
        
        "balochi": """تو پاکستانی ٹرک ڈرایور ءَ ءِ کمک کنۆک ءِت۔ راہ ءِ سر زندگی ءَ کمک، محفوظی ءِ تجویز، ءُ مدد دیت۔ دوستانا، مختصر، ءُ پاکستان ءِ اے ٹرکنگ، لاجسٹکس، ءُ سپر ءِ بارا ءِ زانکار بت۔ زیات گپ مہ زن ءُ زیات جزئیات ءِ اے مہ رو۔ بلوچی ءِ اے جواب دیت۔""",
        
        "saraiki": """تساں پاکستانی ٹرک ڈرائیورں کیتے ہک مددگار معاون ہو۔ راہ تے زندگی کیتے عملی مشوریاں، حفاظت کیاں تجویزں، تے مدد فراہم کرو۔ دوستانہ، مختصر، تے پاکستان وچ ٹرکنگ، لاجسٹکس، تے سفر بارے جانکار بنو۔ ذیادہ گل بات نا کرو تے ذیادہ تفصیل وچ نا جاؤ۔ سرائیکی وچ جواب ڈیو۔""",
        
        "pushto": """تاسو د پاکستاني ټرک ډرایورانو لپاره یو ګټور مرستیال یاست. د سړک په ژوند کې عملي مشورې، د خوندیتوب لارښوونې، او ملاتړ وړاندې کړئ. دوستانه، لنډ، او د پاکستان د ټرکنګ، لاجستیک، او سفر په اړه پوه اوسئ. ډېر خبرې مه کوئ او ډېر تفصیل ته مه ځئ. په پښتو ځواب ورکړئ."""
    }
    
    DEFAULT_LANGUAGE = "english"
    
    @classmethod
    def get_supported_languages(cls) -> list:
        """Get list of supported language codes."""
        return list(cls.SYSTEM_INSTRUCTIONS.keys())
    
    @classmethod
    def get_system_instruction(cls, language: str) -> str:
        """Get system instruction for a specific language."""
        return cls.SYSTEM_INSTRUCTIONS.get(language, cls.SYSTEM_INSTRUCTIONS[cls.DEFAULT_LANGUAGE])
    
    @classmethod
    def is_language_supported(cls, language: str) -> bool:
        """Check if a language is supported."""
        return language in cls.SYSTEM_INSTRUCTIONS


# Global settings instance
settings = Settings()
language_config = LanguageConfig()
