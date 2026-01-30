import os
import json
import re

# Assume these are defined elsewhere or passed as parameters
KNOWLEDGE_BASE_DIR = "knowledge_base"
APP_STRUCTURE_DIR = "app_structures"

class ArabicNLPModule:
    """
    A module designed to parse and generate Arabic natural language,
    with a focus on understanding app structure and generating code-related text.
    """

    def __init__(self):
        self.arabic_parser = ArabicParser()
        self.arabic_generator = ArabicGenerator()

    def process_arabic_instruction(self, instruction: str) -> dict:
        """
        Parses an Arabic instruction to extract app structure components.

        Args:
            instruction: The Arabic natural language instruction.

        Returns:
            A dictionary representing the parsed app structure.
        """
        parsed_data = self.arabic_parser.parse_instruction(instruction)
        return parsed_data

    def generate_arabic_description(self, app_structure: dict) -> str:
        """
        Generates an Arabic description of an app structure.

        Args:
            app_structure: A dictionary representing the app structure.

        Returns:
            An Arabic natural language description of the app.
        """
        description = self.arabic_generator.generate_description(app_structure)
        return description

    def extract_intent_and_entities(self, arabic_text: str) -> dict:
        """
        Extracts user intent and relevant entities from Arabic text.

        Args:
            arabic_text: The Arabic text input from the user.

        Returns:
            A dictionary containing the identified intent and entities.
        """
        # This is a placeholder for a more sophisticated intent/entity extraction
        # that would likely involve a dedicated NLU model.
        # For this example, we'll simulate some basic keyword-based extraction.
        intent = "unknown"
        entities = {}

        if "إنشاء تطبيق" in arabic_text or "صنع تطبيق" in arabic_text:
            intent = "create_app"
            # Example: Extract app name
            match = re.search(r'(?:تطبيق|اسم التطبيق)\s+["\']?([^"\']+?)["\']?', arabic_text)
            if match:
                entities["app_name"] = match.group(1).strip()
            # Example: Extract main feature
            match = re.search(r'(?:ميزة رئيسية|وظيفة أساسية)\s+["\']?([^"\']+?)["\']?', arabic_text)
            if match:
                entities["main_feature"] = match.group(1).strip()

        elif "تعديل تطبيق" in arabic_text or "تحديث تطبيق" in arabic_text:
            intent = "modify_app"
            match = re.search(r'(?:تطبيق|اسم التطبيق)\s+["\']?([^"\']+?)["\']?', arabic_text)
            if match:
                entities["app_name"] = match.group(1).strip()

        elif "وصف" in arabic_text and "تطبيق" in arabic_text:
            intent = "describe_app"
            match = re.search(r'(?:تطبيق|اسم التطبيق)\s+["\']?([^"\']+?)["\']?', arabic_text)
            if match:
                entities["app_name"] = match.group(1).strip()

        return {"intent": intent, "entities": entities}


class ArabicParser:
    """
    Parses Arabic natural language instructions to understand app structure elements.
    This is a simplified parser for demonstration.
    """
    def __init__(self):
        # Load pre-trained models or rules for Arabic parsing if available
        pass

    def parse_instruction(self, instruction: str) -> dict:
        """
        Parses an Arabic instruction string into a structured dictionary.
        This is a simplified example and would need to be much more robust
        for real-world applications.
        """
        app_structure = {
            "name": "UntitledApp",
            "description": "",
            "screens": [],
            "features": [],
            "data_models": []
        }

        # Simplified parsing based on keywords and common Arabic app development terms
        if "إنشاء تطبيق" in instruction or "صنع تطبيق" in instruction:
            match = re.search(r'(?:اسم التطبيق|تطبيق)\s+["\']?([^"\']+?)["\']?', instruction)
            if match:
                app_structure["name"] = match.group(1).strip()

            match = re.search(r'(?:وصف التطبيق|الهدف منه)\s+["\']?([^"\']+?)["\']?', instruction)
            if match:
                app_structure["description"] = match.group(1).strip()

            # Parse screens
            screens_match = re.findall(r'شاشة\s+["\']?([^"\']+?)["\']?(?:\s+تحتوي على\s+["\']?([^"\']+?)["\']?)?', instruction)
            for screen_name, screen_content in screens_match:
                screen_data = {"name": screen_name.strip()}
                if screen_content:
                    screen_data["components"] = [c.strip() for c in screen_content.split(',')]
                app_structure["screens"].append(screen_data)

            # Parse features
            features_match = re.findall(r'ميزة\s+["\']?([^"\']+?)["\']?(?:\s+تقوم بـ\s+["\']?([^"\']+?)["\']?)?', instruction)
            for feature_name, feature_desc in features_match:
                feature_data = {"name": feature_name.strip()}
                if feature_desc:
                    feature_data["description"] = feature_desc.strip()
                app_structure["features"].append(feature_data)

            # Parse data models
            models_match = re.findall(r'نموذج بيانات\s+["\']?([^"\']+?)["\']?(?:\s+له حقول\s+["\']?([^"\']+?)["\']?)?', instruction)
            for model_name, model_fields in models_match:
                model_data = {"name": model_name.strip()}
                if model_fields:
                    model_data["fields"] = [f.strip() for f in model_fields.split(',')]
                app_structure["data_models"].append(model_data)

        return app_structure


