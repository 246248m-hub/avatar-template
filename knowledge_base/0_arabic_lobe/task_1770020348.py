import os
import json
from typing import Dict, Any, List

KNOWLEDGE_BASE_DIR = "./knowledge_base"  # Assuming a knowledge base directory exists
MODIFIED_APK_STRUCTURE_GLOBAL = {}  # Global to hold modified APK structure across lobes

def initialize_knowledge_base():
    """Initializes the knowledge base directory if it doesn't exist."""
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        os.makedirs(KNOWLEDGE_BASE_DIR)
        print(f"Initialized knowledge base directory at: {KNOWLEDGE_BASE_DIR}")

def load_apk_structure_from_json(filepath: str) -> Dict[str, Any]:
    """Loads APK structure from a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: APK structure file not found at {filepath}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}")
        return {}

def save_apk_structure_to_json(structure: Dict[str, Any], filepath: str):
    """Saves APK structure to a JSON file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(structure, f, indent=2, ensure_ascii=False)
    except IOError:
        print(f"Error: Could not save APK structure to {filepath}")

def get_arabic_command_definition(command_name: str) -> Dict[str, Any]:
    """
    Retrieves the definition of an Arabic command from the knowledge base.
    This is a placeholder; in a real scenario, this would query a database
    or a structured knowledge file.
    """
    # Example: In a real scenario, this would fetch from a structured source.
    # For demonstration, we'll hardcode a few.
    arabic_commands = {
        "arabic_command_3": {
            "description": "Modify the main activity name and add a dependency.",
            "parameters": {
                "new_activity_name": "string",
                "dependency_to_add": "string"
            },
            "actions": [
                {"type": "rename_activity", "target": "main_activity", "new_name": "{new_activity_name}"},
                {"type": "add_gradle_dependency", "dependency": "{dependency_to_add}"}
            ]
        }
    }
    return arabic_commands.get(command_name, {})

