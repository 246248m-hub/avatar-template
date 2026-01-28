import os
import re
import json
import shutil
from pathlib import Path

# Define constants for directory structure
MOCK_KNOWLEDGE_BASE_DIR = Path("./mock_knowledge_base")
MOCK_APP_TEMPLATES_DIR = Path("./mock_app_templates")
MOCK_PROJECT_OUTPUT_DIR = Path("./mock_project_output")
MOCK_DEBUG_KEYSTORE_DIR = Path("./mock_debug_keystore")

def ensure_directories_exist():
    """Ensures that all necessary mock directories exist."""
    MOCK_KNOWLEDGE_BASE_DIR.mkdir(exist_ok=True)
    MOCK_APP_TEMPLATES_DIR.mkdir(exist_ok=True)
    MOCK_PROJECT_OUTPUT_DIR.mkdir(exist_ok=True)
    MOCK_DEBUG_KEYSTORE_DIR.mkdir(exist_ok=True)

def create_mock_debug_keystore():
    """Creates a mock debug.keystore file for simulation."""
    ensure_directories_exist()
    debug_keystore_path = MOCK_DEBUG_KEYSTORE_DIR / "debug.keystore"
    if not debug_keystore_path.exists():
        with open(debug_keystore_path, "w") as f:
            f.write("This is a mock debug.keystore file.\n")
        print(f"Mock debug.keystore created at: {debug_keystore_path}")
    return debug_keystore_path

def load_arabic_nlp_data(data_path: Path) -> dict:
    """
    Loads Arabic NLP data from a JSON file.
    This simulates loading linguistic rules, grammar, and vocabulary.
    """
    if not data_path.exists():
        # Create a dummy data file if it doesn't exist
        dummy_data = {
            "grammar_rules": {
                "greeting": ["مرحبا", "أهلاً"],
                "button_creation": ["أنشئ زر", "اصنع زر"]
            },
            "keywords": {
                "button_text": ["اسم الزر", "نص الزر"],
                "action": ["عند الضغط", "وظيفة الزر"]
            },
            "actions": {
                "show_message": "عرض رسالة",
                "navigate_to": "الانتقال إلى"
            }
        }
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(dummy_data, f, ensure_ascii=False, indent=4)
        print(f"Dummy Arabic NLP data created at: {data_path}")
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def parse_arabic_prompt(prompt: str, nlp_data: dict) -> dict:
    """
    Parses an Arabic natural language prompt to extract structured information
    for APK generation.
    """
    parsed_info = {"elements": []}

    # Basic keyword matching and rule application
    prompt_lower = prompt.lower()

    # Check for greetings
    for greeting in nlp_data.get("grammar_rules", {}).get("greeting", []):
        if greeting.lower() in prompt_lower:
            parsed_info["greeting"] = greeting
            break

    # Detect button creation intent
    for button_keyword in nlp_data.get("grammar_rules", {}).get("button_creation", []):
        if button_keyword.lower() in prompt_lower:
            button_details = {}

            # Extract button text
            for text_keyword in nlp_data.get("keywords", {}).get("button_text", []):
                match = re.search(rf"{text_keyword}\s*['\"]?([^'\"]+)['\"]?", prompt, re.IGNORECASE | re.UNICODE)
                if match:
                    button_details["text"] = match.group(1).strip()
                    break

            # Extract button action (simplified)
            for action_keyword in nlp_data.get("keywords", {}).get("action", []):
                for action_type, arabic_action in nlp_data.get("actions", {}).items():
                    if arabic_action.lower() in prompt_lower:
                        # More sophisticated parsing would be needed here to extract
                        # arguments for the action (e.g., message content, screen name)
                        button_details["action_type"] = action_type
                        # Placeholder for action parameters
                        button_details["action_params"] = {}
                        break
                if "action_type" in button_details:
                    break

            if button_details:
                parsed_info["elements"].append({"type": "button", **button_details})
            break # Assume only one button creation intent per prompt for simplicity

    return parsed_info

