import os
import re
import shutil
import subprocess
from pathlib import Path

# Assume KNOWLEDGE_BASE_DIR and PROJECT_TEMPLATES_DIR are defined elsewhere
# For demonstration purposes, let's define them here:
KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
PROJECT_TEMPLATES_DIR = Path("./project_templates")

# Ensure directories exist for the demo
KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)
PROJECT_TEMPLATES_DIR.mkdir(exist_ok=True)

# --- Lobe 0: Language Lobe (Simplified for demonstration) ---
# This lobe would handle core language processing, translation, understanding, etc.
# For this specific task, we'll assume it provides a function to get Arabic text.

def get_arabic_text_from_knowledge_base(prompt_key: str, knowledge_base_path: Path) -> str:
    """
    Simulates retrieving Arabic text from a knowledge base based on a key.
    In a real system, this would involve complex NLP and data retrieval.
    """
    # For demo: a simple mapping
    arabic_texts = {
        "test_prompt_5": "اكتب كود اندرويد لتطبيق يعرض رسالة 'مرحباً بالعالم' على الشاشة.",
        "apk_info_prompt": "إنشاء تطبيق APK بسيط يعرض نصًا يسمى \"اسم التطبيق\" برسالة \"وصف التطبيق\".",
        "activity_creation_prompt": "إنشاء نشاط رئيسي باسم \"MainActivity\" يعرض \"Hello from MainActivity!\"."
    }
    return arabic_texts.get(prompt_key, f"No Arabic text found for key: {prompt_key}")

# --- Lobe 2: Arabic Parser and Generator Lobe ---
# This lobe takes natural language (Arabic in this case) and parses it to
# extract intents and parameters, then generates code structures or other data.

class ArabicIntentParser:
    def __init__(self):
        # In a real system, this would involve training an NLP model for Arabic intent recognition
        pass

    def parse(self, arabic_text: str) -> dict:
        """
        Parses Arabic text to extract intent and associated parameters.
        Returns a dictionary with 'intent' and 'params'.
        """
        intent = "unknown"
        params = {}

        # Basic pattern matching for demonstration
        if "اكتب كود اندرويد لتطبيق" in arabic_text:
            intent = "create_android_app"
            # Extract app name if present (simplified)
            app_name_match = re.search(r"لتطبيق اسمه \"(.*?)\"", arabic_text)
            if app_name_match:
                params["app_name"] = app_name_match.group(1)
            else:
                params["app_name"] = "MyAndroidApp" # Default app name

            # Extract display text if present
            display_text_match = re.search(r"يعرض رسالة \"(.*?)\"", arabic_text)
            if display_text_match:
                params["display_text"] = display_text_match.group(1)
            else:
                params["display_text"] = "Hello World" # Default display text

        elif "إنشاء تطبيق APK بسيط" in arabic_text:
            intent = "create_simple_apk"
            app_name_match = re.search(r"يسمى \"(.*?)\"", arabic_text)
            if app_name_match:
                params["app_name"] = app_name_match.group(1)
            else:
                params["app_name"] = "SimpleAPK"

            description_match = re.search(r"برسالة \"(.*?)\"", arabic_text)
            if description_match:
                params["app_description"] = description_match.group(1)
            else:
                params["app_description"] = "A simple APK"

        elif "إنشاء نشاط رئيسي" in arabic_text:
            intent = "create_android_activity"
            activity_name_match = re.search(r"باسم \"(.*?)\"", arabic_text)
            if activity_name_match:
                params["activity_name"] = activity_name_match.group(1)
            else:
                params["activity_name"] = "MainActivity"

            display_text_match = re.search(r"يعرض \"(.*?)\"", arabic_text)
            if display_text_match:
                params["display_text"] = display_text_match.group(1)
            else:
                params["display_text"] = "Default Activity Text"

        return {"intent": intent, "params": params}

