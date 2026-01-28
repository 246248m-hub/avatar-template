import os
import re
from pathlib import Path

# Global configuration (can be expanded)
GENERATED_APKS_DIR = Path("generated_apks")
TEMP_DIR = Path("temp_apk_build")
KNOWLEDGE_BASE_DIR = Path("knowledge_base")

class ArabicTextProcessor:
    """
    A module to process and generate Arabic text, including parsing and
    synthesizing content relevant to APK generation.
    """
    def __init__(self, knowledge_base_dir: Path):
        self.knowledge_base_dir = knowledge_base_dir
        self.arabic_grammar_rules = self._load_grammar_rules()
        self.apk_component_keywords = self._load_apk_keywords()

    def _load_grammar_rules(self) -> dict:
        """
        Loads Arabic grammar rules from a file.
        (Placeholder: In a real scenario, this would parse a grammar file)
        """
        print("Loading Arabic grammar rules...")
        # Example: basic rules for sentence structure related to app components
        return {
            "sentence_structure": [
                "{noun} {verb} {object}",
                "{noun} {adjective}",
                "إنشاء {component_type}",
                "تعديل {component_type} في {app_name}"
            ],
            "verb_conjugations": {
                "create": ["ينشئ", "يخلق"],
                "modify": ["يعدل", "يغير"]
            },
            "noun_types": {
                "component_type": ["شاشة", "خدمة", "مستقبل بث", "موفر محتوى"],
                "app_name": ["التطبيق", "النظام"]
            }
        }

    def _load_apk_keywords(self) -> dict:
        """
        Loads keywords related to APK components and structure.
        (Placeholder: In a real scenario, this would parse a configuration file)
        """
        print("Loading APK component keywords...")
        return {
            "activity": ["شاشة", "واجهة", "نافذة"],
            "service": ["خدمة", "معالج خلفي"],
            "receiver": ["مستقبل بث", "معالج أحداث"],
            "provider": ["موفر محتوى", "مصدر بيانات"]
        }

    def parse_arabic_request(self, prompt: str) -> dict:
        """
        Parses an Arabic natural language prompt to identify intent and entities
        related to APK generation.
        """
        print(f"Parsing Arabic prompt: '{prompt}'")
        parsed_data = {
            "intent": None,
            "components": [],
            "app_name": None
        }

        # Simple keyword-based intent detection
        if "إنشاء" in prompt or "بناء" in prompt:
            parsed_data["intent"] = "create_apk_component"
        elif "تعديل" in prompt or "تغيير" in prompt:
            parsed_data["intent"] = "modify_apk_component"

        # Identify component types
        for component_type, keywords in self.apk_component_keywords.items():
            for keyword in keywords:
                if keyword in prompt:
                    parsed_data["components"].append({"type": component_type, "name": None}) # Name extraction can be more complex

        # Identify app name (basic example)
        app_name_match = re.search(r"في ([\w\s]+)$", prompt)
        if app_name_match:
            parsed_data["app_name"] = app_name_match.group(1).strip()

        # More sophisticated NLP would involve:
        # - Part-of-speech tagging
        # - Named entity recognition
        # - Dependency parsing
        # - Semantic role labeling

        print(f"Parsed data: {parsed_data}")
        return parsed_data

    def generate_arabic_description(self, parsed_data: dict) -> str:
        """
        Generates an Arabic description based on parsed data, for example,
        describing a component to be created or modified.
        """
        if not parsed_data.get("intent"):
            return "لم يتم فهم الغرض من الطلب."

        intent = parsed_data["intent"]
        components = parsed_data.get("components", [])
        app_name = parsed_data.get("app_name", "التطبيق")

        description_parts = []
        if intent == "create_apk_component":
            description_parts.append(f"سيتم إنشاء مكونات جديدة لـ {app_name}.")
            if components:
                component_descriptions = []
                for component in components:
                    component_type_arabic = next((k for k, v in self.apk_component_keywords.items() if v and component["type"] in self.apk_component_keywords and component["type"] == k), component["type"])
                    component_descriptions.append(f"  - {component_type_arabic}")
                description_parts.append("المكونات المقترحة:")
                description_parts.extend(component_descriptions)
        elif intent == "modify_apk_component":
            description_parts.append(f"سيتم تعديل مكونات في {app_name}.")
            if components:
                component_descriptions = []
                for component in components:
                    component_type_arabic = next((k for k, v in self.apk_component_keywords.items() if v and component["type"] in self.apk_component_keywords and component["type"] == k), component["type"])
                    component_descriptions.append(f"  - {component_type_arabic}")
                description_parts.append("المكونات التي سيتم تعديلها:")
                description_parts.extend(component_descriptions)
        else:
            description_parts.append("الغرض غير معروف.")

        return " ".join(description_parts)

    def extract_component_details_from_text(self, text: str) -> list:
        """
        Extracts specific details about APK components (like name, properties)
        from a block of Arabic text. This would be more complex than simple parsing.
        """
        extracted_components = []
        # This is a simplified example. Real implementation would involve
        # more robust parsing techniques.
        component_pattern = re.compile(r"(?:إنشاء|تعديل)\s+(?:ال)?([\w\s]+?)\s+(?:لـ|في)\s+([\w\s]+)", re.IGNORECASE)
        matches = component_pattern.findall(text)

        for component_name, app_context in matches:
            component_type = None
            for c_type, keywords in self.apk_component_keywords.items():
                if any(keyword in component_name for keyword in keywords):
                    component_type = c_type
                    break
            if component_type:
                extracted_components.append({
                    "type": component_type,
                    "name": component_name.strip(),
                    "app_context": app_context.strip()
                })
        return extracted_components

