import os
import shutil
import pytest

TEST_TASK_DIR = "test_arabic_parser"


# --- Helper Functions ---

def create_test_directory():
    """Creates a temporary directory for test files."""
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
    os.makedirs(TEST_TASK_DIR)
    print(f"Created test directory: {TEST_TASK_DIR}")


def create_test_file(filename, content=""):
    """Creates a test file with the given content in the test directory."""
    filepath = os.path.join(TEST_TASK_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created test file: {filepath}")
    return filepath


# --- Module to be Tested (Placeholder) ---
# In a real scenario, this would be your actual arabic_parser.py module.
# For this example, we'll create a dummy module to simulate its existence.

DUMMY_ARABIC_PARSER_CONTENT = """
def parse_arabic_sentence(sentence):
    \"\"\"
    Placeholder function to simulate parsing an Arabic sentence.
    Returns a list of tokens.
    \"\"\"
    return sentence.split()

def generate_arabic_sentence(tokens):
    \"\"\"
    Placeholder function to simulate generating an Arabic sentence from tokens.
    Returns a string.
    \"\"\"
    return " ".join(tokens)
"""


# --- Test Cases ---

def test_parse_arabic_sentence():
    """Tests the parse_arabic_sentence function."""
    create_test_directory()
    dummy_module_path = create_test_file("arabic_parser.py", DUMMY_ARABIC_PARSER_CONTENT)

    # Dynamically import the dummy module
    import importlib.util
    spec = importlib.util.spec_from_file_location("arabic_parser", dummy_module_path)
    arabic_parser = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(arabic_parser)

    sentence = "مرحبا بالعالم"
    tokens = arabic_parser.parse_arabic_sentence(sentence)
    assert isinstance(tokens, list)
    assert tokens == ["مرحبا", "بالعالم"]
    print(f"Test passed: parse_arabic_sentence('{sentence}') -> {tokens}")


def test_generate_arabic_sentence():
    """Tests the generate_arabic_sentence function."""
    create_test_directory()
    dummy_module_path = create_test_file("arabic_parser.py", DUMMY_ARABIC_PARSER_CONTENT)

    # Dynamically import the dummy module
    import importlib.util
    spec = importlib.util.spec_from_file_location("arabic_parser", dummy_module_path)
    arabic_parser = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(arabic_parser)

    tokens = ["كيف", "حالك", "اليوم"]
    sentence = arabic_parser.generate_arabic_sentence(tokens)
    assert isinstance(sentence, str)
    assert sentence == "كيف حالك اليوم"
    print(f"Test passed: generate_arabic_sentence({tokens}) -> '{sentence}'")


# --- Main Execution Block ---

if __name__ == "__main__":
    # Create the directory for the module we'll be testing
    create_test_directory()
    # Create a dummy arabic_parser.py file
    create_test_file("arabic_parser.py", DUMMY_ARABIC_PARSER_CONTENT)

    print("\n--- Running Test Cases ---")
    try:
        # You can run pytest programmatically like this,
        # but it's more common to run 'pytest' from the command line.
        # For demonstration purposes, we'll call the test functions directly.
        test_parse_arabic_sentence()
        test_generate_arabic_sentence()
    except ImportError as e:
        print(f"Error: {e}")
        print("Please ensure 'pytest' is installed: pip install pytest")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # --- Cleanup ---
    print("\nCleaning up test directory...")
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
        print(f"Removed test directory: {TEST_TASK_DIR}")

    print("\n--- All Test Cases Completed ---")