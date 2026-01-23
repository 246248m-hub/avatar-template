import os
import shutil
import tempfile
from collections import defaultdict

# --- Constants ---
ARABIC_ROOT = "Arabic"
ARABIC_TASKS_DIR = os.path.join(ARABIC_ROOT, "Tasks")
ARABIC_MODULES_DIR = os.path.join(ARABIC_ROOT, "Modules")
ARABIC_DATA_DIR = os.path.join(ARABIC_ROOT, "Data")

# Create directories if they don't exist
os.makedirs(ARABIC_TASKS_DIR, exist_ok=True)
os.makedirs(ARABIC_MODULES_DIR, exist_ok=True)
os.makedirs(ARABIC_DATA_DIR, exist_ok=True)

# --- Helper Functions ---

def available_module_names(refresh=False):
    """
    Lists all available module names in the ARABIC_MODULES_DIR.

    Args:
        refresh (bool): If True, forces a reload of the module list.

    Returns:
        list: A list of module names (filenames without .py extension).
    """
    global _available_modules  # Use a global to cache module names

    if refresh or not hasattr(_available_modules, '__iter__') or not _available_modules:
        _available_modules = []
        if os.path.exists(ARABIC_MODULES_DIR):
            for filename in os.listdir(ARABIC_MODULES_DIR):
                if filename.endswith(".py") and filename != "__init__.py":
                    _available_modules.append(filename[:-3])  # Remove .py extension
    return _available_modules

# Initialize module list on first call
_available_modules = []
available_module_names()

def load_module(module_name):
    """
    Loads a Python module from the ARABIC_MODULES_DIR.

    Args:
        module_name (str): The name of the module to load.

    Returns:
        module: The loaded Python module object, or None if not found.
    """
    if module_name not in available_module_names():
        print(f"Error: Module '{module_name}' not found in {ARABIC_MODULES_DIR}")
        return None

    module_path = os.path.join(ARABIC_MODULES_DIR, f"{module_name}.py")
    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"Error loading module '{module_name}': {e}")
        return None

def save_module(module_name, code):
    """
    Saves Python code as a module in the ARABIC_MODULES_DIR.

    Args:
        module_name (str): The name of the module to save.
        code (str): The Python code to save.
    """
    module_path = os.path.join(ARABIC_MODULES_DIR, f"{module_name}.py")
    try:
        with open(module_path, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"Module '{module_name}' saved to {module_path}")
        available_module_names(refresh=True)  # Refresh the list of available modules
    except Exception as e:
        print(f"Error saving module '{module_name}': {e}")

def delete_module(module_name):
    """
    Deletes a module from the ARABIC_MODULES_DIR.

    Args:
        module_name (str): The name of the module to delete.
    """
    module_path = os.path.join(ARABIC_MODULES_DIR, f"{module_name}.py")
    if os.path.exists(module_path):
        try:
            os.remove(module_path)
            print(f"Module '{module_name}' deleted from {module_path}")
            available_module_names(refresh=True)  # Refresh the list of available modules
        except Exception as e:
            print(f"Error deleting module '{module_name}': {e}")
    else:
        print(f"Module '{module_name}' not found at {module_path}")

# --- Core Functionality ---

def parse_arabic_text(text):
    """
    Parses Arabic text, performing basic tokenization and normalization.

    Args:
        text (str): The input Arabic text.

    Returns:
        list: A list of normalized Arabic tokens.
    """
    # Basic normalization: remove common extra spaces and diacritics
    normalized_text = text.strip()
    normalized_text = ' '.join(normalized_text.split()) # Remove extra whitespace
    # A more robust solution would involve libraries like PyArabic or Farasa for diacritics removal.
    # For this example, we'll assume text is mostly free of diacritics or they are not critical for parsing.

    # Simple tokenization by whitespace
    tokens = normalized_text.split(' ')

    # Further normalization might include:
    # - Removing punctuation (though some punctuation is part of Arabic)
    # - Normalizing different forms of Hamza (أ, إ, آ, ؤ, ئ) to a single form (e.g., 'أ')
    # - Normalizing different forms of Teh Marbuta (ة) to Heh (ه)
    # - Stemming or lemmatization (requires advanced libraries)

    # Example of Hamza normalization (basic)
    hamza_map = {'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ؤ': 'ء', 'ئ': 'ء'}
    normalized_tokens = []
    for token in tokens:
        processed_token = token
        if len(processed_token) > 0 and processed_token[0] in hamza_map:
            processed_token = hamza_map[processed_token[0]] + processed_token[1:]
        normalized_tokens.append(processed_token)

    return normalized_tokens