def apply_arabic_command_to_apk_structure(
    apk_structure: Dict[str, Any],
    arabic_command: Dict[str, Any],
    command_parameters: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Applies the logic defined by an Arabic command to the APK structure.

    Args:
        apk_structure: The current APK structure.
        arabic_command: The definition of the Arabic command.
        command_parameters: The parameters provided for the command.

    Returns:
        The modified APK structure.
    """
    modified_structure = apk_structure.copy()
    actions = arabic_command.get("actions", [])
    command_description = arabic_command.get("description", "Unnamed command")

    print(f"\nApplying Arabic command: '{command_description}' with parameters: {command_parameters}")

    for action in actions:
        action_type = action.get("type")
        if not action_type:
            continue

        if action_type == "rename_activity":
            target_activity = action.get("target")
            new_name = action.get("new_name")
            if target_activity and new_name:
                # Substitute parameters into the new_name string
                formatted_new_name = new_name.format(**command_parameters)
                if "activities" in modified_structure:
                    for activity in modified_structure["activities"]:
                        if activity.get("name") == target_activity:
                            activity["name"] = formatted_new_name
                            print(f"  Renamed activity '{target_activity}' to '{formatted_new_name}'")
                            break
        elif action_type == "add_gradle_dependency":
            dependency = action.get("dependency")
            if dependency:
                # Substitute parameters into the dependency string
                formatted_dependency = dependency.format(**command_parameters)
                if "dependencies" in modified_structure:
                    if formatted_dependency not in modified_structure["dependencies"]:
                        modified_structure["dependencies"].append(formatted_dependency)
                        print(f"  Added Gradle dependency: '{formatted_dependency}'")
                else:
                    modified_structure["dependencies"] = [formatted_dependency]
                    print(f"  Added Gradle dependency: '{formatted_dependency}'")
        else:
            print(f"  Warning: Unknown action type '{action_type}' encountered.")

    return modified_structure

def process_arabic_command_from_natural_language(natural_language_input: str, current_apk_structure: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parses natural language input to identify an Arabic command and its parameters,
    then applies it to the APK structure.

    This is a simplified parser. A real implementation would involve more
    sophisticated NLP techniques (e.g., intent recognition, slot filling).
    """
    print(f"\n--- Processing Arabic command from natural language: '{natural_language_input}' ---")

    # --- Simplified Arabic Command Parsing ---
    # This is a heuristic-based approach for demonstration.
    # A robust solution would use an NLP model trained on Arabic commands.

    identified_command_name = None
    command_parameters = {}

    # Example heuristic for "arabic_command_3"
    if "change the main activity to" in natural_language_input and "and add dependency" in natural_language_input:
        parts = natural_language_input.split("change the main activity to")
        if len(parts) > 1:
            sub_parts = parts[1].split("and add dependency")
            if len(sub_parts) > 1:
                identified_command_name = "arabic_command_3"
                new_activity_name = sub_parts[0].strip()
                dependency_to_add = sub_parts[1].strip()
                command_parameters = {
                    "new_activity_name": new_activity_name,
                    "dependency_to_add": dependency_to_add
                }
                print(f"  Identified command: '{identified_command_name}'")
                print(f"  Extracted parameters: {command_parameters}")

    if identified_command_name:
        arabic_command_definition = get_arabic_command_definition(identified_command_name)
        if arabic_command_definition:
            modified_apk_structure = apply_arabic_command_to_apk_structure(
                current_apk_structure,
                arabic_command_definition,
                command_parameters
            )
            return modified_apk_structure
        else:
            print(f"  Error: Definition for command '{identified_command_name}' not found in knowledge base.")
    else:
        print("  Could not identify a known Arabic command from the input.")

    return current_apk_structure # Return original if no command identified or applied

# --- DEMO USAGE ---

def demo_arabic_command_processing():
    """Demonstrates the processing of Arabic natural language commands."""
    print("\n--- Initiating Lobe 0_arabic_lobe ---")
    initialize_knowledge_base()

    # Dummy APK structure for demonstration
    initial_apk_structure = {
        "package_name": "com.example.myapp",
        "version_code": 1,
        "version_name": "1.0",
        "activities": [
            {"name": "MainActivity", "layout": "activity_main.xml"},
            {"name": "SettingsActivity", "layout": "activity_settings.xml"}
        ],
        "dependencies": [
            "implementation 'androidx.core:core-ktx:1.9.0'"
        ]
    }

    print("\nInitial APK Structure:\n", json.dumps(initial_apk_structure, indent=2, ensure_ascii=False))

    # Example natural language input in Arabic (conceptually) or a translation of intent
    # For this demo, we'll use an English string that maps to an Arabic intent.
    # In a real scenario, this would be actual Arabic text processed by a language model.
    arabic_nl_command_1 = "غير اسم النشاط الرئيسي إلى MyAwesomeActivity وأضف الاعتمادية com.google.android.material:material:1.10.0"
    # A more direct mapping if we only parse English intents for now.
    # This simulates receiving a parsed intent from an Arabic NLP stage.
    simulated_nl_intent_1 = "change the main activity to MyAwesomeActivity and add dependency com.google.android.material:material:1.10.0"

    # Process the simulated natural language command
    modified_apk_structure_1 = process_arabic_command_from_natural_language(
        simulated_nl_intent_1,
        initial_apk_structure
    )

    # Store the modified structure globally for potential use by other lobes
    global MODIFIED_APK_STRUCTURE_GLOBAL
    MODIFIED_APK_STRUCTURE_GLOBAL = modified_apk_structure_1

    print("\nUpdated APK Structure (after command 1):\n", json.dumps(MODIFIED_APK_STRUCTURE_GLOBAL, indent=2, ensure_ascii=False))

    # Example of another command, perhaps with slightly different phrasing or
    # targeting different aspects if the command definition supported it.
    # For now, let's assume the same command definition.
    simulated_nl_intent_2 = "alter the main activity to SuperAppActivity and include the dependency org.jetbrains.kotlin:kotlin-stdlib:1.9.20"

    modified_apk_structure_2 = process_arabic_command_from_natural_language(
        simulated_nl_intent_2,
        MODIFIED_APK_STRUCTURE_GLOBAL # Apply to the previously modified structure
    )
    MODIFIED_APK_STRUCTURE_GLOBAL = modified_apk_structure_2

    print("\nUpdated APK Structure (after command 2):\n", json.dumps(MODIFIED_APK_STRUCTURE_GLOBAL, indent=2, ensure_ascii=False))


    # Simulate another command that might not match the current simple parser
    simulated_nl_intent_3 = "add a new feature called 'UserLogin'"
    modified_apk_structure_3 = process_arabic_command_from_natural_language(
        simulated_nl_intent_3,
        MODIFIED_APK_STRUCTURE_GLOBAL
    )
    # If no command was identified, MODIFIED_APK_STRUCTURE_GLOBAL remains unchanged.
    # We can confirm by checking if it's different from modified_apk_structure_3
    if modified_apk_structure_3 == MODIFIED_APK_STRUCTURE_GLOBAL:
        print("\n(No known command identified for: 'add a new feature called \'UserLogin\'')")
    else:
        MODIFIED_APK_STRUCTURE_GLOBAL = modified_apk_structure_3
        print("\nUpdated APK Structure (after command 3):\n", json.dumps(MODIFIED_APK_STRUCTURE_GLOBAL, indent=2, ensure_ascii=False))

    # Clean up dummy directory
    if os.path.exists(KNOWLEDGE_BASE_DIR):
        try:
            os.rmdir(KNOWLEDGE_BASE_DIR)
            print(f"\nCleaned up knowledge base directory: {KNOWLEDGE_BASE_DIR}")
        except OSError as e:
            print(f"Error cleaning up directory {KNOWLEDGE_BASE_DIR}: {e}")

    print("\n--- Lobe 0_arabic_lobe Demo Finished ---")

if __name__ == "__main__":
    demo_arabic_command_processing()