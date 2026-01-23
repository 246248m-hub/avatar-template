import os
import shutil
from pathlib import Path
import sys
import importlib.util

# Define the root directory for tasks
ROOT_DIR = Path(__file__).parent.parent.parent

# Define a placeholder for the task directory
TEST_TASK_DIR = None

def setup_task_environment(task_name):
    """Sets up a temporary directory for a specific task."""
    global TEST_TASK_DIR
    TEST_TASK_DIR = ROOT_DIR / "tasks" / task_name
    if TEST_TASK_DIR.exists():
        shutil.rmtree(TEST_TASK_DIR)
    TEST_TASK_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Created test directory for task: {TEST_TASK_DIR}")
    return TEST_TASK_DIR

def create_module_file(module_name, content):
    """Creates a Python module file within the current task directory."""
    if TEST_TASK_DIR is None:
        raise ValueError("Task environment not set up. Call setup_task_environment first.")
    module_path = TEST_TASK_DIR / f"{module_name}.py"
    with open(module_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created module file: {module_path}")
    return module_path

def load_module_from_path(module_name, module_path):
    """Loads a module from a given file path."""
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None:
        raise ImportError(f"Could not create module spec for {module_name} at {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    print(f"Loaded module: {module_name}")
    return module

def available_module_names():
    """Lists available module names in the current task directory."""
    if TEST_TASK_DIR is None:
        return []
    return [f.stem for f in TEST_TASK_DIR.glob("*.py")]

# --- PHASE 0: Master Language ---
# Task: Build a foundational module for Arabic text parsing and generation.

def test_arabic_parser_generator():
    """
    Tests the foundational Arabic text parsing and generation module.
    """
    print("\n--- Testing Phase 0: Master Language ---")
    task_name = "arabic_language_module"
    setup_task_environment(task_name)

    # Define the content for the Arabic language module
    arabic_module_content = """
import re

class ArabicParserGenerator:
    def __init__(self):
        # Basic patterns for Arabic letters and common diacritics
        # This is a simplified example. A robust parser would need more complex rules.
        self.arabic_letters = re.compile(r'[\\u0600-\\u06FF]')
        self.diacritics = re.compile(r'[\\u064B-\\u065F]')
        self.non_arabic_chars = re.compile(r'[^\\u0600-\\u06FF\\s]') # Exclude letters, spaces

    def parse_text(self, text):
        \"\"\"
        Parses Arabic text, separating letters, diacritics, and other characters.
        Returns a list of tuples: (type, value), where type is 'letter', 'diacritic', or 'other'.
        \"\"\"
        parsed_elements = []
        for char in text:
            if self.arabic_letters.match(char):
                if self.diacritics.match(char):
                    parsed_elements.append(('diacritic', char))
                else:
                    parsed_elements.append(('letter', char))
            else:
                parsed_elements.append(('other', char))
        return parsed_elements

    def generate_text(self, parsed_elements):
        \"\"\"
        Generates Arabic text from a list of parsed elements.
        Assumes elements are in the correct order.
        \"\"\"
        generated_text = ""
        for element_type, value in parsed_elements:
            generated_text += value
        return generated_text

    def is_arabic(self, text):
        \"\"\"
        Checks if a string contains any Arabic letters.
        \"\"\"
        return bool(self.arabic_letters.search(text))

    def remove_diacritics(self, text):
        \"\"\"
        Removes diacritics from Arabic text.
        \"\"\"
        return self.diacritics.sub('', text)

    def remove_non_arabic(self, text):
        \"\"\"
        Removes characters that are not Arabic letters or spaces.
        \"\"\"
        return self.non_arabic_chars.sub('', text)

# Example Usage (for demonstration within the module itself if executed directly)
if __name__ == "__main__":
    parser_gen = ArabicParserGenerator()
    arabic_sample = "ٱلسَّلَامُ عَلَيْكُم وَرَحْمَةُ ٱللَّٰهِ وَبَرَكَاتُهُ"
    print(f"Original: {arabic_sample}")

    # Parsing
    parsed = parser_gen.parse_text(arabic_sample)
    print(f"Parsed: {parsed}")

    # Generation
    generated = parser_gen.generate_text(parsed)
    print(f"Generated: {generated}")

    # Check if Arabic
    print(f"Is Arabic? {parser_gen.is_arabic(arabic_sample)}")
    print(f"Is Arabic? {parser_gen.is_arabic('Hello world')}")

    # Remove diacritics
    no_diacritics = parser_gen.remove_diacritics(arabic_sample)
    print(f"No Diacritics: {no_diacritics}")

    # Remove non-Arabic
    only_arabic_letters_and_spaces = parser_gen.remove_non_arabic(arabic_sample + " and numbers 123")
    print(f"Only Arabic Letters/Spaces: {only_arabic_letters_and_spaces}")

"""
    # Create the module file
    module_file_path = create_module_file("arabic_language_module", arabic_module_content)

    # Load the module
    arabic_module = load_module_from_path("arabic_language_module", module_file_path)

    # Perform assertions and tests
    print("\nRunning test cases for ArabicParserGenerator...")
    apg = arabic_module.ArabicParserGenerator()

    # Test parsing
    arabic_sample_1 = "ٱلسَّلَامُ"
    parsed_1 = apg.parse_text(arabic_sample_1)
    assert parsed_1 == [('letter', 'ٱ'), ('diacritic', 'َ'), ('letter', 'س'), ('diacritic', 'َّ'), ('letter', 'ل'), ('diacritic', 'ا'), ('diacritic', 'م'), ('diacritic', 'ُ')], f"Parsing failed for '{arabic_sample_1}'. Expected correct parsing, got {parsed_1}"
    print("Test Case 1: Parsing basic Arabic with diacritics - PASSED")

    arabic_sample_2 = "مرحبا بالعالم 123!"
    parsed_2 = apg.parse_text(arabic_sample_2)
    # The current parser is basic. It treats spaces and numbers as 'other'.
    # A more advanced parser would differentiate spaces.
    expected_parsed_2 = [
        ('letter', 'م'), ('letter', 'ر'), ('letter', 'ح'), ('letter', 'ب'), ('letter', 'ا'),
        ('other', ' '), ('letter', 'ب'), ('letter', 'ا'), ('letter', 'ل'), ('letter', 'ع'),
        ('letter', 'ا'), ('letter', 'ل'), ('letter', 'م'), ('other', ' '), ('other', '1'),
        ('other', '2'), ('other', '3'), ('other', '!')
    ]
    assert parsed_2 == expected_parsed_2, f"Parsing failed for '{arabic_sample_2}'. Expected {expected_parsed_2}, got {parsed_2}"
    print("Test Case 2: Parsing Arabic with spaces and non-Arabic chars - PASSED")

    # Test generation
    generated_1 = apg.generate_text(parsed_1)
    assert generated_1 == arabic_sample_1, f"Generation failed for parsed_1. Expected '{arabic_sample_1}', got '{generated_1}'"
    print("Test Case 3: Generation from parsed elements - PASSED")

    # Test is_arabic
    assert apg.is_arabic(arabic_sample_1) is True, f"is_arabic failed for '{arabic_sample_1}'. Expected True, got False"
    print("Test Case 4: is_arabic check (True) - PASSED")
    assert apg.is_arabic("Hello") is False, f"is_arabic failed for 'Hello'. Expected False, got True"
    print("Test Case 5: is_arabic check (False) - PASSED")

    # Test remove_diacritics
    no_diacritics_sample = "ٱلسَّلَامُ"
    expected_no_diacritics = "السلام"
    removed_diacritics = apg.remove_diacritics(no_diacritics_sample)
    assert removed_diacritics == expected_no_diacritics, f"remove_diacritics failed for '{no_diacritics_sample}'. Expected '{expected_no_diacritics}', got '{removed_diacritics}'"
    print("Test Case 6: remove_diacritics - PASSED")

    # Test remove_non_arabic
    non_arabic_test_string = "مرحباً بالعالم 123!"
    expected_non_arabic_removed = "مرحباً بالعالم " # Spaces are kept by the current regex
    removed_non_arabic = apg.remove_non_arabic(non_arabic_test_string)
    assert removed_non_arabic == expected_non_arabic_removed, f"remove_non_arabic failed for '{non_arabic_test_string}'. Expected '{expected_non_arabic_removed}', got '{removed_non_arabic}'"
    print("Test Case 7: remove_non_arabic - PASSED")

    # Test with a more complex sentence
    complex_arabic = "ٱلسَّلَامُ عَلَيْكُم وَرَحْمَةُ ٱللَّٰهِ وَبَرَكَاتُهُ"
    parsed_complex = apg.parse_text(complex_arabic)
    generated_complex = apg.generate_text(parsed_complex)
    assert generated_complex == complex_arabic, f"Complex sentence generation failed. Expected '{complex_arabic}', got '{generated_complex}'"
    print("Test Case 8: Complex sentence parsing and generation - PASSED")

    no_diacritics_complex = apg.remove_diacritics(complex_arabic)
    expected_no_diacritics_complex = "السلام عليكم ورحمة الله وبركاته"
    assert no_diacritics_complex == expected_no_diacritics_complex, f"Complex remove_diacritics failed. Expected '{expected_no_diacritics_complex}', got '{no_diacritics_complex}'"
    print("Test Case 9: Complex sentence remove_diacritics - PASSED")


    # Verify available modules after loading
    print(f"\nModules available after loading: {available_module_names()}")
    assert "arabic_language_module" in available_module_names(), "arabic_language_module should be listed as available."
    print("Test Case 10: Module availability check - PASSED")


# Execute the test function
if __name__ == "__main__":
    try:
        test_arabic_parser_generator()
    except Exception as e:
        print(f"\nAn error occurred during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # --- Cleanup ---
        print("\nCleaning up test directory...")
        if TEST_TASK_DIR and os.path.exists(TEST_TASK_DIR):
            shutil.rmtree(TEST_TASK_DIR)
            print(f"Removed test directory: {TEST_TASK_DIR}")

        print("\n--- All Test Cases Completed ---")