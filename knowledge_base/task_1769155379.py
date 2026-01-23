import os
import shutil
import pytest
from pathlib import Path

# Assume this is your module file for Arabic text parsing and generation
# For the purpose of this example, we'll create a dummy module file.
ARABIC_MODULE_NAME = "arabic_nlp_module"
ARABIC_MODULE_FILE = f"{ARABIC_MODULE_NAME}.py"

# Create a dummy module file for testing purposes
DUMMY_MODULE_CONTENT = """
import re

def parse_arabic_text(text):
    \"\"\"Parses Arabic text, returning a list of words and basic information.\"\"\"
    words = re.findall(r'\w+', text, re.UNICODE)
    return {
        "original_text": text,
        "words": words,
        "word_count": len(words)
    }

def generate_arabic_sentence(words):
    \"\"\"Generates an Arabic sentence from a list of words.\"\"\"
    return " ".join(words)

def is_arabic(text):
    \"\"\"Checks if a given text string contains predominantly Arabic characters.\"\"\"
    arabic_chars = re.compile(r'[\\u0600-\\u06FF]+')
    return bool(arabic_chars.search(text))
"""

TEST_TASK_DIR = Path("test_arabic_nlp_phase0")

def setup_module_file():
    """Sets up the dummy Arabic NLP module file in the test directory."""
    if not TEST_TASK_DIR.exists():
        TEST_TASK_DIR.mkdir()
    module_path = TEST_TASK_DIR / ARABIC_MODULE_FILE
    with open(module_path, "w", encoding="utf-8") as f:
        f.write(DUMMY_MODULE_CONTENT)
    # Add the test directory to sys.path to allow importing
    import sys
    sys.path.insert(0, str(TEST_TASK_DIR))

def cleanup_module_file():
    """Cleans up the dummy Arabic NLP module file and its directory."""
    # Remove the test directory from sys.path
    import sys
    if str(TEST_TASK_DIR) in sys.path:
        sys.path.remove(str(TEST_TASK_DIR))

    if TEST_TASK_DIR.exists():
        shutil.rmtree(TEST_TASK_DIR)

def load_module(module_name):
    """Dynamically loads a Python module."""
    try:
        module = __import__(module_name)
        # If the module was imported previously and is already in sys.modules,
        # it might not reflect changes if the file was modified.
        # Reloading can be necessary if the module's content has changed
        # during a test run, though often it's better to manage imports
        # within test scopes or ensure a clean import.
        # The 'Memory' error suggests this might be relevant.
        # For demonstration, we'll try reloading if it's already loaded.
        if module_name in sys.modules:
            import importlib
            module = importlib.reload(module)
        return module
    except ImportError:
        print(f"Error: Module '{module_name}' not found.")
        return None

def available_module_names():
    """Returns a list of names of currently loaded modules."""
    return list(sys.modules.keys())

# --- Test Cases ---

def test_arabic_nlp_module_loading():
    """Tests if the Arabic NLP module can be loaded correctly."""
    print("\n--- Testing Arabic NLP Module Loading ---")
    setup_module_file()

    # Initially, the module should not be loaded
    assert ARABIC_MODULE_NAME not in available_module_names()

    arabic_nlp = load_module(ARABIC_MODULE_NAME)
    assert arabic_nlp is not None
    assert ARABIC_MODULE_NAME in available_module_names() # Check if it's loaded after import

    # Test reloading - if the module was modified, this should load the new version.
    # In our case, we are not modifying the file between loads, but this demonstrates the concept.
    arabic_nlp_reloaded = load_module(ARABIC_MODULE_NAME)
    assert arabic_nlp_reloaded is not None
    assert arabic_nlp_reloaded == arabic_nlp # Should be the same module object if no changes

    print("Arabic NLP module loaded successfully.")

def test_parse_arabic_text():
    """Tests the parse_arabic_text function."""
    print("\n--- Testing parse_arabic_text ---")
    setup_module_file()
    arabic_nlp = load_module(ARABIC_MODULE_NAME)
    assert arabic_nlp is not None

    text = "مرحبا بالعالم، كيف حالك؟"
    parsed_data = arabic_nlp.parse_arabic_text(text)

    assert isinstance(parsed_data, dict)
    assert parsed_data["original_text"] == text
    assert parsed_data["words"] == ["مرحبا", "بالعالم", "كيف", "حالك"]
    assert parsed_data["word_count"] == 4
    print(f"Parsed: {parsed_data}")

    text_empty = ""
    parsed_data_empty = arabic_nlp.parse_arabic_text(text_empty)
    assert parsed_data_empty["words"] == []
    assert parsed_data_empty["word_count"] == 0
    print(f"Parsed empty: {parsed_data_empty}")

    text_no_arabic = "Hello world"
    parsed_data_no_arabic = arabic_nlp.parse_arabic_text(text_no_arabic)
    assert parsed_data_no_arabic["words"] == ["Hello", "world"]
    assert parsed_data_no_arabic["word_count"] == 2
    print(f"Parsed no arabic: {parsed_data_no_arabic}")


def test_generate_arabic_sentence():
    """Tests the generate_arabic_sentence function."""
    print("\n--- Testing generate_arabic_sentence ---")
    setup_module_file()
    arabic_nlp = load_module(ARABIC_MODULE_NAME)
    assert arabic_nlp is not None

    words = ["هذا", "مثال", "لجملة", "عربية"]
    sentence = arabic_nlp.generate_arabic_sentence(words)

    assert sentence == "هذا مثال لجملة عربية"
    print(f"Generated sentence: {sentence}")

    words_empty = []
    sentence_empty = arabic_nlp.generate_arabic_sentence(words_empty)
    assert sentence_empty == ""
    print(f"Generated empty sentence: '{sentence_empty}'")

def test_is_arabic():
    """Tests the is_arabic function."""
    print("\n--- Testing is_arabic ---")
    setup_module_file()
    arabic_nlp = load_module(ARABIC_MODULE_NAME)
    assert arabic_nlp is not None

    assert arabic_nlp.is_arabic("مرحبا") is True
    assert arabic_nlp.is_arabic("هذا نص عربي") is True
    assert arabic_nlp.is_arabic("Hello") is False
    assert arabic_nlp.is_arabic("English with 123") is False
    assert arabic_nlp.is_arabic("Mix عربي English") is True # Contains Arabic
    assert arabic_nlp.is_arabic("") is False
    print("is_arabic tests passed.")

# --- Main execution block ---
if __name__ == "__main__":
    print("--- Starting PHASE 0: Master Language (Arabic NLP Foundational Module) ---")

    # Ensure the dummy module is set up before any tests that rely on it
    setup_module_file()

    try:
        # Run all tests
        test_arabic_nlp_module_loading()
        test_parse_arabic_text()
        test_generate_arabic_sentence()
        test_is_arabic()

    except Exception as e:
        print(f"\nAn error occurred during testing: {e}")
        pytest.fail(f"Test failed: {e}") # Use pytest.fail for integration with pytest runners

    finally:
        # --- Cleanup ---
        print("\nCleaning up test directory...")
        cleanup_module_file()
        print(f"Removed test directory and cleared sys.path: {TEST_TASK_DIR}")

        print("\n--- All Test Cases Completed ---")