class ArabicGenerator:
    """
    Generates Arabic natural language text from structured data.
    This is a simplified generator for demonstration.
    """
    def __init__(self):
        # Load pre-trained models or rules for Arabic generation if available
        pass

    def generate_description(self, app_structure: dict) -> str:
        """
        Generates an Arabic description of an app from its structure.
        """
        description_parts = []
        description_parts.append(f"تطبيق باسم: {app_structure.get('name', 'غير محدد')}.")
        if app_structure.get('description'):
            description_parts.append(f"الهدف منه: {app_structure['description']}.")

        if app_structure.get('screens'):
            description_parts.append("يحتوي على الشاشات التالية:")
            for screen in app_structure['screens']:
                screen_desc = f"- شاشة '{screen.get('name', 'غير محدد')}'"
                if screen.get('components'):
                    screen_desc += f" تحتوي على: {', '.join(screen['components'])}"
                description_parts.append(screen_desc)

        if app_structure.get('features'):
            description_parts.append("ويوفر الميزات التالية:")
            for feature in app_structure['features']:
                feature_desc = f"- ميزة '{feature.get('name', 'غير محدد')}'"
                if feature.get('description'):
                    feature_desc += f" تقوم بـ: {feature['description']}"
                description_parts.append(feature_desc)

        if app_structure.get('data_models'):
            description_parts.append("مع نماذج البيانات التالية:")
            for model in app_structure['data_models']:
                model_desc = f"- نموذج '{model.get('name', 'غير محدد')}'"
                if model.get('fields'):
                    model_desc += f" له حقول: {', '.join(model['fields'])}"
                description_parts.append(model_desc)

        return "\n".join(description_parts)

# --- Example Usage and Integration Demonstration ---

if __name__ == "__main__":
    # This block is for demonstration purposes and would typically not run
    # when this module is imported and used by another lobe.

    print("--- Demonstrating Arabic NLP Module ---")

    arabic_nlp_module = ArabicNLPModule()

    # Example 1: Parsing an Arabic instruction to create an app structure
    instruction_create_app = (
        "إنشاء تطبيق باسم 'مدير المهام'. "
        "وصف التطبيق 'لتنظيم المهام اليومية'. "
        "شاشة 'القائمة الرئيسية' تحتوي على 'عرض المهام، إضافة مهمة'. "
        "شاشة 'تفاصيل المهمة' تحتوي على 'عنوان، وصف، تاريخ استحقاق'. "
        "ميزة 'إضافة مهمة' تقوم بـ 'إدخال تفاصيل مهمة جديدة'. "
        "نموذج بيانات 'مهمة' له حقول 'معرف، عنوان، وصف، حالة، تاريخ الإنشاء'."
    )
    print(f"\n--- Parsing Arabic Instruction ---")
    print(f"Instruction: {instruction_create_app}")
    parsed_app_structure = arabic_nlp_module.process_arabic_instruction(instruction_create_app)
    print("\nParsed App Structure:")
    print(json.dumps(parsed_app_structure, indent=4, ensure_ascii=False))

    # Example 2: Generating Arabic description from an app structure
    if parsed_app_structure:
        print(f"\n--- Generating Arabic Description ---")
        generated_arabic_desc = arabic_nlp_module.generate_arabic_description(parsed_app_structure)
        print("Generated Description:")
        print(generated_arabic_desc)

    # Example 3: Extracting intent and entities from Arabic text
    user_query_1 = "أريد إنشاء تطبيق جديد لإدارة المخزون"
    user_query_2 = "ما هي ميزات تطبيق 'مفكرة الملاحظات'؟"
    user_query_3 = "تعديل تطبيق 'حاسبة الرواتب'"

    print(f"\n--- Extracting Intent and Entities ---")
    intent_entities_1 = arabic_nlp_module.extract_intent_and_entities(user_query_1)
    print(f"Query: '{user_query_1}' -> {intent_entities_1}")

    intent_entities_2 = arabic_nlp_module.extract_intent_and_entities(user_query_2)
    print(f"Query: '{user_query_2}' -> {intent_entities_2}")

    intent_entities_3 = arabic_nlp_module.extract_intent_and_entities(user_query_3)
    print(f"Query: '{user_query_3}' -> {intent_entities_3}")


    print("\n--- Arabic NLP Module Demonstration Finished ---")