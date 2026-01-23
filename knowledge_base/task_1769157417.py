import os
import shutil
from typing import List, Dict, Any

# --- Configuration ---
TEST_TASK_DIR = "arabic_parsing_test_files"

# --- Helper Functions ---

def setup_test_directory() -> None:
    """Creates a temporary directory for test files."""
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
    os.makedirs(TEST_TASK_DIR)
    print(f"Created test directory: {TEST_TASK_DIR}")

def cleanup_test_directory() -> None:
    """Removes the temporary directory used for test files."""
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
        print(f"Removed test directory: {TEST_TASK_DIR}")

def create_test_file(filename: str, content: str) -> str:
    """Creates a test file with given content in the test directory."""
    filepath = os.path.join(TEST_TASK_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created test file: {filepath}")
    return filepath

def load_arabic_module_content(module_name: str) -> str:
    """
    Simulates loading the content of an Arabic module.
    In a real scenario, this would involve importing or reading from a file.
    For this example, we'll return a predefined string based on the module name.
    """
    module_content = {
        "greetings": """# Arabic Greetings Module
def say_hello(name="العالم"):
    return f"مرحباً يا {name}!"

def say_goodbye(name="العالم"):
    return f"إلى اللقاء يا {name}!"
""",
        "numbers": """# Arabic Numbers Module
def get_arabic_number(num: int) -> str:
    arabic_map = {
        0: "صفر", 1: "واحد", 2: "اثنان", 3: "ثلاثة", 4: "أربعة",
        5: "خمسة", 6: "ستة", 7: "سبعة", 8: "ثمانية", 9: "تسعة"
    }
    return arabic_map.get(num, str(num))
""",
        "grammar": """# Arabic Grammar Module
def conjugate_verb(verb: str, tense: str, person: str) -> str:
    # Simplified conjugation logic for demonstration
    if tense == "present" and person == "first_singular":
        return f"أنا {verb}"
    elif tense == "present" and person == "second_singular_male":
        return f"أنتَ {verb}"
    return verb # Default to original verb if no specific rule
"""
    }
    return module_content.get(module_name, "# Module not found")

def parse_arabic_text(text: str) -> Dict[str, Any]:
    """
    Parses Arabic text to extract structured information.
    This is a highly simplified parser for demonstration.
    In a real-world scenario, this would involve NLP libraries like NLTK, spaCy, or Araby.
    """
    parsed_data = {"original_text": text, "tokens": [], "entities": {}, "intent": None}

    # Basic tokenization (splitting by whitespace)
    parsed_data["tokens"] = text.split()

    # Very basic entity extraction (e.g., names, numbers)
    if "مرحباً يا" in text:
        parts = text.split("مرحباً يا")
        if len(parts) > 1:
            name = parts[1].strip()
            parsed_data["entities"]["person_name"] = name
            parsed_data["intent"] = "greeting"
    elif "صفر" in text or "واحد" in text:
        parsed_data["entities"]["number_word"] = "some_number" # Placeholder
        parsed_data["intent"] = "number_inquiry"
    elif "أنا" in text:
        parts = text.split("أنا")
        if len(parts) > 1:
            verb_part = parts[1].strip()
            parsed_data["entities"]["verb_phrase"] = verb_part
            parsed_data["intent"] = "action_statement"


    return parsed_data

def generate_arabic_text(data: Dict[str, Any]) -> str:
    """
    Generates Arabic text from structured data.
    This is a simplified generator. Real-world generation is complex.
    """
    if data.get("intent") == "greeting":
        name = data.get("entities", {}).get("person_name", "العالم")
        return f"مرحباً يا {name}!"
    elif data.get("intent") == "number_inquiry":
        num_word = data.get("entities", {}).get("number_word", "الرقم")
        return f"الرقم هو {num_word}."
    elif data.get("intent") == "action_statement":
        verb_phrase = data.get("entities", {}).get("verb_phrase", "")
        return f"أنا {verb_phrase}."
    elif "message" in data:
        return data["message"]
    return "نص غير معروف."

def available_module_names() -> List[str]:
    """
    Returns a list of available Arabic module names.
    In a real system, this would scan a directory or a manifest.
    For this example, we return predefined module names.
    """
    return ["greetings", "numbers", "grammar"]

# --- Main Module Functions ---

def load_arabic_module(module_name: str) -> None:
    """
    Loads an Arabic module. In this simulation, it just makes its content available.
    A real implementation would involve dynamic importing or registering functions.
    """
    if module_name not in available_module_names():
        print(f"Error: Module '{module_name}' not found.")
        return

    # In a real system, you might do:
    # try:
    #     import importlib
    #     module = importlib.import_module(f"arabic_modules.{module_name}")
    #     # Register functions from the module globally or in a registry
    #     print(f"Successfully loaded module: {module_name}")
    # except ImportError:
    #     print(f"Error loading module {module_name}.")

    # For simulation, we just acknowledge it's loaded.
    print(f"Simulating loading module: {module_name}")
    # We can simulate access to its content if needed for further tests,
    # but the prompt suggests this function is just for loading.

def get_parsed_arabic_text(filepath: str) -> Dict[str, Any]:
    """
    Reads Arabic text from a file and parses it.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            arabic_text = f.read()
        return parse_arabic_text(arabic_text)
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return {}
    except Exception as e:
        print(f"An error occurred while reading or parsing file {filepath}: {e}")
        return {}

def generate_arabic_output(data: Dict[str, Any]) -> str:
    """
    Generates Arabic text output based on provided structured data.
    """
    return generate_arabic_text(data)

# --- Test Cases ---

def test_parsing_and_generation() -> None:
    """
    Tests the core parsing and generation functionalities.
    """
    print("\n--- Running Test Case: Parsing and Generation ---")
    setup_test_directory()

    # Test 1: Basic Greeting Parsing and Generation
    greeting_text = "مرحباً يا أحمد!"
    filepath = create_test_file("greeting.txt", greeting_text)
    parsed_greeting = get_parsed_arabic_text(filepath)
    print(f"Parsed '{greeting_text}': {parsed_greeting}")
    generated_greeting = generate_arabic_output(parsed_greeting)
    print(f"Generated from parsed data: '{generated_greeting}'")
    assert generated_greeting == "مرحباً يا أحمد!"

    # Test 2: Basic Number Parsing (Simplified)
    number_text = "الرقم هو صفر."
    filepath = create_test_file("number.txt", number_text)
    parsed_number = get_parsed_arabic_text(filepath)
    print(f"Parsed '{number_text}': {parsed_number}")
    generated_number = generate_arabic_output(parsed_number)
    print(f"Generated from parsed data: '{generated_number}'")
    # Note: The current generator is very basic for numbers, so we expect a generic output.
    assert generated_number == "الرقم هو some_number."

    # Test 3: Generation from structured data without prior parsing
    data_to_generate = {"message": "هذا نص تم إنشاؤه مباشرة."}
    generated_direct = generate_arabic_output(data_to_generate)
    print(f"Generated directly from data {data_to_generate}: '{generated_direct}'")
    assert generated_direct == "هذا نص تم إنشاؤه مباشرة."

    # Test 4: Parsing text that might be generated
    generated_greeting_data = {"intent": "greeting", "entities": {"person_name": "فاطمة"}}
    generated_greeting_text = generate_arabic_output(generated_greeting_data)
    print(f"Generated greeting text: '{generated_greeting_text}'")
    filepath = create_test_file("generated_greeting.txt", generated_greeting_text)
    re_parsed_greeting = get_parsed_arabic_text(filepath)
    print(f"Re-parsed generated text: {re_parsed_greeting}")
    assert re_parsed_greeting["intent"] == "greeting"
    assert re_parsed_greeting["entities"]["person_name"] == "فاطمة"

    print("--- Test Case Completed: Parsing and Generation ---")

def test_module_loading() -> None:
    """
    Tests the module loading functionality.
    """
    print("\n--- Running Test Case: Module Loading ---")

    # Get available module names
    available_modules = available_module_names()
    print(f"Available modules: {available_modules}")
    assert "greetings" in available_modules
    assert "numbers" in available_modules
    assert "grammar" in available_modules

    # Test loading existing modules
    load_arabic_module("greetings")
    load_arabic_module("numbers")

    # Test loading a non-existent module
    load_arabic_module("non_existent_module")

    print("--- Test Case Completed: Module Loading ---")

def run_all_tests() -> None:
    """
    Runs all defined test cases.
    """
    print("--- Starting All Test Cases ---")
    test_parsing_and_generation()
    test_module_loading()

    # --- Cleanup ---
    print("\nCleaning up test directory...")
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
        print(f"Removed test directory: {TEST_TASK_DIR}")

    print("\n--- All Test Cases Completed ---")

if __name__ == "__main__":
    run_all_tests()