def generate_arabic_text(tokens):
    """
    Generates Arabic text from a list of tokens.

    Args:
        tokens (list): A list of Arabic tokens.

    Returns:
        str: The generated Arabic text.
    """
    # Simple joining of tokens with spaces
    return ' '.join(tokens)

def build_arabic_parsing_module(module_name, parsing_logic_code):
    """
    Builds and saves a new Python module for Arabic text parsing.

    Args:
        module_name (str): The name of the module to create.
        parsing_logic_code (str): The Python code defining the parsing functions.
    """
    # Ensure the module_name is valid for a Python identifier
    if not module_name.isidentifier():
        print(f"Error: Module name '{module_name}' is not a valid Python identifier.")
        return

    # Construct the full module code
    full_code = f"""
import re
import os
import shutil
import tempfile
import importlib.util
from collections import defaultdict

# Ensure the directory structure is maintained for modules
ARABIC_ROOT = "Arabic"
ARABIC_MODULES_DIR = os.path.join(ARABIC_ROOT, "Modules")
ARABIC_DATA_DIR = os.path.join(ARABIC_ROOT, "Data")
os.makedirs(ARABIC_MODULES_DIR, exist_ok=True)
os.makedirs(ARABIC_DATA_DIR, exist_ok=True)

# --- Module-specific Parsing Logic ---
{parsing_logic_code}

# --- Helper functions expected by the system ---
def available_module_names(refresh=False):
    # This is a placeholder. The system manages available modules globally.
    # For the purpose of this module, it just needs to be present.
    pass

def load_module(module_name):
    # This is a placeholder. The system manages module loading.
    pass

def save_module(module_name, code):
    # This is a placeholder. The system manages module saving.
    pass

def delete_module(module_name):
    # This is a placeholder. The system manages module deletion.
    pass
"""
    save_module(module_name, full_code)

def build_arabic_generation_module(module_name, generation_logic_code):
    """
    Builds and saves a new Python module for Arabic text generation.

    Args:
        module_name (str): The name of the module to create.
        generation_logic_code (str): The Python code defining the generation functions.
    """
    # Ensure the module_name is valid for a Python identifier
    if not module_name.isidentifier():
        print(f"Error: Module name '{module_name}' is not a valid Python identifier.")
        return

    # Construct the full module code
    full_code = f"""
import re
import os
import shutil
import tempfile
import importlib.util
from collections import defaultdict

# Ensure the directory structure is maintained for modules
ARABIC_ROOT = "Arabic"
ARABIC_MODULES_DIR = os.path.join(ARABIC_ROOT, "Modules")
ARABIC_DATA_DIR = os.path.join(ARABIC_ROOT, "Data")
os.makedirs(ARABIC_MODULES_DIR, exist_ok=True)
os.makedirs(ARABIC_DATA_DIR, exist_ok=True)

# --- Module-specific Generation Logic ---
{generation_logic_code}

# --- Helper functions expected by the system ---
def available_module_names(refresh=False):
    # This is a placeholder. The system manages available modules globally.
    # For the purpose of this module, it just needs to be present.
    pass

def load_module(module_name):
    # This is a placeholder. The system manages module loading.
    pass

def save_module(module_name, code):
    # This is a placeholder. The system manages module saving.
    pass

def delete_module(module_name):
    # This is a placeholder. The system manages module deletion.
    pass
"""
    save_module(module_name, full_code)


# --- Example Usage and Testing ---
import unittest
import importlib.util