class ArabicAPKGenerator:
    def __init__(self, project_templates_path: Path):
        self.project_templates_path = project_templates_path
        self.parser = ArabicIntentParser()

    def generate_apk_components(self, arabic_prompt: str) -> dict:
        """
        Takes an Arabic prompt, parses it, and generates structured data
        representing the desired APK components.
        """
        parsed_data = self.parser.parse(arabic_prompt)
        intent = parsed_data["intent"]
        params = parsed_data["params"]

        generated_output = {}

        if intent == "create_android_app":
            app_name = params.get("app_name", "MyAndroidApp")
            display_text = params.get("display_text", "Hello World")
            print(f"--- Generating components for Android App: '{app_name}' with text: '{display_text}' ---")
            # In a full system, this would orchestrate calls to other lobes
            # For now, we'll just structure the output
            generated_output["apk_structure"] = {
                "type": "android_app",
                "app_name": app_name,
                "main_activity": {
                    "name": "MainActivity",
                    "layout_text": f"TextView with text: '{display_text}'"
                },
                "dependencies": ["androidx.appcompat:appcompat:1.6.1"]
            }
            generated_output["apk_intent_data"] = {
                "app_name": app_name,
                "main_activity_name": "MainActivity",
                "initial_message": display_text
            }

        elif intent == "create_simple_apk":
            app_name = params.get("app_name", "SimpleAPK")
            app_description = params.get("app_description", "A simple APK")
            print(f"--- Generating components for Simple APK: '{app_name}' with description: '{app_description}' ---")
            generated_output["apk_structure"] = {
                "type": "simple_apk",
                "app_name": app_name,
                "description": app_description
            }
            generated_output["apk_intent_data"] = {
                "app_name": app_name,
                "description": app_description
            }

        elif intent == "create_android_activity":
            activity_name = params.get("activity_name", "MainActivity")
            display_text = params.get("display_text", "Default Activity Text")
            print(f"--- Generating components for Android Activity: '{activity_name}' with text: '{display_text}' ---")
            generated_output["apk_structure"] = {
                "type": "android_activity",
                "activity_name": activity_name,
                "content": f"Layout with a TextView displaying: '{display_text}'"
            }
            generated_output["apk_intent_data"] = {
                "activity_name": activity_name,
                "display_text": display_text
            }

        else:
            print(f"--- Unknown intent '{intent}' from prompt: '{arabic_prompt}' ---")
            generated_output["error"] = f"Could not generate APK components for unknown intent: {intent}"

        return generated_output

# --- Helper function to simulate inter-lobe communication ---
def demo_lobe2_arabic_parser_and_generator(knowledge_base_path: Path, project_templates_path: Path):
    """
    Demonstrates the functionality of Lobe 2 (Arabic Parser and Generator).
    """
    print("\n--- Starting Lobe 2: Arabic Parser and Generator Demo ---")

    generator = ArabicAPKGenerator(project_templates_path)

    # Test case 1: Create a simple Android app
    prompt_1 = get_arabic_text_from_knowledge_base("test_prompt_5", knowledge_base_path)
    print(f"\nArabic Prompt 1: \"{prompt_1}\"")
    output_1 = generator.generate_apk_components(prompt_1)
    print(f"Generated Output 1: {output_1}")

    # Test case 2: Create a simple APK with name and description
    prompt_2 = get_arabic_text_from_knowledge_base("apk_info_prompt", knowledge_base_path)
    print(f"\nArabic Prompt 2: \"{prompt_2}\"")
    output_2 = generator.generate_apk_components(prompt_2)
    print(f"Generated Output 2: {output_2}")

    # Test case 3: Create a specific Android activity
    prompt_3 = get_arabic_text_from_knowledge_base("activity_creation_prompt", knowledge_base_path)
    print(f"\nArabic Prompt 3: \"{prompt_3}\"")
    output_3 = generator.generate_apk_components(prompt_3)
    print(f"Generated Output 3: {output_3}")

    # In a full system, Lobe 2 would then pass its outputs to other lobes.
    # For example, initial_code would go to Lobe 4 (code_generation_lobe)
    # and apk_intent_data would go to Lobe 8 (apk_compiler_lobe).

    print("\n--- Lobe 2: Arabic Parser and Generator Demo Finished ---")
    return output_1, output_2, output_3

# --- Example of how this might be called (for testing purposes) ---
if __name__ == "__main__":
    # Create dummy directories and files if they don't exist
    KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)
    PROJECT_TEMPLATES_DIR.mkdir(exist_ok=True)

    # Add some dummy knowledge base entries for demonstration
    with open(KNOWLEDGE_BASE_DIR / "arabic_prompts.txt", "w", encoding="utf-8") as f:
        f.write("test_prompt_5: اكتب كود اندرويد لتطبيق يعرض رسالة 'مرحباً بالعالم' على الشاشة.\n")
        f.write("apk_info_prompt: إنشاء تطبيق APK بسيط يعرض نصًا يسمى \"اسم التطبيق\" برسالة \"وصف التطبيق\".\n")
        f.write("activity_creation_prompt: إنشاء نشاط رئيسي باسم \"MainActivity\" يعرض \"Hello from MainActivity!\" .\n")

    # Run the demo
    output1, output2, output3 = demo_lobe2_arabic_parser_and_generator(KNOWLEDGE_BASE_DIR, PROJECT_TEMPLATES_DIR)

    # In a real system, these outputs would be passed to subsequent lobes.
    # For example:
    # lobe4_code_generation.generate_code(output1.get("apk_structure"), output1.get("apk_intent_data"))
    # lobe8_apk_compiler.compile_apk(output1.get("apk_intent_data"))