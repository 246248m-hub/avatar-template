import os
import re
import shutil
from typing import Dict, List, Any

# Constants (assuming these are defined elsewhere or will be defined in other lobes)
# KNOWLEDGE_BASE_DIR = "path/to/knowledge_base"
# OUTPUT_APKS_DIR = "path/to/output_apks"
# ANDROID_PROJECT_TEMPLATE_DIR = "path/to/android_template"

# Mock constants for demonstration purposes if not defined globally
KNOWLEDGE_BASE_DIR = "mock_knowledge_base"
OUTPUT_APKS_DIR = "mock_output_apks"
ANDROID_PROJECT_TEMPLATE_DIR = "mock_android_template"

# Ensure directories exist for mock purposes
os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
os.makedirs(OUTPUT_APKS_DIR, exist_ok=True)
os.makedirs(ANDROID_PROJECT_TEMPLATE_DIR, exist_ok=True)


def cleanup_dummy_files():
    """
    Cleans up dummy files and directories created during module testing.
    This function is intended for use in testing and demonstration scenarios.
    """
    print("Cleaning up dummy files and directories...")
    # Example cleanup: remove any .txt files in the knowledge base
    for filename in os.listdir(KNOWLEDGE_BASE_DIR):
        if filename.endswith(".txt"):
            os.remove(os.path.join(KNOWLEDGE_BASE_DIR, filename))
            print(f"Removed dummy file: {os.path.join(KNOWLEDGE_BASE_DIR, filename)}")

    # Clean up dummy template directory if it exists
    if os.path.exists(ANDROID_PROJECT_TEMPLATE_DIR):
        shutil.rmtree(ANDROID_PROJECT_TEMPLATE_DIR)
        print(f"Cleaned up dummy Android project template directory: {ANDROID_PROJECT_TEMPLATE_DIR}")

    # Clean up output APK directory if it exists
    if os.path.exists(OUTPUT_APKS_DIR):
        shutil.rmtree(OUTPUT_APKS_DIR)
        print(f"Cleaned up dummy output APK directory: {OUTPUT_APKS_DIR}")