class TestArabicParsingGeneration(unittest.TestCase):

    def setUp(self):
        """Set up for test cases."""
        # Create a temporary directory for task-specific files
        self.TEST_TASK_DIR = tempfile.mkdtemp()
        print(f"\nCreated temporary test directory: {self.TEST_TASK_DIR}")

        # Ensure the Arabic root and module directories exist for the tests
        os.makedirs(ARABIC_MODULES_DIR, exist_ok=True)
        os.makedirs(ARABIC_DATA_DIR, exist_ok=True)

        # Add the current directory to sys.path to allow importing modules from ARABIC_MODULES_DIR
        import sys
        sys.path.insert(0, ARABIC_MODULES_DIR)

    def tearDown(self):
        """Clean up after test cases."""
        # Remove the temporary directory
        if os.path.exists(self.TEST_TASK_DIR):
            shutil.rmtree(self.TEST_TASK_DIR)
            print(f"Removed temporary test directory: {self.TEST_TASK_DIR}")

        # Remove the current directory from sys.path
        import sys
        if ARABIC_MODULES_DIR in sys.path:
            sys.path.remove(ARABIC_MODULES_DIR)

        # Cleanup created modules for a clean slate in subsequent runs
        for mod_name in available_module_names():
            if mod_name.startswith("test_"): # Only clean up test modules
                delete_module(mod_name)
        available_module_names(refresh=True) # Refresh after deletion


    def test_basic_parsing_and_generation(self):
        """Test basic Arabic text parsing and generation."""
        arabic_text = "السلام عليكم يا عالم!"
        tokens = parse_arabic_text(arabic_text)
        generated_text = generate_arabic_text(tokens)

        self.assertEqual(tokens, ["السلام", "عليكم", "يا", "عالم!"])
        self.assertEqual(generated_text, "السلام عليكم يا عالم!")

    def test_normalization_parsing(self):
        """Test normalization within parsing."""
        text_with_extra_spaces = "   مرحباً   بالعالم   "
        tokens = parse_arabic_text(text_with_extra_spaces)
        self.assertEqual(tokens, ["مرحباً", "بالعالم"])

        text_with_different_hamza = "إنه أمرٌ أروع!"
        tokens_hamza = parse_arabic_text(text_with_different_hamza)
        # Expecting 'ا' for 'إ' and 'ا' for 'أ' with this basic normalization
        self.assertEqual(tokens_hamza, ["انه", "امرٌ", "اروع!"])

    def test_building_and_loading_parsing_module(self):
        """Test building and loading a custom Arabic parsing module."""
        module_name = "custom_parser_v1"
        parsing_code = """
def parse_custom_arabic(text):
    # A very simple custom parser that splits by ' ' and '!'
    text = text.replace('!', ' ').strip()
    return text.split(' ')

def generate_custom_arabic(tokens):
    return ' '.join(tokens)
"""
        build_arabic_parsing_module(module_name, parsing_code)

        # Verify the module is available
        self.assertIn(module_name, available_module_names())

        # Load the module
        loaded_module = load_module(module_name)
        self.assertIsNotNone(loaded_module)

        # Test the functions from the loaded module
        test_text = "مرحباً بالعالم!"
        custom_tokens = loaded_module.parse_custom_arabic(test_text)
        self.assertEqual(custom_tokens, ["مرحباً", "بالعالم"])

        generated_text_from_module = loaded_module.generate_custom_arabic(custom_tokens)
        self.assertEqual(generated_text_from_module, "مرحباً بالعالم")

    def test_building_and_loading_generation_module(self):
        """Test building and loading a custom Arabic generation module."""
        module_name = "custom_generator_v1"
        generation_code = """
def generate_custom_arabic_text(tokens):
    # Joins tokens, adds a period at the end if missing
    text = '-'.join(tokens)
    if not text.endswith('.'):
        text += '.'
    return text

def parse_custom_arabic_text(text):
    # Dummy parser for this test
    return text.split('-')
"""
        build_arabic_generation_module(module_name, generation_code)

        # Verify the module is available
        self.assertIn(module_name, available_module_names())

        # Load the module
        loaded_module = load_module(module_name)
        self.assertIsNotNone(loaded_module)

        # Test the functions from the loaded module
        test_tokens = ["اليوم", "جميل"]
        generated_text = loaded_module.generate_custom_arabic_text(test_tokens)
        self.assertEqual(generated_text, "اليوم-جميل.")

        parsed_tokens = loaded_module.parse_custom_arabic_text(generated_text)
        self.assertEqual(parsed_tokens, ["اليوم", "جميل."])

    def test_deleting_module(self):
        """Test deleting a created module."""
        module_name = "module_to_delete_test"
        # Create a dummy module first
        save_module(module_name, "print('This is a dummy module.')")
        self.assertIn(module_name, available_module_names())

        delete_module(module_name)
        self.assertNotIn(module_name, available_module_names())

        # Test deleting a non-existent module
        delete_module("non_existent_module_123") # Should not raise an error and print a message

    def test_available_module_names_refresh(self):
        """Test the refresh functionality of available_module_names."""
        initial_modules = available_module_names()
        module_name = "refresh_test_module"
        save_module(module_name, "# Test module")
        new_modules = available_module_names()
        self.assertIn(module_name, new_modules)
        self.assertNotIn(module_name, initial_modules)

        available_module_names(refresh=True) # Explicitly refresh
        self.assertIn(module_name, available_module_names())

        delete_module(module_name)


