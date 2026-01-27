import os
import re

class ArabicParser:
    """
    A module for parsing and understanding Arabic natural language.
    This is a simplified parser focusing on identifying core intents and entities.
    """

    def __init__(self):
        self.arabic_stopwords = set([
            "و", "في", "من", "إلى", "على", "عن", "بـ", "لـ", "كـ", "أن", "أنّ", "إن", "إنّ",
            "كان", "كانت", "يكون", "تكون", "ما", "متى", "كيف", "أين", "من", "ماذا", "هل",
            "ال", "ـه", "ـها", "ـك", "ـها", "ـي", "ـنا", "ـكم", "ـهم", "ـهن", "ا", "ـوا",
            "ـو", "ـي", "ـون", "ـين", "ـات", "ـة", "ـت", "ـان", "ـان", "ـون", "ـاء", "ـاء",
            "ـر", "ـس", "ـف", "ـق", "ـل", "ـم", "ـن", "ـه", "ـو", "ـي"
        ])
        self.intent_keywords = {
            "create_app": ["إنشاء", "تطوير", "بناء", "عمل", "صنع"],
            "add_feature": ["إضافة", "تضمين", "وضع", "إلحاق"],
            "remove_feature": ["إزالة", "حذف", "تخطي", "عدم"],
            "update_ui": ["تحديث", "تغيير", "تصميم", "واجهة"],
            "deploy_app": ["نشر", "إطلاق", "رفع", "تشغيل"]
        }
        self.entity_patterns = {
            "app_name": r"اسم التطبيق هو ([\w\s]+)",
            "feature_name": r"ميزة ([\w\s]+)",
            "ui_element": r"(زر|صورة|نص|قائمة|نموذج) ([\w\s]+)",
            "language": r"بلغة ([\w\s]+)",
            "platform": r"على (أندرويد|ios|ويندوز|لينكس|ماك)"
        }

    def tokenize(self, text: str) -> list[str]:
        """Basic Arabic tokenization, removing common punctuation and stopwords."""
        text = text.lower()
        # Remove common punctuation
        text = re.sub(r'[^\w\s Arabic]', '', text)
        tokens = text.split()
        return [token for token in tokens if token not in self.arabic_stopwords and len(token) > 1]

    def analyze_intent(self, tokens: list[str]) -> str | None:
        """Identifies the primary intent based on keywords."""
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in tokens:
                    return intent
        return None

    def extract_entities(self, text: str) -> dict[str, str]:
        """Extracts entities from the text using defined patterns."""
        entities = {}
        for entity_type, pattern in self.entity_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if entity_type == "ui_element":
                    # For UI elements, capture both the type and the name
                    entities[entity_type] = {"type": match.group(1), "name": match.group(2).strip()}
                else:
                    entities[entity_type] = match.group(1).strip()
        return entities

    def parse(self, natural_language_input: str) -> dict:
        """
        Parses Arabic natural language input to identify intent and entities.

        Args:
            natural_language_input: The Arabic text to parse.

        Returns:
            A dictionary containing the identified intent and extracted entities.
        """
        tokens = self.tokenize(natural_language_input)
        intent = self.analyze_intent(tokens)
        entities = self.extract_entities(natural_language_input)

        return {
            "original_input": natural_language_input,
            "tokens": tokens,
            "intent": intent,
            "entities": entities
        }

class ArabicNLPModule:
    """
    Encapsulates Arabic Natural Language Processing functionalities.
    This module acts as a bridge between raw Arabic text and structured data
    that other lobes can understand.
    """

    def __init__(self):
        self.parser = ArabicParser()

    def process_arabic_request(self, arabic_text: str) -> dict:
        """
        Processes a raw Arabic text request, performing parsing and analysis.

        Args:
            arabic_text: The natural language Arabic input string.

        Returns:
            A structured dictionary containing the parsed intent, entities,
            and original input.
        """
        if not arabic_text:
            return {"error": "No Arabic text provided."}

        parsed_data = self.parser.parse(arabic_text)
        print(f"\n--- Arabic NLP Processing Result ---")
        print(f"Original Input: {parsed_data['original_input']}")
        print(f"Tokens: {parsed_data['tokens']}")
        print(f"Identified Intent: {parsed_data['intent']}")
        print(f"Extracted Entities: {parsed_data['entities']}")
        print(f"------------------------------------")

        return parsed_data

    def cleanup_arabic_resources(self):
        """
        Placeholder for cleaning up any Arabic-specific temporary files or models
        that might be generated or used by the parser.
        In a real scenario, this would involve file system operations.
        """
        print("\n--- Cleaning up Arabic NLP module resources ---")
        # Example: os.remove("temp_arabic_model.pkl") if it existed
        print("Arabic NLP resources cleaned up (simulated).")
        print("---------------------------------------------")

if __name__ == '__main__':
    # --- Demo of ArabicNLPModule ---
    print("--- Starting ArabicNLPModule Demo ---")

    arabic_nlp_module = ArabicNLPModule()

    # Test Case 1: Creating an app with a name and platform
    test_prompt_1 = "أريد إنشاء تطبيق اسمه 'مديري اليومي' على منصة أندرويد."
    result_1 = arabic_nlp_module.process_arabic_request(test_prompt_1)

    # Test Case 2: Adding a feature to an existing app
    test_prompt_2 = "أضف ميزة تسجيل الدخول باستخدام جوجل إلى التطبيق."
    result_2 = arabic_nlp_module.process_arabic_request(test_prompt_2)

    # Test Case 3: Updating UI element
    test_prompt_3 = "قم بتغيير لون زر 'ابدأ' إلى الأزرق."
    result_3 = arabic_nlp_module.process_arabic_request(test_prompt_3)

    # Test Case 4: Removing a feature
    test_prompt_4 = "أزل خاصية الإشعارات من التطبيق."
    result_4 = arabic_nlp_module.process_arabic_request(test_prompt_4)

    # Test Case 5: Deploying an app
    test_prompt_5 = "نشر التطبيق الجديد على متجر جوجل بلاي."
    result_5 = arabic_nlp_module.process_arabic_request(test_prompt_5)

    # Simulate cleanup
    arabic_nlp_module.cleanup_arabic_resources()

    print("\n--- ArabicNLPModule Demo Finished ---")