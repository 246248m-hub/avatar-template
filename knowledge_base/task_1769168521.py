import os
import shutil
import unittest

# Define a placeholder for the task directory
TEST_TASK_DIR = "arabic_parsing_module_test"

# Mock functions for demonstration purposes
def create_module(module_name, code):
    """Creates a Python module file."""
    if not os.path.exists(TEST_TASK_DIR):
        os.makedirs(TEST_TASK_DIR)
    file_path = os.path.join(TEST_TASK_DIR, f"{module_name}.py")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"Created module: {file_path}")
    return file_path

def available_module_names():
    """Simulates finding available modules in the task directory."""
    if not os.path.exists(TEST_TASK_DIR):
        return []
    return [f.replace(".py", "") for f in os.listdir(TEST_TASK_DIR) if f.endswith(".py")]

def load_module(module_name):
    """Simulates loading a module by dynamically creating and importing it."""
    # In a real scenario, this would involve importing from the task directory.
    # For this mock, we'll assume it's already created and can be imported directly.
    print(f"Simulating loading module: {module_name}")
    try:
        # This is a simplified mock. In a real system, you'd need to manage
        # the Python path or use importlib to load from a specific directory.
        import importlib
        return importlib.import_module(f"{TEST_TASK_DIR}.{module_name}")
    except ModuleNotFoundError:
        print(f"Module {module_name} not found.")
        return None


class TestArabicParsingModule(unittest.TestCase):

    def setUp(self):
        """Set up test environment by creating the task directory."""
        if os.path.exists(TEST_TASK_DIR):
            shutil.rmtree(TEST_TASK_DIR)
        os.makedirs(TEST_TASK_DIR)
        print(f"\nSetting up test directory: {TEST_TASK_DIR}")

    def tearDown(self):
        """Clean up the test environment by removing the task directory."""
        print("\nCleaning up test directory...")
        if os.path.exists(TEST_TASK_DIR):
            shutil.rmtree(TEST_TASK_DIR)
            print(f"Removed test directory: {TEST_TASK_DIR}")

    def test_module_creation_and_loading(self):
        """Tests if a module can be created and then loaded."""
        module_name = "arabic_utils"
        module_code = """
def parse_arabic(text):
    '''Parses Arabic text, returning a simplified representation.'''
    return text.lower().strip()

def generate_arabic_greeting(name):
    '''Generates a simple Arabic greeting.'''
    return f"مرحباً يا {name}!"
"""
        create_module(module_name, module_code)

        # Ensure the module is visible for loading
        import sys
        sys.path.insert(0, TEST_TASK_DIR)
        importlib.invalidate_caches()

        loaded_module = load_module(module_name)
        self.assertIsNotNone(loaded_module, f"Module '{module_name}' should be loaded successfully.")

        # Test functions within the loaded module
        self.assertTrue(hasattr(loaded_module, 'parse_arabic'))
        self.assertTrue(hasattr(loaded_module, 'generate_arabic_greeting'))

        parsed_text = loaded_module.parse_arabic("  ٱلسَّلَامُ عَلَيْكُم ")
        self.assertEqual(parsed_text, "ٱلسَّلَامُ عَلَيْكُم") # Basic stripping and lowercasing

        greeting = loaded_module.generate_arabic_greeting("علي")
        self.assertEqual(greeting, "مرحباً يا علي!")

        # Clean up sys.path modification
        sys.path.pop(0)
        importlib.invalidate_caches()

    def test_multiple_module_loading(self):
        """Tests loading multiple modules."""
        module1_name = "arabic_parser"
        module1_code = "def parse_word(word): return f'parsed_{word}'"
        create_module(module1_name, module1_code)

        module2_name = "arabic_generator"
        module2_code = "def generate_sentence(words): return ' '.join(words)"
        create_module(module2_name, module2_code)

        # Add directory to sys.path to allow dynamic imports
        import sys
        sys.path.insert(0, TEST_TASK_DIR)
        importlib.invalidate_caches()

        module_names_before = available_module_names()
        self.assertIn(module1_name, module_names_before)
        self.assertIn(module2_name, module_names_before)

        loaded_module1 = load_module(module1_name)
        loaded_module2 = load_module(module2_name)

        self.assertIsNotNone(loaded_module1)
        self.assertIsNotNone(loaded_module2)

        self.assertEqual(loaded_module1.parse_word("test"), "parsed_test")
        self.assertEqual(loaded_module2.generate_sentence(["hello", "world"]), "hello world")

        # Clean up sys.path modification
        sys.path.pop(0)
        importlib.invalidate_caches()

    def test_empty_task_directory(self):
        """Tests that available_module_names returns empty list when directory is empty."""
        # Ensure the directory is empty or doesn't exist before this test
        if os.path.exists(TEST_TASK_DIR):
            shutil.rmtree(TEST_TASK_DIR)
        os.makedirs(TEST_TASK_DIR) # Create an empty directory

        available = available_module_names()
        self.assertEqual(available, [], "available_module_names should return an empty list for an empty directory.")

    def test_non_existent_module_load(self):
        """Tests loading a module that does not exist."""
        module_name = "non_existent_module"
        # Ensure the module is not created
        if os.path.exists(os.path.join(TEST_TASK_DIR, f"{module_name}.py")):
            os.remove(os.path.join(TEST_TASK_DIR, f"{module_name}.py"))

        # Add directory to sys.path to allow dynamic imports
        import sys
        sys.path.insert(0, TEST_TASK_DIR)
        importlib.invalidate_caches()

        loaded_module = load_module(module_name)
        self.assertIsNone(loaded_module, f"Loading a non-existent module '{module_name}' should return None.")

        # Clean up sys.path modification
        sys.path.pop(0)
        importlib.invalidate_caches()


if __name__ == '__main__':
    # Create the task directory if it doesn't exist for the initial setup
    if not os.path.exists(TEST_TASK_DIR):
        os.makedirs(TEST_TASK_DIR)
        print(f"Created initial test directory: {TEST_TASK_DIR}")

    # The original error was related to memory management or module loading scope.
    # The fix involves ensuring modules are correctly loaded and unloaded/invalidated
    # from the cache, especially when the test environment changes.
    # The `setUp` and `tearDown` methods handle directory creation and deletion.
    # The `sys.path` manipulation and `importlib.invalidate_caches()` are crucial
    # for dynamic module loading and unloading in test environments.

    unittest.main(argv=['first-arg-is-ignored'], exit=False)