def parse_arabic_instruction(instruction: str) -> Dict[str, Any]:
    """
    Parses a natural language Arabic instruction into a structured command.

    This function aims to identify key components of an Arabic instruction related
    to APK generation, such as the desired app name, features, or components.

    Args:
        instruction (str): The natural language instruction in Arabic.

    Returns:
        Dict[str, Any]: A dictionary representing the parsed instruction.
                       Example: {'action': 'create_app', 'app_name': 'آلة حاسبة', 'features': ['addition', 'subtraction']}
    """
    parsed_data: Dict[str, Any] = {"instruction_type": "unknown"}

    # --- Basic Pattern Matching for Common Instructions ---

    # Pattern to detect app creation and name
    app_creation_pattern = re.compile(r"إنشاء تطبيق اسمه ([\u0600-\u06FF\s]+?)(?: مع الميزات)?")
    match_app_name = app_creation_pattern.search(instruction)
    if match_app_name:
        parsed_data["action"] = "create_app"
        parsed_data["app_name"] = match_app_name.group(1).strip()

        # Try to extract features if present
        features_part_match = re.search(r"مع الميزات ([\u0600-\u06FF\s,]+)", instruction)
        if features_part_match:
            features_str = features_part_match.group(1).strip()
            parsed_data["features"] = [f.strip() for f in features_str.split(',') if f.strip()]
        else:
            parsed_data["features"] = []
        return parsed_data

    # Pattern for adding specific components/screens
    add_component_pattern = re.compile(r"إضافة شاشة ([\u0600-\u06FF\s]+?) إلى التطبيق ([\u0600-\u06FF\s]+?)")
    match_add_component = add_component_pattern.search(instruction)
    if match_add_component:
        parsed_data["action"] = "add_component"
        parsed_data["component_name"] = match_add_component.group(1).strip()
        parsed_data["app_name"] = match_add_component.group(2).strip()
        return parsed_data

    # Pattern for updating an existing app
    update_app_pattern = re.compile(r"تحديث التطبيق ([\u0600-\u06FF\s]+?) لإضافة ([\u0600-\u06FF\s,]+)")
    match_update_app = update_app_pattern.search(instruction)
    if match_update_app:
        parsed_data["action"] = "update_app"
        parsed_data["app_name"] = match_update_app.group(1).strip()
        features_str = match_update_app.group(2).strip()
        parsed_data["features_to_add"] = [f.strip() for f in features_str.split(',') if f.strip()]
        return parsed_data

    # Pattern for building/compiling an app
    build_app_pattern = re.compile(r"بناء التطبيق ([\u0600-\u06FF\s]+?)")
    match_build_app = build_app_pattern.search(instruction)
    if match_build_app:
        parsed_data["action"] = "build_app"
        parsed_data["app_name"] = match_build_app.group(1).strip()
        return parsed_data

    # --- More Sophisticated NLP could be integrated here ---
    # For now, we'll keep it to basic patterns.
    # A more advanced approach would involve:
    # 1. Tokenization of Arabic text.
    # 2. Lemmatization/Stemming.
    # 3. Part-of-Speech Tagging.
    # 4. Named Entity Recognition (NER) to identify app names, features, etc.
    # 5. Intent classification to determine the user's goal (create, update, build, etc.).

    # If no specific pattern matches, try a generic interpretation
    if not parsed_data.get("action", "unknown") == "unknown":
        return parsed_data

    # Generic fallback for simple instructions, assuming the whole instruction is the app name if no other keywords are found
    # This is a very weak fallback and needs improvement.
    if instruction.strip():
        parsed_data["action"] = "process_general_request"
        parsed_data["raw_instruction"] = instruction.strip()
        # Attempt to extract a potential app name if it looks like one
        potential_app_name_match = re.search(r"^([\u0600-\u06FF\s]+)(?:\.|$)", instruction)
        if potential_app_name_match:
            parsed_data["potential_app_name"] = potential_app_name_match.group(1).strip()

    return parsed_data


def generate_arabic_response(parsed_instruction: Dict[str, Any]) -> str:
    """
    Generates a natural language Arabic response based on the parsed instruction.

    Args:
        parsed_instruction (Dict[str, Any]): The structured data from the parsed instruction.

    Returns:
        str: An Arabic response.
    """
    action = parsed_instruction.get("action", "unknown")
    app_name = parsed_instruction.get("app_name", "التطبيق")
    component_name = parsed_instruction.get("component_name", "المكون")
    features = parsed_instruction.get("features", [])
    features_to_add = parsed_instruction.get("features_to_add", [])
    raw_instruction = parsed_instruction.get("raw_instruction", "")

    if action == "create_app":
        response = f"تم فهم طلبك بإنشاء تطبيق جديد باسم '{app_name}'."
        if features:
            response += f" سيتم تضمين الميزات التالية: {', '.join(features)}."
        else:
            response += " لم يتم تحديد ميزات إضافية في الوقت الحالي."
        return response
    elif action == "add_component":
        response = f"تم فهم طلبك بإضافة شاشة '{component_name}' إلى التطبيق '{app_name}'."
        return response
    elif action == "update_app":
        response = f"تم فهم طلبك بتحديث التطبيق '{app_name}'."
        if features_to_add:
            response += f" سيتم إضافة الميزات التالية: {', '.join(features_to_add)}."
        else:
            response += " لم يتم تحديد ميزات إضافية للتحديث."
        return response
    elif action == "build_app":
        response = f"تم فهم طلبك ببناء التطبيق '{app_name}'. سيتم البدء في عملية التحويل البرمجي."
        return response
    elif action == "process_general_request":
        if raw_instruction:
            return f"تم استلام طلبك العام: '{raw_instruction}'. أحاول فهم المطلوب..."
        else:
            return "لم أتمكن من فهم طلبك بدقة. يرجى تقديم تعليمات أوضح."
    else:
        return "لم أتمكن من فهم التعليمات المقدمة. يرجى توضيح طلبك."


