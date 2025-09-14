"""
Response schemas and JSON structures for structured data extraction.
Following Single Responsibility Principle - handles only response format definitions.
"""

from typing import Dict


class LogisticsResponseSchema:
    """
    Defines the JSON response schema for logistics data extraction.
    Centralizes the structure for better maintainability.
    """
    
    @staticmethod
    def get_json_schema() -> str:
        """
        Get the JSON schema structure for logistics responses.
        
        Returns:
            JSON schema as string
        """
        return """{
  "response": "Your helpful response message (optional - only if you need to ask questions or provide general advice)",
  "data": {
    "origin": "pickup location if mentioned",
    "destination": "delivery location if mentioned", 
    "pick_up_time": "pickup date/time if mentioned",
    "cargo_type": "type of goods if mentioned",
    "weight": "cargo weight if mentioned",
    "special_requirements": "special handling needs if mentioned",
    "payment_offer": "payment amount if mentioned",
    "number_of_trucks": "number of trucks needed if mentioned",
    "is_pooling": "true/false if cargo pooling mentioned"
  }
}"""
    
    @staticmethod
    def get_json_instructions(language: str) -> str:
        """
        Get language-specific JSON formatting instructions.
        
        Args:
            language: Language code
            
        Returns:
            Formatted JSON instructions for the specified language
        """
        schema = LogisticsResponseSchema.get_json_schema()
        
        instructions = {
            "english": f"""Always respond in JSON format using this exact schema:

{schema}

If no logistics data is found, set "data" to null and provide a helpful response in "response". 
Extract only information explicitly mentioned in the user's message.""",

            "urdu": f"""ہمیشہ اس JSON فارمیٹ میں جواب دیں:

{schema}

اگر کوئی لاجسٹکس ڈیٹا نہیں ملا تو "data" کو null رکھیں اور "response" میں مددگار جواب دیں۔
صرف وہی معلومات نکالیں جو صارف کے پیغام میں واضح طور پر ذکر ہوں۔""",

            "punjabi": f"""ہمیشہ اس JSON فارمیٹ وچ جواب دیو:

{schema}

جے کوئی لاجسٹکس ڈیٹا نہیں ملیا تاں "data" نوں null رکھو تے "response" وچ مددگار جواب دیو۔""",

            "pushto": f"""تل په دغه JSON بڼه ځواب ورکړئ:

{schema}

که هیڅ لاجستیک ډیټا ونه موندل شوه، "data" ته null ورکړئ او په "response" کې مرستندوی ځواب ورکړئ۔""",

            "balochi": f"""هميشه ءِ اے JSON ءِ شکل ءِ اے جواب دیت:

{schema}

اگر کانت لاجسٹک ڈیٹا نہ اِنت، "data" ءَ null بکنیت ءُ "response" ءِ اے کمک ءِ جواب دیت۔""",

            "saraiki": f"""ہمیشہ ایں JSON فارمیٹ وچ جواب ڈیو:

{schema}

جے کوئی لاجسٹکس ڈیٹا کونا ملے تاں "data" نوں null رکھو تے "response" وچ مددگار جواب ڈیو۔"""
        }
        
        return instructions.get(language, instructions["english"])
    
    @staticmethod
    def get_supported_fields() -> Dict[str, str]:
        """
        Get the supported logistics data fields with descriptions.
        
        Returns:
            Dictionary mapping field names to descriptions
        """
        return {
            "origin": "Pickup location",
            "destination": "Delivery location",
            "pick_up_time": "Pickup date/time",
            "cargo_type": "Type of goods",
            "weight": "Cargo weight",
            "special_requirements": "Special handling needs",
            "payment_offer": "Payment amount",
            "number_of_trucks": "Number of trucks needed",
            "is_pooling": "Whether cargo pooling is mentioned"
        }