if __name__ == "__main__":
    import sys
    import importlib.util

    # Ensure the ARABIC_MODULES_DIR is in sys.path for potential imports during execution
    if ARABIC_MODULES_DIR not in sys.path:
        sys.path.insert(0, ARABIC_MODULES_DIR)

    # Create a dummy __init__.py file for the Modules directory if it doesn't exist
    init_py_path = os.path.join(ARABIC_MODULES_DIR, "__init__.py")
    if not os.path.exists(init_py_path):
        with open(init_py_path, "w") as f:
            pass # Empty init file

    print("Running tests for Arabic Text Parsing and Generation module...")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

    # --- Demonstration of core functionality ---
    print("\n--- Demonstrating Core Functionality ---")

    # 1. Basic Parsing and Generation
    sample_text = "مرحباً بالعالم، كيف حالك اليوم؟"
    print(f"\nOriginal text: {sample_text}")
    parsed_tokens = parse_arabic_text(sample_text)
    print(f"Parsed tokens: {parsed_tokens}")
    generated_text = generate_arabic_text(parsed_tokens)
    print(f"Generated text: {generated_text}")

    # 2. Building and Using a Custom Parsing Module
    print("\n--- Building and Using a Custom Parsing Module ---")
    custom_parser_name = "my_advanced_parser"
    custom_parser_code = """
import re

def parse_advanced_arabic(text):
    # Example: Remove specific punctuation, normalize Hamza, split by space
    text = re.sub(r'[،؟!;]', '', text) # Remove common Arabic punctuation
    hamza_map = {'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ؤ': 'ء', 'ئ': 'ء'}
    processed_text = ""
    for char in text:
        if char in hamza_map:
            processed_text += hamza_map[char]
        else:
            processed_text += char
    return processed_text.split()

def generate_advanced_arabic(tokens):
    return ' '.join(tokens)
"""
    build_arabic_parsing_module(custom_parser_name, custom_parser_code)

    if custom_parser_name in available_module_names():
        custom_module = load_module(custom_parser_name)
        if custom_module:
            advanced_text = "أهلاً و سهلاً، كيف الأوضاع؟!"
            print(f"Advanced text: {advanced_text}")
            advanced_tokens = custom_module.parse_advanced_arabic(advanced_text)
            print(f"Parsed tokens (custom module): {advanced_tokens}")
            generated_advanced_text = custom_module.generate_advanced_arabic(advanced_tokens)
            print(f"Generated text (custom module): {generated_advanced_text}")
    else:
        print(f"Failed to load custom parser module '{custom_parser_name}'.")

    # 3. Building and Using a Custom Generation Module
    print("\n--- Building and Using a Custom Generation Module ---")
    custom_generator_name = "my_sentence_builder"
    custom_generator_code = """
def build_sentence_arabic(tokens):
    # Joins tokens and ensures it ends with a period.
    sentence = ' '.join(tokens)
    if not sentence.endswith('。'):
        sentence += '。'
    return sentence

def tokenize_for_sentence_builder(text):
    # Basic tokenizer for this builder
    return text.split()
"""
    build_arabic_generation_module(custom_generator_name, custom_generator_code)

    if custom_generator_name in available_module_names():
        custom_gen_module = load_module(custom_generator_name)
        if custom_gen_module:
            sentence_tokens = ["هذا", "نص", "جديد"]
            print(f"Tokens for sentence builder: {sentence_tokens}")
            built_sentence = custom_gen_module.build_sentence_arabic(sentence_tokens)
            print(f"Built sentence (custom module): {built_sentence}")
    else:
        print(f"Failed to load custom generator module '{custom_generator_name}'.")


    # --- Cleanup ---
    print("\nCleaning up created modules...")
    for mod_name in ["custom_parser_v1", "custom_generator_v1", "my_advanced_parser", "my_sentence_builder"]:
        if mod_name in available_module_names():
            delete_module(mod_name)
    print("Cleanup complete.")

    # Clean up the ARABIC_ROOT directory if it's empty and not needed
    # This is optional and depends on whether you want to keep the structure
    # if os.path.exists(ARABIC_ROOT) and not os.listdir(ARABIC_ROOT):
    #     os.rmdir(ARABIC_ROOT)
    #     print(f"Removed empty directory: {ARABIC_ROOT}")

    print("\n--- All Tasks Completed ---")