def process_arabic_nlp_request(user_input: str, knowledge_base_path: str) -> Dict[str, Any]:
    """
    Orchestrates the processing of an Arabic natural language instruction.
    This function acts as an entry point for Arabic NLP tasks within the system.

    Args:
        user_input (str): The raw Arabic natural language input from the user.
        knowledge_base_path (str): Path to the knowledge base directory.

    Returns:
        Dict[str, Any]: A dictionary containing the parsed instruction and a generated response.
    """
    print(f"Processing Arabic NLP request: '{user_input}'")

    # 1. Parse the Arabic instruction
    parsed_data = parse_arabic_instruction(user_input)
    print(f"Parsed instruction: {parsed_data}")

    # 2. Generate an Arabic response based on the parsed data
    generated_response = generate_arabic_response(parsed_data)
    print(f"Generated Arabic response: '{generated_response}'")

    # 3. (Optional) Interact with the knowledge base
    # For example, if the instruction was to create an app, we might log this or
    # retrieve existing app definitions from the knowledge base.
    # This part is highly dependent on the specific functionality and other lobes.
    if parsed_data.get("action") == "create_app":
        app_name = parsed_data.get("app_name", "untitled_app")
        app_definition_file = os.path.join(knowledge_base_path, f"{app_name}_def.json")
        # In a real scenario, this would involve creating a JSON definition
        # For demonstration, just acknowledging its potential existence.
        print(f"Potential app definition file would be: {app_definition_file}")

    return {
        "parsed_instruction": parsed_data,
        "generated_response": generated_response
    }

# --- Example Usage / Demo ---
if __name__ == "__main__":
    print("--- Arabic Parser and Generator Module Demo ---")

    # Example 1: Create a simple calculator app
    instruction1 = "إنشاء تطبيق اسمه آلة حاسبة بسيطة مع الميزات جمع, طرح"
    print(f"\nInput: {instruction1}")
    result1 = process_arabic_nlp_request(instruction1, KNOWLEDGE_BASE_DIR)
    print(f"Result: {result1}")

    # Example 2: Add a screen to an existing app
    instruction2 = "إضافة شاشة قائمة رئيسية إلى التطبيق آلة حاسبة بسيطة"
    print(f"\nInput: {instruction2}")
    result2 = process_arabic_nlp_request(instruction2, KNOWLEDGE_BASE_DIR)
    print(f"Result: {result2}")

    # Example 3: Update an app to add features
    instruction3 = "تحديث التطبيق آلة حاسبة بسيطة لإضافة ضرب, قسمة"
    print(f"\nInput: {instruction3}")
    result3 = process_arabic_nlp_request(instruction3, KNOWLEDGE_BASE_DIR)
    print(f"Result: {result3}")

    # Example 4: Build an app
    instruction4 = "بناء التطبيق آلة حاسبة بسيطة"
    print(f"\nInput: {instruction4}")
    result4 = process_arabic_nlp_request(instruction4, KNOWLEDGE_BASE_DIR)
    print(f"Result: {result4}")

    # Example 5: Unclear instruction
    instruction5 = "كيف يمكنني فعل ذلك؟"
    print(f"\nInput: {instruction5}")
    result5 = process_arabic_nlp_request(instruction5, KNOWLEDGE_BASE_DIR)
    print(f"Result: {result5}")

    # Example 6: Another creation request without explicit features
    instruction6 = "إنشاء تطبيق اسمه متتبع المهام"
    print(f"\nInput: {instruction6}")
    result6 = process_arabic_nlp_request(instruction6, KNOWLEDGE_BASE_DIR)
    print(f"Result: {result6}")

    # Clean up dummy files created during this demo
    print("\n--- Cleaning up dummy files ---")
    cleanup_dummy_files()

    print("\n--- Arabic Parser and Generator Module Demo Finished ---")