import os
import re
import shutil
from pathlib import Path

# Define constants for Arabic characters and common patterns
ARABIC_ALPHABET = "ابتثجحخدذرزسشصضطظعغفقكلمنهويآأؤإئىة"
ARABIC_DIACRITICS = "ًٌٍَُِّْ"
ARABIC_PUNCTUATION = "،؛؟."
ARABIC_NUMBERS = "٠١٢٣٤٥٦٧٨٩"
ARABIC_IRREGULAR_SPACES = r"[\u00A0\u200B\u200C\u200D]"  # Non-breaking space, Zero-width non-joiner, etc.

class ArabicTextProcessor:
    """
    A module for processing and manipulating Arabic text, laying the groundwork
    for natural language understanding and code generation from Arabic prompts.
    """

    def __init__(self):
        """Initializes the ArabicTextProcessor."""
        self.normalized_arabic_chars = {
            'آ': 'ا', 'أ': 'ا', 'إ': 'ا', 'ؤ': 'و', 'ئ': 'ي', 'ى': 'ي', 'ة': 'ه'
        }

    def normalize_arabic_text(self, text: str) -> str:
        """
        Normalizes Arabic text by:
        1. Removing diacritics.
        2. Replacing common ligatures and variations with their base characters.
        3. Removing irregular spaces.
        4. Standardizing spacing.

        Args:
            text: The input Arabic string.

        Returns:
            A normalized Arabic string.
        """
        # 1. Remove diacritics
        text = re.sub(f"[{ARABIC_DIACRITICS}]", "", text)

        # 2. Replace variations with base characters
        for variant, base in self.normalized_arabic_chars.items():
            text = text.replace(variant, base)

        # 3. Remove irregular spaces
        text = re.sub(ARABIC_IRREGULAR_SPACES, " ", text)

        # 4. Standardize spacing (multiple spaces to single space) and trim
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def extract_arabic_keywords(self, text: str, keywords: list[str]) -> list[str]:
        """
        Extracts specific Arabic keywords from a normalized text.

        Args:
            text: The normalized Arabic string.
            keywords: A list of Arabic keywords to search for.

        Returns:
            A list of found Arabic keywords.
        """
        normalized_text = self.normalize_arabic_text(text)
        found_keywords = []
        for keyword in keywords:
            normalized_keyword = self.normalize_arabic_text(keyword)
            if normalized_keyword in normalized_text:
                found_keywords.append(keyword)
        return found_keywords

    def identify_arabic_commands(self, text: str) -> list[str]:
        """
        Identifies potential commands within Arabic text.
        This is a simplified approach; a more robust NLP model would be needed
        for complex command parsing.

        Args:
            text: The input Arabic string.

        Returns:
            A list of identified command phrases.
        """
        normalized_text = self.normalize_arabic_text(text)
        # Example: Looking for phrases starting with "أنشئ" (create), "عدّل" (modify), "احذف" (delete)
        # This would be expanded with more verbs and sentence structures.
        potential_commands = re.findall(r"\b(أنشئ|عدّل|احذف|ابحث عن)\b\s*(.*?)(?=[،؛.؟]|$)", normalized_text)
        commands = []
        for command_verb, command_argument in potential_commands:
            commands.append(f"{command_verb} {command_argument.strip()}")
        return commands

    def extract_arabic_parameters(self, text: str, parameter_patterns: dict[str, str]) -> dict[str, str]:
        """
        Extracts parameters from Arabic text based on predefined patterns.

        Args:
            text: The input Arabic string.
            parameter_patterns: A dictionary where keys are parameter names
                                (e.g., 'app_name', 'version') and values are
                                regular expression patterns to find them in Arabic.

        Returns:
            A dictionary of extracted parameter names and their values.
        """
        normalized_text = self.normalize_arabic_text(text)
        extracted_params = {}
        for param_name, pattern in parameter_patterns.items():
            # Ensure the pattern is also normalized if it contains Arabic variants
            normalized_pattern = self.normalize_arabic_text(pattern)
            match = re.search(normalized_pattern, normalized_text)
            if match:
                # Extract the value from the matched group, cleaning it further
                value = match.group(1).strip() if match.groups() else match.group(0).strip()
                extracted_params[param_name] = self.normalize_arabic_text(value)
        return extracted_params

    def generate_arabic_response(self, processed_data: dict) -> str:
        """
        Generates a simple Arabic response based on processed NLP data.
        This function acts as a basic feedback mechanism.

        Args:
            processed_data: A dictionary containing information derived from NLP processing.

        Returns:
            An Arabic response string.
        """
        response_parts = ["تم فهم طلبك."]
        if 'commands' in processed_data and processed_data['commands']:
            response_parts.append(f"الأوامر المكتشفة: {', '.join(processed_data['commands'])}.")
        if 'keywords' in processed_data and processed_data['keywords']:
            response_parts.append(f"الكلمات المفتاحية: {', '.join(processed_data['keywords'])}.")
        if 'parameters' in processed_data and processed_data['parameters']:
            params_str = ", ".join([f"{k}: {v}" for k, v in processed_data['parameters'].items()])
            response_parts.append(f"المعاملات المستخرجة: {params_str}.")

        return " ".join(response_parts)


