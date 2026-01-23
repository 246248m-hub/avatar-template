import os
import shutil
import unittest
from pathlib import Path

# Define the base directory for tasks
BASE_TASK_DIR = Path(__file__).parent.parent.parent / "tasks"

# Ensure the base tasks directory exists
BASE_TASK_DIR.mkdir(exist_ok=True)

# Define a specific directory for this task
TASK_MODULE_DIR = BASE_TASK_DIR / "arabic_parsing"
TASK_MODULE_DIR.mkdir(exist_ok=True)

# Define the test directory
TEST_TASK_DIR = TASK_MODULE_DIR / "tests"
TEST_TASK_DIR.mkdir(exist_ok=True)

# --- Module Code ---
# arabic_parsing.py
ARABIC_PARSING_MODULE_CODE = """
import re

def parse_arabic_text(text):
    \"\"\"
    Parses Arabic text, performing basic cleaning and normalization.

    Args:
        text (str): The Arabic text to parse.

    Returns:
        str: The cleaned and normalized Arabic text.
    \"\"\"
    # Remove common non-Arabic characters and normalize some variations
    # Keep Arabic letters, numbers, space, and basic punctuation
    cleaned_text = re.sub(r'[^\\u0600-\\u06FF\\u0750-\\u077F\\u08A0-\\u08FF0-9 \\u060C\\u061B\\u061F\\u0021\\u003F]', '', text)

    # Normalize specific problematic characters (e.g., different forms of alef, yaa)
    # This is a simplified normalization, more comprehensive normalization might be needed
    normalized_text = cleaned_text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
    normalized_text = normalized_text.replace('ى', 'ي')
    normalized_text = normalized_text.replace('ة', 'ه') # Commonly done, though can change meaning
    normalized_text = normalized_text.strip()
    return normalized_text

def generate_arabic_sentence(words):
    \"\"\"
    Generates an Arabic sentence from a list of words.

    Args:
        words (list[str]): A list of Arabic words.

    Returns:
        str: The generated Arabic sentence.
    \"\"\"
    if not words:
        return ""
    # Basic sentence construction: join words with a space.
    # More advanced generation would involve grammar rules.
    sentence = " ".join(words)
    return sentence

# Placeholder for more advanced parsing/generation functions
def analyze_arabic_morphology(word):
    \"\"\"
    Placeholder for Arabic morphology analysis.

    Args:
        word (str): An Arabic word.

    Returns:
        dict: A dictionary representing morphological features (placeholder).
    \"\"\"
    return {"root": word, "features": "placeholder"}

def translate_to_arabic(english_text):
    \"\"\"
    Placeholder for English to Arabic translation.

    Args:
        english_text (str): English text.

    Returns:
        str: Translated Arabic text (placeholder).
    \"\"\"
    return "Arabic translation placeholder for: " + english_text

# Function to list available modules (for demonstration/testing)
def available_module_names():
    \"\"\"
    Lists the names of available modules in the current directory.
    This is a simplistic approach for demonstration.
    \"\"\"
    current_dir = Path(__file__).parent
    module_files = current_dir.glob("*.py")
    module_names = [f.stem for f in module_files if f.stem != "__init__"]
    return module_names

"""

