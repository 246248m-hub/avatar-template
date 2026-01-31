import os
import re
import shutil

# Assume KNOWLEDGE_BASE_DIR and RATED_PROJECT_DIR are defined elsewhere
# Assume a function like 'generate_apk_structure' exists in Lobe 4
# Assume a function like 'build_apk' exists in Lobe 8

# --- Lobe 3: Arabic Parser and Generator ---

def parse_arabic_input(arabic_text: str) -> dict:
    """
    Parses Arabic natural language input to extract intents and entities.
    This is a placeholder; actual implementation would involve NLP libraries
    like CAMeL Tools or AraBERT for advanced parsing.
    """
    parsed_data = {
        "intent": None,
        "entities": {}
    }

    # Simple keyword-based intent detection
    if re.search(r"أنشئ تطبيق|صمم تطبيق|اطلب تطبيق", arabic_text, re.IGNORECASE):
        parsed_data["intent"] = "create_app"
    elif re.search(r"تحديث|غير", arabic_text, re.IGNORECASE):
        parsed_data["intent"] = "update_app"
    elif re.search(r"احذف|إزالة", arabic_text, re.IGNORECASE):
        parsed_data["intent"] = "delete_app"

    # Simple entity extraction (e.g., app name)
    app_name_match = re.search(r"تطبيق اسمه (.+?)(?:،|\.|$)", arabic_text, re.IGNORECASE)
    if app_name_match:
        parsed_data["entities"]["app_name"] = app_name_match.group(1).strip()

    # More complex entity extraction would go here for UI elements, functionalities, etc.
    # Example: extracting button labels, text fields, etc.
    button_matches = re.findall(r"زر (.+?)(?:،|\.|$)", arabic_text, re.IGNORECASE)
    if button_matches:
        parsed_data["entities"]["buttons"] = [btn.strip() for btn in button_matches]

    text_field_matches = re.findall(r"حقل نصي لـ (.+?)(?:،|\.|$)", arabic_text, re.IGNORECASE)
    if text_field_matches:
        parsed_data["entities"]["text_fields"] = [tf.strip() for tf in text_field_matches]


    return parsed_data

def generate_code_from_parsed(parsed_data: dict, project_dir: str) -> str:
    """
    Generates basic Android project structure and code snippets based on parsed data.
    This function would interact with Lobe 4 (Code Generation Lobe).
    """
    intent = parsed_data.get("intent")
    entities = parsed_data.get("entities", {})
    app_name = entities.get("app_name", "MyApp")

    print(f"Generating code structure for app: {app_name} with intent: {intent}")

    # This is a mock call to Lobe 4's functionality
    # In a real scenario, this would involve calling a function from Lobe 4
    # For demonstration, we'll just simulate the creation of a dummy directory
    if intent == "create_app":
        generated_code_path = os.path.join(project_dir, f"{app_name.replace(' ', '_')}_project")
        os.makedirs(generated_code_path, exist_ok=True)
        # Simulate creating dummy files for Android project structure
        with open(os.path.join(generated_code_path, "AndroidManifest.xml"), "w") as f:
            f.write("<manifest package=\"com.example." + app_name.lower().replace(' ', '') + "\">\n</manifest>")
        with open(os.path.join(generated_code_path, "MainActivity.java"), "w") as f:
            f.write("public class MainActivity {\n}\n")
        print(f"Simulated Android project structure created at: {generated_code_path}")
        return generated_code_path
    else:
        print(f"Intent '{intent}' not directly supported for code generation in this demo.")
        return None

# --- Lobe 0: Arabic Lobe (Integration point for Lobe 3) ---
def arabic_lobe_workflow(arabic_prompt: str, knowledge_base_dir: str, rated_project_dir: str) -> str:
    """
    Orchestrates the Arabic parsing and code generation workflow.
    """
    print("\n--- Initiating Arabic Lobe Workflow ---")

    # 1. Parse Arabic input
    print(f"Parsing Arabic prompt: '{arabic_prompt}'")
    parsed_data = parse_arabic_input(arabic_prompt)
    print(f"Parsed data: {parsed_data}")

    # 2. Generate code structure based on parsed data (simulating Lobe 4 interaction)
    print(f"Generating code structure. Project directory: {rated_project_dir}")
    generated_project_path = generate_code_from_parsed(parsed_data, rated_project_dir)

    if generated_project_path:
        print(f"Code generation initiated. Simulated project path: {generated_project_path}")
        # In a real system, this path would be passed to Lobe 4 for detailed code generation.
        # For this demo, we assume Lobe 4 has already "done its job" in generate_code_from_parsed.
        return generated_project_path
    else:
        print("Code generation failed or intent not supported.")
        return None

