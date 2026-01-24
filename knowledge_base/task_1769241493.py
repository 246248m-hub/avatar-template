import os
import shutil
import sys
import subprocess
import re

# Define a placeholder for the main testing directory
TEST_TASK_DIR = "temp_arabic_parser_tests"

def create_test_directory():
    """Creates the test directory if it doesn't exist."""
    if not os.path.exists(TEST_TASK_DIR):
        os.makedirs(TEST_TASK_DIR)
        print(f"Created test directory: {TEST_TASK_DIR}")

def clean_test_directory():
    """Removes the test directory and its contents."""
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
        print(f"Removed test directory: {TEST_TASK_DIR}")

def create_python_file(filename, content):
    """Creates a Python file in the test directory."""
    filepath = os.path.join(TEST_TASK_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath

def run_python_script(filepath):
    """Runs a Python script and returns its stdout and stderr."""
    try:
        result = subprocess.run(
            [sys.executable, filepath],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        print(f"Error running script {filepath}:")
        print(f"STDOUT:\n{e.stdout}")
        print(f"STDERR:\n{e.stderr}")
        raise

# --- Module Building - Arabic Text Parsing and Generation ---

ARABIC_PARSER_MODULE_CONTENT = """
import re

class ArabicTextParser:
    def __init__(self):
        # Basic Arabic character ranges (consonants, vowels, etc.)
        # This is a simplification and might need expansion for full support
        self.arabic_chars = re.compile(r'^[\\u0600-\\u06FF]+$')
        # Pattern to detect common Arabic words, including diacritics
        self.word_pattern = re.compile(r'[\\u0621-\\u064A\\u064B-\\u0652]+')

    def is_arabic(self, text):
        \"\"\"Checks if the entire string consists of Arabic characters.\"\"\"
        if not text:
            return False
        return bool(self.arabic_chars.match(text))

    def extract_words(self, text):
        \"\"\"Extracts all Arabic words from a given text.\"\"\"
        if not text:
            return []
        return self.word_pattern.findall(text)

    def remove_diacritics(self, text):
        \"\"\"Removes diacritics (tashkeel) from Arabic text.\"\"\"
        # Diacritics range: U+064B - U+0652
        return re.sub(r'[\\u064B-\\u0652]', '', text)

    def generate_simple_arabic_sentence(self, words):
        \"\"\"Generates a simple Arabic sentence from a list of words.\"\"\"
        if not words:
            return ""
        return " ".join(words) + "।" # Using a full stop character

class ArabicTextGenerator:
    def __init__(self):
        self.greetings = ["مرحبا", "أهلا", "السلام عليكم"]
        self.farewells = ["وداعا", "إلى اللقاء"]
        self.common_nouns = ["كتاب", "قلم", "بيت", "سيارة"]
        self.common_verbs = ["يقرأ", "يكتب", "يذهب", "يأكل"]

    def create_greeting(self):
        \"\"\"Generates a random Arabic greeting.\"\"\"
        import random
        return random.choice(self.greetings)

    def create_farewell(self):
        \"\"\"Generates a random Arabic farewell.\"\"\"
        import random
        return random.choice(self.farewells)

    def create_simple_sentence(self):
        \"\"\"Generates a very simple, grammatically questionable, Arabic sentence.\"\"\"
        import random
        subject = random.choice(self.common_nouns)
        verb = random.choice(self.common_verbs)
        return f"{subject} {verb}।"

if __name__ == '__main__':
    print("--- Arabic Text Parser and Generator Module Test ---")

    # Test Parser
    print("\\nTesting ArabicTextParser:")
    parser = ArabicTextParser()

    arabic_text_with_diacritics = "بِسْمِ ٱللَّٰهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"
    arabic_text_no_diacritics = "بسم الله الرحمن الرحيم"
    mixed_text = "This is an English sentence with كلمة عربية."
    empty_text = ""

    print(f"Is '{arabic_text_with_diacritics}' Arabic? {parser.is_arabic(arabic_text_with_diacritics)}")
    print(f"Is '{arabic_text_no_diacritics}' Arabic? {parser.is_arabic(arabic_text_no_diacritics)}")
    print(f"Is '{mixed_text}' Arabic? {parser.is_arabic(mixed_text)}")
    print(f"Is '{empty_text}' Arabic? {parser.is_arabic(empty_text)}")

    print(f"Extracting words from '{arabic_text_with_diacritics}': {parser.extract_words(arabic_text_with_diacritics)}")
    print(f"Extracting words from '{arabic_text_no_diacritics}': {parser.extract_words(arabic_text_no_diacritics)}")
    print(f"Extracting words from '{mixed_text}': {parser.extract_words(mixed_text)}")
    print(f"Extracting words from '{empty_text}': {parser.extract_words(empty_text)}")

    print(f"Removing diacritics from '{arabic_text_with_diacritics}': {parser.remove_diacritics(arabic_text_with_diacritics)}")
    print(f"Removing diacritics from '{arabic_text_no_diacritics}': {parser.remove_diacritics(arabic_text_no_diacritics)}")

    sentence_to_parse = ["هذه", "جملة", "مفيدة"]
    print(f"Generating sentence from {sentence_to_parse}: {parser.generate_simple_arabic_sentence(sentence_to_parse)}")
    print(f"Generating sentence from []: {parser.generate_simple_arabic_sentence([])}")


    # Test Generator
    print("\\nTesting ArabicTextGenerator:")
    generator = ArabicTextGenerator()

    print(f"Generated greeting: {generator.create_greeting()}")
    print(f"Generated farewell: {generator.create_farewell()}")
    for _ in range(3):
        print(f"Generated simple sentence: {generator.create_simple_sentence()}")

    print("\\n--- Module Test Completed ---")
"""

# --- Test Cases ---

def test_arabic_parser_module():
    """Tests the Arabic Text Parsing and Generation module."""
    print("\n--- Running Test: Arabic Parser Module ---")
    module_filename = "arabic_parser_generator.py"
    module_filepath = create_python_file(module_filename, ARABIC_PARSER_MODULE_CONTENT)

    stdout, stderr = run_python_script(module_filepath)

    print("--- STDOUT ---")
    print(stdout)
    print("--- STDERR ---")
    print(stderr)

    assert "--- Arabic Text Parser and Generator Module Test ---" in stdout
    assert "Testing ArabicTextParser:" in stdout
    assert "Is 'بِسْمِ ٱللَّٰهِ ٱٱلرَّحْمَٰنِ ٱلرَّحِيمِ' Arabic? True" in stdout
    assert "Is 'بسم الله الرحمن الرحيم' Arabic? True" in stdout
    assert "Is 'This is an English sentence with كلمة عربية.' Arabic? False" in stdout
    assert "Is '' Arabic? False" in stdout
    assert "Extracting words from 'بِسْمِ ٱللَّٰهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ': ['بِسْمِ', 'ٱللَّٰهِ', 'ٱلرَّحْمَٰنِ', 'ٱلرَّحِيمِ']" in stdout
    assert "Extracting words from 'بسم الله الرحمن الرحيم': ['بسم', 'الله', 'الرحمن', 'الرحيم']" in stdout
    assert "Extracting words from 'This is an English sentence with كلمة عربية.': ['كلمة', 'عربية']" in stdout
    assert "Extracting words from '': []" in stdout
    assert "Removing diacritics from 'بِسْمِ ٱللَّٰهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ': 'بسم الله الرحمن الرحيم'" in stdout
    assert "Removing diacritics from 'بسم الله الرحمن الرحيم': 'بسم الله الرحمن الرحيم'" in stdout
    assert "Generating sentence from ['هذه', 'جملة', 'مفيدة']: هذه جملة مفيدة।" in stdout
    assert "Generating sentence from []: " in stdout
    assert "Testing ArabicTextGenerator:" in stdout
    assert "Generated greeting:" in stdout
    assert "Generated farewell:" in stdout
    assert "Generated simple sentence:" in stdout
    assert "--- Module Test Completed ---" in stdout

    print("Test Passed: Arabic Parser Module")

# --- Main Execution Flow ---

def main():
    """Main function to run all tests."""
    create_test_directory()

    try:
        test_arabic_parser_module()
        # Add more test functions here as needed for other modules

    except Exception as e:
        print(f"\n!!! An error occurred during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) # Indicate failure

    finally:
        # --- Cleanup ---
        print("\nCleaning up test directory...")
        if os.path.exists(TEST_TASK_DIR):
            shutil.rmtree(TEST_TASK_DIR)
            print(f"Removed test directory: {TEST_TASK_DIR}")

        print("\n--- All Test Cases Completed ---")

if __name__ == "__main__":
    main()