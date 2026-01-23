import os
import shutil
import re

TEST_TASK_DIR = "./arabic_parser_test"

def available_module_names():
    """
    Lists all available modules in the current directory.
    """
    modules = []
    for item in os.listdir("."):
        if item.endswith(".py") and not item.startswith("__"):
            modules.append(item[:-3])
    return modules

def setup_test_directory():
    """
    Sets up a temporary directory for testing the Arabic parsing and generation module.
    """
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
    os.makedirs(TEST_TASK_DIR)
    os.chdir(TEST_TASK_DIR)
    print(f"Test directory created and changed to: {os.getcwd()}")

def create_module_file(module_name, content):
    """
    Creates a Python file for a module with the given name and content.
    """
    with open(f"{module_name}.py", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created module file: {module_name}.py")

def create_arabic_parser_module(module_name="arabic_parser"):
    """
    Creates a basic Python module for Arabic text parsing and generation.
    """
    content = """
import re

class ArabicParser:
    def __init__(self):
        # Basic Arabic letters and common diacritics
        self.arabic_letters = "ءأإؤآبتثجحخدذرزسشصضطظعغـفـقـكلمنهويىة"
        self.diacritics = "ًٌٍَُِّْـ"
        self.all_arabic_chars = self.arabic_letters + self.diacritics

    def is_arabic(self, text):
        \"\"\"
        Checks if the given text contains predominantly Arabic characters.
        \"\"\"
        if not text:
            return False
        arabic_char_count = sum(1 for char in text if char in self.all_arabic_chars)
        return arabic_char_count / len(text) > 0.7

    def normalize_arabic(self, text):
        \"\"\"
        Normalizes Arabic text by removing extra spaces and some common variations.
        \"\"\"
        if not self.is_arabic(text):
            return text

        # Remove diacritics
        text = re.sub(f"[{self.diacritics}]", "", text)

        # Normalize alef forms
        text = re.sub("[أإآ]", "ا", text)

        # Normalize ya forms
        text = re.sub("[يى]", "ي", text)

        # Normalize ta marbuta
        text = re.sub("ة", "ه", text)

        # Remove extra spaces
        text = re.sub("\\s+", " ", text).strip()

        return text

    def parse_arabic_word(self, word):
        \"\"\"
        Parses a single Arabic word, separating it into letters.
        For simplicity, this only splits characters. More advanced parsing
        would involve morphology, roots, etc.
        \"\"\"
        if not self.is_arabic(word):
            return []
        return list(word)

    def generate_arabic_sentence(self, words):
        \"\"\"
        Generates an Arabic sentence from a list of words.
        Basic generation by joining words with spaces.
        \"\"\"
        if not all(isinstance(word, str) for word in words):
            raise TypeError("All elements in the list must be strings.")
        return " ".join(words)

if __name__ == '__main__':
    parser = ArabicParser()

    # Test is_arabic
    print(f"'السلام عليكم' is Arabic: {parser.is_arabic('السلام عليكم')}")
    print(f"'Hello world' is Arabic: {parser.is_arabic('Hello world')}")
    print(f"'مرحبا 123' is Arabic: {parser.is_arabic('مرحبا 123')}")
    print(f"'' is Arabic: {parser.is_arabic('')}")

    # Test normalize_arabic
    text_with_diacritics = "اَلْحَمْدُ لِلَّهِ رَبِّ اَلْعَالَمِينَ"
    print(f"Original: {text_with_diacritics}")
    print(f"Normalized: {parser.normalize_arabic(text_with_diacritics)}")
    text_with_alef_variations = "أإآ"
    print(f"Original: {text_with_alef_variations}")
    print(f"Normalized: {parser.normalize_arabic(text_with_alef_variations)}")
    text_with_ya_variations = "يى"
    print(f"Original: {text_with_ya_variations}")
    print(f"Normalized: {parser.normalize_arabic(text_with_ya_variations)}")
    text_with_ta_marbuta = "مكتبة"
    print(f"Original: {text_with_ta_marbuta}")
    print(f"Normalized: {parser.normalize_arabic(text_with_ta_marbuta)}")
    text_with_extra_spaces = "  هذا   نص   مع  مسافات   "
    print(f"Original: '{text_with_extra_spaces}'")
    print(f"Normalized: '{parser.normalize_arabic(text_with_extra_spaces)}'")


    # Test parse_arabic_word
    word_to_parse = "كتاب"
    print(f"Parsing '{word_to_parse}': {parser.parse_arabic_word(word_to_parse)}")
    word_with_non_arabic = "test123abc"
    print(f"Parsing '{word_with_non_arabic}': {parser.parse_arabic_word(word_with_non_arabic)}")

    # Test generate_arabic_sentence
    sentence_words = ["هذا", "مساء", "الخير"]
    print(f"Generating sentence from {sentence_words}: '{parser.generate_arabic_sentence(sentence_words)}'")
    try:
        parser.generate_arabic_sentence([1, 2, 3])
    except TypeError as e:
        print(f"Caught expected error: {e}")
"""
    create_module_file(module_name, content)
    return module_name

def run_test_case_arabic_parser():
    """
    Tests the ArabicParser module.
    """
    print("\n--- Running Test Case: Arabic Parser ---")
    setup_test_directory()
    module_name = create_arabic_parser_module()

    # Load the module dynamically for testing
    try:
        # Ensure the module is loaded in the current scope or reloaded if necessary
        # If the module was already imported, this might not update it.
        # A more robust approach for repeated testing in the same session would be to
        # remove it from sys.modules first. For this single run, direct import is fine.
        # For the error "// Memory: vailable_module_names() # Should be loaded again",
        # it implies that `available_module_names` might be called after the module
        # was created but not "refreshed" in the import system.
        # The act of creating the file and then attempting to import it ensures it's available.
        # If this were part of a larger system where the module might already be imported,
        # a reload mechanism would be needed.
        # For demonstration, let's assume we're running this in a clean environment or
        # simulating a first-time load.
        import arabic_parser
        print(f"Successfully imported module: {module_name}")

        # Execute the __main__ block of the created module to run its tests
        import runpy
        runpy.run_module(module_name, run_name="__main__")

        print(f"Test case for '{module_name}' completed successfully.")

    except ImportError:
        print(f"Error: Could not import module '{module_name}'. Ensure it was created correctly.")
    except Exception as e:
        print(f"An unexpected error occurred during test execution: {e}")
    finally:
        # Go back to the original directory
        os.chdir("..")
        print(f"Returned to original directory: {os.getcwd()}")

# --- Main Execution ---
if __name__ == "__main__":
    # --- Test Arabic Parser Module ---
    run_test_case_arabic_parser()

    # --- Cleanup ---
    print("\nCleaning up test directory...")
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
        print(f"Removed test directory: {TEST_TASK_DIR}")

    print("\n--- All Test Cases Completed ---")