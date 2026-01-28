import os
import shutil
from pathlib import Path

# --- Constants ---
KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
GENERATED_APKS_DIR = Path("./generated_apks")
DEMO_FILES_DIR = Path("./demo_files")

# --- Helper Functions ---
def setup_demo_environment():
    """Sets up directories and dummy files for demonstration."""
    KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)
    GENERATED_APKS_DIR.mkdir(exist_ok=True)
    DEMO_FILES_DIR.mkdir(exist_ok=True)

    # Create dummy Arabic text files
    with open(DEMO_FILES_DIR / "sample_arabic_input_1.txt", "w", encoding="utf-8") as f:
        f.write("إنشاء تطبيق أندرويد بسيط يعرض رسالة ترحيب.\n")
    with open(DEMO_FILES_DIR / "sample_arabic_input_2.txt", "w", encoding="utf-8") as f:
        f.write("إنشاء تطبيق يعرض قائمة بالعناصر.\n")
    with open(DEMO_FILES_DIR / "sample_arabic_input_3.txt", "w", encoding="utf-8") as f:
        f.write("إنشاء تطبيق يعرض صورة مع زر.\n")

    # Create dummy knowledge base files (for illustration, actual NLP would be more complex)
    with open(KNOWLEDGE_BASE_DIR / "layout_templates.json", "w", encoding="utf-8") as f:
        f.write('{"basic_welcome": {"layout": "TextView", "text": "Welcome!"}, "item_list": {"layout": "ListView"}, "image_with_button": {"layout": ["ImageView", "Button"]}}')
    with open(KNOWLEDGE_BASE_DIR / "component_mapping.json", "w", encoding="utf-8") as f:
        f.write('{"app": "Application", "display": "Activity", "message": "TextView", "list": "ListView", "image": "ImageView", "button": "Button"}')

def cleanup_dummy_files():
    """Cleans up directories and dummy files created for demonstration."""
    if DEMO_FILES_DIR.exists():
        shutil.rmtree(DEMO_FILES_DIR)
    if KNOWLEDGE_BASE_DIR.exists():
        shutil.rmtree(KNOWLEDGE_BASE_DIR)
    # GENERATED_APKS_DIR is kept for actual APKs, but can be cleaned if needed
    # if GENERATED_APKS_DIR.exists():
    #     shutil.rmtree(GENERATED_APKS_DIR)