def generate_app_structure_from_arabic_parse(parsed_data: dict, app_name: str) -> dict:
    """
    Generates a high-level representation of the app structure based on parsed Arabic data.
    This would typically involve translating the parsed components into an internal
    representation that can be used by the code generation lobe.
    """
    app_structure = {
        "appName": app_name,
        "components": []
    }

    for element in parsed_data.get("elements", []):
        if element["type"] == "button":
            component = {
                "type": "Button",
                "text": element.get("text", "Default Button Text"),
                "onClick": {
                    "actionType": element.get("action_type", "none"),
                    "parameters": element.get("action_params", {})
                }
            }
            app_structure["components"].append(component)

    return app_structure

def build_arabic_parser_module(knowledge_base_dir: Path, app_templates_dir: Path, output_dir: Path):
    """
    Builds and demonstrates the Arabic parser module.
    This function orchestrates loading NLP data, parsing a prompt,
    and generating an internal app structure representation.
    """
    ensure_directories_exist()
    debug_keystore_path = create_mock_debug_keystore()

    arabic_nlp_data_path = knowledge_base_dir / "arabic_nlp_config.json"
    nlp_data = load_arabic_nlp_data(arabic_nlp_data_path)

    # Example Arabic prompt
    arabic_prompt = "مرحبا! أنشئ زر باسم 'اضغط هنا' يقوم بعرض رسالة 'أهلاً بك!'"
    print(f"\n--- Parsing Arabic Prompt ---")
    print(f"Prompt: \"{arabic_prompt}\"")

    parsed_arabic_info = parse_arabic_prompt(arabic_prompt, nlp_data)
    print(f"Parsed Arabic Info: {json.dumps(parsed_arabic_info, ensure_ascii=False, indent=2)}")

    # Generate internal app structure from parsed data
    app_name_for_demo = "MyArabicApp"
    app_structure_representation = generate_app_structure_from_arabic_parse(
        parsed_arabic_info,
        app_name_for_demo
    )
    print(f"\n--- Generated App Structure Representation ---")
    print(f"App Name: {app_structure_representation['appName']}")
    print(f"Components: {json.dumps(app_structure_representation['components'], ensure_ascii=False, indent=2)}")

    # Simulate saving this structure for the next lobe
    structure_file_path = output_dir / f"{app_name_for_demo}_structure.json"
    with open(structure_file_path, 'w', encoding='utf-8') as f:
        json.dump(app_structure_representation, f, ensure_ascii=False, indent=4)
    print(f"App structure representation saved to: {structure_file_path}")

    print("\n--- Arabic Parser Module Demo Finished ---")
    return debug_keystore_path # Return for potential cleanup by other lobes

if __name__ == '__main__':
    # Example usage of the Arabic parser module
    print("--- Initiating Arabic Parser Module Demo ---")
    # Create mock directories if they don't exist for standalone run
    os.makedirs(MOCK_KNOWLEDGE_BASE_DIR, exist_ok=True)
    os.makedirs(MOCK_APP_TEMPLATES_DIR, exist_ok=True)
    os.makedirs(MOCK_PROJECT_OUTPUT_DIR, exist_ok=True)
    os.makedirs(MOCK_DEBUG_KEYSTORE_DIR, exist_ok=True)

    demo_debug_keystore_path = build_arabic_parser_module(
        MOCK_KNOWLEDGE_BASE_DIR,
        MOCK_APP_TEMPLATES_DIR,
        MOCK_PROJECT_OUTPUT_DIR
    )

    # Example of how a subsequent lobe might clean up
    if demo_debug_keystore_path and demo_debug_keystore_path.exists():
        print("\n--- Cleaning up mocked debug.keystore from Arabic Parser Demo ---")
        try:
            demo_debug_keystore_path.unlink()
            demo_debug_keystore_path.parent.rmdir()
            print("Mock debug.keystore cleaned up.")
        except OSError as e:
            print(f"Error cleaning up debug.keystore: {e}")

    # Clean up other mock directories if desired after demo
    # print("\n--- Cleaning up mock directories ---")
    # shutil.rmtree(MOCK_KNOWLEDGE_BASE_DIR)
    # shutil.rmtree(MOCK_APP_TEMPLATES_DIR)
    # shutil.rmtree(MOCK_PROJECT_OUTPUT_DIR)
    # shutil.rmtree(MOCK_DEBUG_KEYSTORE_DIR)
    # print("Mock directories cleaned up.")