def create_apk_structure_files(component_type: str, component_name: str, app_name: str):
    """
    Creates dummy files representing an APK component structure.
    """
    if not GENERATED_APKS_DIR.exists():
        GENERATED_APKS_DIR.mkdir(parents=True)

    app_dir = GENERATED_APKS_DIR / app_name.replace(" ", "_").lower()
    if not app_dir.exists():
        app_dir.mkdir()

    component_dir = app_dir / component_type.lower()
    if not component_dir.exists():
        component_dir.mkdir()

    # Create a dummy file for the component
    component_file = component_dir / f"{component_name.replace(' ', '_').lower()}.dummy"
    with open(component_file, "w", encoding="utf-8") as f:
        f.write(f"# Dummy file for {component_type}: {component_name} in app: {app_name}\n")
        f.write(f"// This represents the structure of an APK component.\n")
        f.write(f"// Further logic will define its actual content.\n")
    print(f"Created dummy component file: {component_file}")
    return component_file

def cleanup_generated_apk_structures():
    """
    Cleans up the generated dummy APK structure directories.
    """
    print("Cleaning up generated APK structures...")
    if GENERATED_APKS_DIR.exists():
        import shutil
        shutil.rmtree(GENERATED_APKS_DIR)
        print(f"Removed directory: {GENERATED_APKS_DIR}")

def demo_arabic_processing_and_apk_struct_generation():
    """
    Demonstrates the Arabic Text Processor and its integration with APK structure generation.
    """
    print("\n--- Initiating Arabic Parser and Generator Module Demo ---")

    arabic_processor = ArabicTextProcessor(KNOWLEDGE_BASE_DIR)

    # --- Test Case 1: Parsing and Generating Description ---
    print("\n--- Test Case 1: Parsing and Generating Description ---")
    test_prompt_1 = "إنشاء شاشة تسجيل الدخول في تطبيق التسوق"
    parsed_data_1 = arabic_processor.parse_arabic_request(test_prompt_1)
    generated_description_1 = arabic_processor.generate_arabic_description(parsed_data_1)
    print(f"Prompt: '{test_prompt_1}'")
    print(f"Generated Description: {generated_description_1}")

    test_prompt_2 = "تعديل خدمة الإشعارات في نظام المراسلة"
    parsed_data_2 = arabic_processor.parse_arabic_request(test_prompt_2)
    generated_description_2 = arabic_processor.generate_arabic_description(parsed_data_2)
    print(f"\nPrompt: '{test_prompt_2}'")
    print(f"Generated Description: {generated_description_2}")

    # --- Test Case 2: Generating APK Structure Files ---
    print("\n--- Test Case 2: Generating APK Structure Files ---")
    test_prompt_3 = "بناء واجهة رئيسية لتطبيق إدارة المهام"
    parsed_data_3 = arabic_processor.parse_arabic_request(test_prompt_3)
    print(f"Parsed data for prompt '{test_prompt_3}': {parsed_data_3}")

    if parsed_data_3["intent"] == "create_apk_component" and parsed_data_3["components"]:
        # Assuming we create the first identified component
        component_info = parsed_data_3["components"][0]
        component_type = component_info["type"]
        # Attempt to infer a name if not explicitly parsed
        component_name_guess = "default_component_name"
        if "شاشة" in test_prompt_3:
            component_name_guess = "main_screen"
        elif "خدمة" in test_prompt_3:
            component_name_guess = "background_service"

        # Extracting a more specific name if possible (simple regex)
        name_match = re.search(r"(?:إنشاء|بناء)\s+(?:ال)?([\w\s]+?)(?:\s+في|\s+لـ)", test_prompt_3)
        if name_match:
            component_name_guess = name_match.group(1).strip()

        app_name = parsed_data_3.get("app_name", "my_application")

        created_file = create_apk_structure_files(component_type, component_name_guess, app_name)
        if created_file and created_file.exists():
            print(f"Successfully generated APK structure file for '{component_name_guess}'.")
        else:
            print(f"Failed to generate APK structure file for '{component_name_guess}'.")
    else:
        print("Could not generate APK structure: Intent not recognized or no components found.")

    # --- Test Case 3: Extracting Component Details from Text ---
    print("\n--- Test Case 3: Extracting Component Details from Text ---")
    arabic_text_for_extraction = """
    لقد قررت إنشاء شاشة للمستخدمين الجدد في نظام إدارة العملاء.
    أيضاً، نحتاج لتعديل خدمة الخلفية المسؤولة عن إرسال التنبيهات في تطبيق التذكيرات.
    """
    extracted_details = arabic_processor.extract_component_details_from_text(arabic_text_for_extraction)
    print(f"Text for extraction:\n{arabic_text_for_extraction}")
    print(f"Extracted component details: {extracted_details}")

    # Verify creation and cleanup
    if GENERATED_APKS_DIR.exists():
        print(f"\nDirectory '{GENERATED_APKS_DIR}' exists after generation.")
    else:
        print(f"\nDirectory '{GENERATED_APKS_DIR}' does NOT exist after generation (unexpected).")

    cleanup_generated_apk_structures()

    if not GENERATED_APKS_DIR.exists():
        print("Cleanup successful.")
    else:
        print("Cleanup failed.")

    print("\n--- Arabic Parser and Generator Module Demo Finished ---")

# Execute the demo
if __name__ == "__main__":
    # Ensure necessary directories exist for the demo
    KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)
    GENERATED_APKS_DIR.mkdir(exist_ok=True) # Created and cleaned up within demo

    demo_arabic_processing_and_apk_struct_generation()