# --- Lobe 0_arabic_lobe ---
class ArabicNLPProcessor:
    def __init__(self, knowledge_base_dir: Path):
        self.knowledge_base_dir = knowledge_base_dir
        self.component_mapping = self._load_json("component_mapping.json")
        self.layout_templates = self._load_json("layout_templates.json")

    def _load_json(self, filename: str):
        """Loads JSON data from the knowledge base."""
        filepath = self.knowledge_base_dir / filename
        if not filepath.exists():
            return {}
        import json
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def parse_arabic_prompt(self, prompt: str) -> dict:
        """
        Parses Arabic natural language prompt to identify application components and their properties.
        This is a simplified example. A real implementation would involve advanced NLP techniques.
        """
        parsed_components = {}
        prompt_lower = prompt.lower()

        # Simple keyword matching for demonstration
        if "إنشاء تطبيق أندرويد بسيط يعرض رسالة ترحيب" in prompt_lower:
            parsed_components["app_type"] = "basic_welcome"
            parsed_components["components"] = ["app", "display", "message"]
            parsed_components["message_text"] = "Welcome from Arabic App!"
        elif "إنشاء تطبيق يعرض قائمة بالعناصر" in prompt_lower:
            parsed_components["app_type"] = "item_list"
            parsed_components["components"] = ["app", "display", "list"]
        elif "إنشاء تطبيق يعرض صورة مع زر" in prompt_lower:
            parsed_components["app_type"] = "image_with_button"
            parsed_components["components"] = ["app", "display", "image", "button"]
        else:
            # Fallback or more sophisticated parsing
            if "تطبيق" in prompt_lower:
                parsed_components["components"] = ["app"]
            if "يعرض" in prompt_lower or "display" in prompt_lower:
                if "components" not in parsed_components:
                    parsed_components["components"] = ["app", "display"]
                else:
                    parsed_components["components"].append("display")
            if "رسالة" in prompt_lower or "message" in prompt_lower:
                if "components" not in parsed_components:
                    parsed_components["components"] = ["app", "display", "message"]
                else:
                    parsed_components["components"].append("message")
            if "قائمة" in prompt_lower or "list" in prompt_lower:
                if "components" not in parsed_components:
                    parsed_components["components"] = ["app", "display", "list"]
                else:
                    parsed_components["components"].append("list")
            if "صورة" in prompt_lower or "image" in prompt_lower:
                if "components" not in parsed_components:
                    parsed_components["components"] = ["app", "display", "image"]
                else:
                    parsed_components["components"].append("image")
            if "زر" in prompt_lower or "button" in prompt_lower:
                if "components" not in parsed_components:
                    parsed_components["components"] = ["app", "display", "button"]
                else:
                    parsed_components["components"].append("button")

        # Map identified components to their Android equivalents using component_mapping
        android_components = []
        for comp_name in parsed_components.get("components", []):
            android_comp = self.component_mapping.get(comp_name, comp_name)
            android_components.append(android_comp)
        parsed_components["android_components"] = android_components

        # Attempt to get layout information based on identified app type or components
        layout_info = {}
        app_type = parsed_components.get("app_type")
        if app_type and app_type in self.layout_templates:
            layout_info = self.layout_templates[app_type]
            parsed_components["layout_structure"] = layout_info.get("layout")
            parsed_components["layout_properties"] = {k: v for k, v in layout_info.items() if k != "layout"}
        else:
            # Simple fallback if no specific template matched
            if "message" in parsed_components.get("components", []):
                layout_info["layout"] = "TextView"
                layout_info["text"] = parsed_components.get("message_text", "Default Message")
            elif "list" in parsed_components.get("components", []):
                layout_info["layout"] = "ListView"
            elif "image" in parsed_components.get("components", []):
                layout_info["layout"] = "ImageView"
            elif "button" in parsed_components.get("components", []):
                layout_info["layout"] = "Button"
            parsed_components["layout_structure"] = layout_info.get("layout")
            parsed_components["layout_properties"] = {k: v for k, v in layout_info.items() if k != "layout"}


        return parsed_components

    def generate_apk_structure_data(self, parsed_data: dict) -> dict:
        """
        Generates structured data suitable for APK code generation based on parsed NLP.
        This bridges the NLP output to a format for code generation.
        """
        apk_structure = {
            "package_name": "com.unifiedmind.generated",
            "app_name": "UnifiedMindApp",
            "activities": [],
            "layout_files": {}
        }

        # Determine main activity and its layout
        main_activity_name = "MainActivity"
        main_layout_name = "activity_main"
        layout_structure = parsed_data.get("layout_structure")
        layout_properties = parsed_data.get("layout_properties", {})

        if layout_structure:
            activity_data = {
                "name": main_activity_name,
                "layout_file": main_layout_name,
                "components": []
            }
            if isinstance(layout_structure, str):
                activity_data["components"].append({"type": layout_structure, **layout_properties})
            elif isinstance(layout_structure, list):
                for comp_type in layout_structure:
                    activity_data["components"].append({"type": comp_type, **layout_properties})
            apk_structure["activities"].append(activity_data)

            apk_structure["layout_files"][main_layout_name] = {
                "root_layout": main_layout_name,
                "components": activity_data["components"]
            }
        else:
            # Default activity if no specific layout parsed
            activity_data = {
                "name": main_activity_name,
                "layout_file": main_layout_name,
                "components": [{"type": "TextView", "text": "Hello World!"}]
            }
            apk_structure["activities"].append(activity_data)
            apk_structure["layout_files"][main_layout_name] = {
                "root_layout": main_layout_name,
                "components": activity_data["components"]
            }


        return apk_structure

def demo_arabic_processing_and_apk_struct_generation():
    """Demonstrates the Arabic NLP parsing and APK structure generation."""
    print("\n--- Starting Arabic Parser and Generator Module Demo ---")
    setup_demo_environment()

    nlp_processor = ArabicNLPProcessor(KNOWLEDGE_BASE_DIR)

    arabic_prompts = [
        "إنشاء تطبيق أندرويد بسيط يعرض رسالة ترحيب.",
        "إنشاء تطبيق يعرض قائمة بالعناصر.",
        "إنشاء تطبيق يعرض صورة مع زر.",
        "أريد تطبيق بسيط.", # Less specific prompt
        "تصميم واجهة تعرض نصاً وزراً." # Another variation
    ]

    for i, prompt in enumerate(arabic_prompts):
        print(f"\n--- Processing Prompt {i+1}: '{prompt}' ---")
        parsed_data = nlp_processor.parse_arabic_prompt(prompt)
        print(f"Parsed Data: {parsed_data}")

        apk_structure_data = nlp_processor.generate_apk_structure_data(parsed_data)
        print(f"Generated APK Structure Data: {apk_structure_data}")

        # In a real scenario, this apk_structure_data would be passed to Lobe 4_code_generation_lobe
        # For demo, we'll just print it.
        # Example of how it might be used:
        # code_generator = CodeGenerator(apk_structure_data)
        # code_generator.generate_android_project()

    print("\n--- Arabic Parser and Generator Module Demo Finished ---")

if __name__ == "__main__":
    demo_arabic_processing_and_apk_struct_generation()
    cleanup_dummy_files()