# --- Helper functions for cleanup (used by multiple lobes) ---
def cleanup_dummy_files(directory_to_clean: str = None):
    """
    Cleans up dummy files and directories created during demos.
    If directory_to_clean is None, it cleans up common demo directories.
    """
    if directory_to_clean and os.path.exists(directory_to_clean):
        try:
            shutil.rmtree(directory_to_clean)
            print(f"Cleaned up: {directory_to_clean}")
        except OSError as e:
            print(f"Error cleaning up {directory_to_clean}: {e}")
    else:
        # General cleanup for common demo directories
        for dirname in ["arabic_generated_apps", "android_output", "generated_code"]:
            path = os.path.join(".", dirname)
            if os.path.exists(path):
                try:
                    shutil.rmtree(path)
                    print(f"Cleaned up: {path}")
                except OSError as e:
                    print(f"Error cleaning up {path}: {e}")

# --- Example Usage ---
if __name__ == "__main__":
    # Define dummy directories for the demo
    KNOWLEDGE_BASE_DIR = "./knowledge_base"
    RATED_PROJECT_DIR = "./rated_projects"
    OUTPUT_APK_DIR = "./output_apks"
    os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
    os.makedirs(RATED_PROJECT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_APK_DIR, exist_ok=True)

    # --- Demo 1: Basic App Creation ---
    test_prompt_1 = "أنشئ تطبيق اسمه حاسبة بسيطة وأضف زر للجمع وزر للطرح."
    print("\n--- Demo: Arabic Parser and Generator Module (Basic App Creation) ---")
    generated_project_path_1 = arabic_lobe_workflow(test_prompt_1, KNOWLEDGE_BASE_DIR, RATED_PROJECT_DIR)
    if generated_project_path_1:
        print(f"Arabic prompt '{test_prompt_1}' processed. Simulated project generated at: {generated_project_path_1}")
        # Simulate passing to Lobe 8 (APK Compiler) for completion
        print("\n--- Simulating Lobe 8 (APK Compiler) interaction ---")
        dummy_apk_path_1 = os.path.join(OUTPUT_APK_DIR, "calculator_app.apk")
        print(f"Simulating APK build for: {generated_project_path_1}")
        # In reality, Lobe 8 would take the project path and build the APK.
        # Here, we just create a dummy APK file.
        with open(dummy_apk_path_1, "w") as f:
            f.write("This is a dummy APK file.")
        print(f"Simulated APK generated at: {dummy_apk_path_1}")

    # --- Demo 2: App Update (Illustrative - current parser is basic) ---
    test_prompt_2 = "حدث تطبيق حاسبة بسيطة ليدعم الضرب."
    print("\n--- Demo: Arabic Parser and Generator Module (App Update) ---")
    generated_project_path_2 = arabic_lobe_workflow(test_prompt_2, KNOWLEDGE_BASE_DIR, RATED_PROJECT_DIR)
    if generated_project_path_2:
        print(f"Arabic prompt '{test_prompt_2}' processed. Simulated project generated at: {generated_project_path_2}")
        # Simulate passing to Lobe 8 (APK Compiler) for completion
        print("\n--- Simulating Lobe 8 (APK Compiler) interaction ---")
        dummy_apk_path_2 = os.path.join(OUTPUT_APK_DIR, "calculator_app_updated.apk")
        print(f"Simulating APK build for updated app: {generated_project_path_2}")
        with open(dummy_apk_path_2, "w") as f:
            f.write("This is a dummy updated APK file.")
        print(f"Simulated updated APK generated at: {dummy_apk_path_2}")

    # Clean up dummy files created by this lobe's demos
    print("\n--- Cleaning up dummy files for Lobe 3 Demos ---")
    cleanup_dummy_files(RATED_PROJECT_DIR) # This will remove the generated_project_path directories
    cleanup_dummy_files(OUTPUT_APK_DIR)

    print("\n--- Arabic Parser and Generator Module Demo Finished ---")

    # --- Lobe 0: Language Lobe Demo (as per the interlinked memory) ---
    # This section demonstrates the previous state of Lobe 0 as seen in the memory.
    # In the grand objective, Lobe 3 is a more advanced evolution of Lobe 0's parsing capabilities.
    print("\n--- Re-running Lobe 0 (Language Lobe) Demo from Interlinked Memory ---")
    # Mocking the function call from Lobe 0's last thought
    def c_text(prompt: str, knowledge_dir: str) -> str:
        print(f"Mock function c_text called with prompt: '{prompt}' (Knowledge Dir: {knowledge_dir})")
        # Simulate generating some text based on the prompt
        if "hello" in prompt.lower():
            return "Hello there! How can I assist you today?"
        elif "weather" in prompt.lower():
            return "The weather is sunny with a slight breeze."
        else:
            return "I'm not sure how to respond to that."

    test_prompt_5 = "Say hello and ask about the weather."
    print(f"Calling mock c_text for prompt: '{test_prompt_5}'")
    generated_output_5 = c_text(test_prompt_5, KNOWLEDGE_BASE_DIR)
    print(f"Generated text for prompt '{test_prompt_5}': {generated_output_5}")

    # Clean up dummy files from the Lobe 0 demo
    print("\n--- Cleaning up dummy files for Lobe 0 Demo ---")
    # Assuming c_text might create files in KNOWLEDGE_BASE_DIR if it were real,
    # but in this mock it doesn't. We'll just ensure the base dirs exist.
    pass # No specific files to clean up for this mock

    print("\n--- Arabic Parser and Generator Module Demo Finished ---")