import os
import shutil
import pytest

# Define a temporary directory for testing
TEST_TASK_DIR = "temp_arabic_parser_test"

class ArabicParser:
    def __init__(self):
        pass

    def parse_text(self, text: str) -> dict:
        """
        Parses Arabic text and extracts basic information.
        For now, this is a placeholder.
        """
        if not text:
            return {"words": [], "length": 0, "arabic_chars": 0}

        words = text.split()
        arabic_chars = sum(1 for char in text if '\u0600' <= char <= '\u06FF')
        return {
            "words": words,
            "length": len(text),
            "arabic_chars": arabic_chars
        }

    def generate_text(self, data: dict) -> str:
        """
        Generates Arabic text from structured data.
        For now, this is a placeholder.
        """
        if not data or "words" not in data or not data["words"]:
            return ""
        return " ".join(data["words"])

# --- Pytest Test Cases ---

def setup_module(module):
    """Setup function to create the test directory."""
    if not os.path.exists(TEST_TASK_DIR):
        os.makedirs(TEST_TASK_DIR)
    print(f"\nCreated test directory: {TEST_TASK_DIR}")

def teardown_module(module):
    """Teardown function to remove the test directory."""
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
        print(f"\nRemoved test directory: {TEST_TASK_DIR}")

def test_parser_empty_string():
    parser = ArabicParser()
    result = parser.parse_text("")
    assert result == {"words": [], "length": 0, "arabic_chars": 0}

def test_parser_basic_arabic_text():
    parser = ArabicParser()
    text = "مرحبا بالعالم"
    result = parser.parse_text(text)
    assert result["words"] == ["مرحبا", "بالعالم"]
    assert result["length"] == len(text)
    assert result["arabic_chars"] == len(text) # Assuming all characters are Arabic

def test_parser_mixed_text():
    parser = ArabicParser()
    text = "Hello مرحبا 123 بالعالم!"
    result = parser.parse_text(text)
    assert result["words"] == ["Hello", "مرحبا", "123", "بالعالم!"]
    assert result["length"] == len(text)
    assert result["arabic_chars"] == len("مرحبا بالعالم") # Count only Arabic chars

def test_generator_empty_data():
    parser = ArabicParser()
    data = {}
    generated_text = parser.generate_text(data)
    assert generated_text == ""

def test_generator_empty_word_list():
    parser = ArabicParser()
    data = {"words": []}
    generated_text = parser.generate_text(data)
    assert generated_text == ""

def test_generator_basic_words():
    parser = ArabicParser()
    data = {"words": ["مرحبا", "بك"]}
    generated_text = parser.generate_text(data)
    assert generated_text == "مرحبا بك"

def test_generator_with_other_keys_ignored():
    parser = ArabicParser()
    data = {"words": ["كيف", "حالك"], "language": "Arabic", "version": 1.0}
    generated_text = parser.generate_text(data)
    assert generated_text == "كيف حالك"

# --- Main Execution Block (for demonstration if not run with pytest) ---
if __name__ == "__main__":
    print("Running Arabic Parser Module Demonstration:")

    # Test Parsing
    print("\n--- Testing Parsing ---")
    parser = ArabicParser()
    sample_text_1 = "السلام عليكم ورحمة الله وبركاته"
    parsed_data_1 = parser.parse_text(sample_text_1)
    print(f"Original Text 1: '{sample_text_1}'")
    print(f"Parsed Data 1: {parsed_data_1}")

    sample_text_2 = "This is a test with some Arabic: مرحبا بالعالم."
    parsed_data_2 = parser.parse_text(sample_text_2)
    print(f"Original Text 2: '{sample_text_2}'")
    print(f"Parsed Data 2: {parsed_data_2}")

    sample_text_3 = ""
    parsed_data_3 = parser.parse_text(sample_text_3)
    print(f"Original Text 3: '{sample_text_3}'")
    print(f"Parsed Data 3: {parsed_data_3}")

    # Test Generation
    print("\n--- Testing Generation ---")
    sample_data_1 = {"words": ["صباح", "الخير"], "metadata": "simple greeting"}
    generated_text_1 = parser.generate_text(sample_data_1)
    print(f"Data for Generation 1: {sample_data_1}")
    print(f"Generated Text 1: '{generated_text_1}'")

    sample_data_2 = {"words": [], "source": "unknown"}
    generated_text_2 = parser.generate_text(sample_data_2)
    print(f"Data for Generation 2: {sample_data_2}")
    print(f"Generated Text 2: '{generated_text_2}'")

    # To run the pytest tests, you would typically execute:
    # pytest your_module_name.py
    print("\nTo run automated tests, save this code as a Python file (e.g., arabic_module.py)")
    print("and run 'pytest arabic_module.py' in your terminal after installing pytest (`pip install pytest`).")

    # --- Cleanup ---
    print("\nCleaning up test directory...")
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
        print(f"Removed test directory: {TEST_TASK_DIR}")

    print("\n--- All Test Cases Completed ---")