# --- Test Code ---
# test_arabic_parsing.py
TEST_ARABIC_PARSING_CODE = """
import unittest
import sys
import os

# Adjust Python path to include the tasks directory if necessary
# This is crucial for importing modules from the tasks directory
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from tasks.arabic_parsing.arabic_parsing import parse_arabic_text, generate_arabic_sentence, analyze_arabic_morphology, translate_to_arabic
except ImportError:
    print("Failed to import arabic_parsing module. Ensure sys.path is correctly configured.")
    raise

class TestArabicParsing(unittest.TestCase):

    def test_parse_arabic_text_basic(self):
        text = "مرحباً بالعالم! هذا نص تجريبي."
        expected = "مرحبا بالعالم هذا نص تجريبي"
        self.assertEqual(parse_arabic_text(text), expected)

    def test_parse_arabic_text_with_numbers_and_punctuation(self):
        text = "السعر هو 123.45 ريال، هل هذا صحيح؟"
        expected = "السعر هو 12345 ريال هل هذا صحيح"
        self.assertEqual(parse_arabic_text(text), expected)

    def test_parse_arabic_text_with_normalization(self):
        text = "أهلاً إبراهيم، هذا ياءٌ و تاءٌ مربوطةٌ."
        expected = "اهلا ابراهيم هذا ياء و تاء مربوطه"
        self.assertEqual(parse_arabic_text(text), expected)

    def test_parse_arabic_text_empty(self):
        text = ""
        expected = ""
        self.assertEqual(parse_arabic_text(text), expected)

    def test_parse_arabic_text_only_noise(self):
        text = "!@#$%^&*()"
        expected = ""
        self.assertEqual(parse_arabic_text(text), expected)

    def test_generate_arabic_sentence_basic(self):
        words = ["مرحبا", "بالعالم"]
        expected = "مرحبا بالعالم"
        self.assertEqual(generate_arabic_sentence(words), expected)

    def test_generate_arabic_sentence_single_word(self):
        words = ["السلام"]
        expected = "السلام"
        self.assertEqual(generate_arabic_sentence(words), expected)

    def test_generate_arabic_sentence_empty(self):
        words = []
        expected = ""
        self.assertEqual(generate_arabic_sentence(words), expected)

    def test_analyze_arabic_morphology_placeholder(self):
        word = "كتاب"
        result = analyze_arabic_morphology(word)
        self.assertIsInstance(result, dict)
        self.assertIn("root", result)
        self.assertIn("features", result)
        self.assertEqual(result["root"], word)

    def test_translate_to_arabic_placeholder(self):
        english = "Hello world"
        expected_prefix = "Arabic translation placeholder for: "
        self.assertTrue(translate_to_arabic(english).startswith(expected_prefix))
        self.assertIn(english, translate_to_arabic(english))

if __name__ == '__main__':
    unittest.main()
"""


def setup_module():
    """Sets up the module directory and files."""
    print(f"Setting up module directory: {TASK_MODULE_DIR}")
    with open(TASK_MODULE_DIR / "arabic_parsing.py", "w", encoding="utf-8") as f:
        f.write(ARABIC_PARSING_MODULE_CODE)
    print(f"Created: {TASK_MODULE_DIR / 'arabic_parsing.py'}")

    # Create an empty __init__.py to make it a package
    (TASK_MODULE_DIR / "__init__.py").touch()

    print(f"Setting up test directory: {TEST_TASK_DIR}")
    with open(TEST_TASK_DIR / "test_arabic_parsing.py", "w", encoding="utf-8") as f:
        f.write(TEST_ARABIC_PARSING_CODE)
    print(f"Created: {TEST_TASK_DIR / 'test_arabic_parsing.py'}")

def run_tests():
    """Runs the unit tests for the arabic_parsing module."""
    print("\nRunning tests for arabic_parsing module...")
    # Dynamically discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(TEST_TASK_DIR), pattern="test_*.py")
    runner = unittest.TextTestRunner()
    runner.run(suite)

# --- Main Execution ---
if __name__ == "__main__":
    # Cleanup any previous test runs
    if os.path.exists(TASK_MODULE_DIR):
        print(f"Cleaning up existing module directory: {TASK_MODULE_DIR}")
        shutil.rmtree(TASK_MODULE_DIR)

    setup_module()
    run_tests()

    # --- Cleanup ---
    print("\nCleaning up test directory...")
    if os.path.exists(TASK_MODULE_DIR):
        shutil.rmtree(TASK_MODULE_DIR)
        print(f"Removed test directory: {TASK_MODULE_DIR}")

    print("\n--- All Test Cases Completed ---")