def demo_arabic_text_processor():
    """
    Demonstrates the functionality of the ArabicTextProcessor module.
    This serves as an integration point towards understanding Arabic NLP.
    """
    print("\n--- Initiating ArabicTextProcessor Module Demo ---")
    processor = ArabicTextProcessor()

    # --- Test Case 1: Normalization ---
    print("\n--- Testing Text Normalization ---")
    arabic_text_with_variants = "أهلاً وسهلاً بكم يا عرب! هذا نصٌّ بهِ حركاتٌ وتشكيلاتٌ ولفظٌ مختلفٌ. ؤآإأىة"
    normalized_text = processor.normalize_arabic_text(arabic_text_with_variants)
    print(f"Original: {arabic_text_with_variants}")
    print(f"Normalized: {normalized_text}")
    expected_normalized = "اهلا وسهلا بكم يا عرب هذا نص به حركات وتشكيلات ولفظ مختلف ووااوااه ه" # Based on current normalization rules
    assert normalized_text == expected_normalized, f"Normalization failed. Expected: {expected_normalized}, Got: {normalized_text}"
    print("Normalization test passed.")

    # --- Test Case 2: Keyword Extraction ---
    print("\n--- Testing Keyword Extraction ---")
    search_text = "أريد إنشاء تطبيق جديد باسم 'سوق دوت كوم' يعمل على نظام أندرويد."
    keywords_to_find = ["تطبيق", "نظام", "اسم"]
    found = processor.extract_arabic_keywords(search_text, keywords_to_find)
    print(f"Text: {search_text}")
    print(f"Keywords to find: {keywords_to_find}")
    print(f"Found keywords: {found}")
    assert "تطبيق" in found and "نظام" in found, "Keyword extraction test failed."
    print("Keyword extraction test passed.")

    # --- Test Case 3: Command Identification ---
    print("\n--- Testing Command Identification ---")
    command_text = "أنشئ تطبيقاً جديداً. ثم عدّل الإعدادات. احذف النسخة القديمة."
    commands_found = processor.identify_arabic_commands(command_text)
    print(f"Text: {command_text}")
    print(f"Identified commands: {commands_found}")
    assert "أنشئ تطبيقاً جديداً" in commands_found, "Command identification test failed for 'أنشئ'."
    assert "عدّل الإعدادات" in commands_found, "Command identification test failed for 'عدّل'."
    assert "احذف النسخة القديمة" in commands_found, "Command identification test failed for 'احذف'."
    print("Command identification test passed.")

    # --- Test Case 4: Parameter Extraction ---
    print("\n--- Testing Parameter Extraction ---")
    param_text = "إنشاء تطبيق جديد اسمه 'مدير المهام' الإصدار 1.2.3 الوصف: أداة لتنظيم الأنشكالا"
    param_patterns = {
        "app_name": r"اسمه\s*'([^']+)'",
        "version": r"الإصدار\s*([\d.]+)",
        "description": r"الوصف:\s*(.*)"
    }
    extracted_params = processor.extract_arabic_parameters(param_text, param_patterns)
    print(f"Text: {param_text}")
    print(f"Parameter patterns: {param_patterns}")
    print(f"Extracted parameters: {extracted_params}")
    assert extracted_params.get("app_name") == "مدير المهام", "Parameter extraction test failed for 'app_name'."
    assert extracted_params.get("version") == "1.2.3", "Parameter extraction test failed for 'version'."
    # Note: 'الوصف' pattern might need adjustment for more complex Arabic sentences
    assert extracted_params.get("description") == "أداة لتنظيم الأشكالا", "Parameter extraction test failed for 'description'."
    print("Parameter extraction test passed.")

    # --- Test Case 5: Generating Response ---
    print("\n--- Testing Response Generation ---")
    sample_data = {
        'commands': ["إنشاء تطبيق"],
        'keywords': ["تطبيق", "نظام"],
        'parameters': {"app_name": "متجري", "version": "1.0"}
    }
    response = processor.generate_arabic_response(sample_data)
    print(f"Input data: {sample_data}")
    print(f"Generated response: {response}")
    assert "تم فهم طلبك" in response, "Response generation test failed."
    assert "الأوامر المكتشفة" in response, "Response generation test failed."
    assert "الكلمات المفتاحية" in response, "Response generation test failed."
    assert "المعاملات المستخرجة" in response, "Response generation test failed."
    print("Response generation test passed.")

    print("\n--- ArabicTextProcessor Module Demo Finished ---")

# Example of how this module would be called by other lobes
if __name__ == "__main__":
    demo_arabic_text_processor()