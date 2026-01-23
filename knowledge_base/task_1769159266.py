import os
import shutil
import unittest

# Assume these are defined elsewhere in your project structure
# For this example, we'll create dummy versions
AVAILABLE_MODULES = {}

def load_module(module_name):
    if module_name in AVAILABLE_MODULES:
        return AVAILABLE_MODULES[module_name]
    else:
        raise ModuleNotFoundError(f"Module '{module_name}' not found.")

def register_module(module_name, module_instance):
    AVAILABLE_MODULES[module_name] = module_instance

def available_module_names():
    return list(AVAILABLE_MODULES.keys())

class ArabicParser:
    def parse(self, text):
        # Dummy parsing logic for demonstration
        return {"original": text, "processed": text.lower()}

class ArabicGenerator:
    def generate(self, data):
        # Dummy generation logic for demonstration
        return data.get("processed", "")

# Define the directory for test files
TEST_TASK_DIR = "test_arabic_parsing_gen"

class TestArabicParsingGeneration(unittest.TestCase):

    def setUp(self):
        """Set up a clean environment for each test."""
        print("\nSetting up test environment...")
        if os.path.exists(TEST_TASK_DIR):
            shutil.rmtree(TEST_TASK_DIR)
        os.makedirs(TEST_TASK_DIR)
        print(f"Created test directory: {TEST_TASK_DIR}")

        # Register dummy modules for testing
        self.parser = ArabicParser()
        self.generator = ArabicGenerator()
        register_module("arabic_parser", self.parser)
        register_module("arabic_generator", self.generator)
        print("Registered dummy modules: arabic_parser, arabic_generator")

    def tearDown(self):
        """Clean up the test environment after each test."""
        # Memory: vailable_module_names() # Should be loaded again
        # This line seems to indicate a potential issue where available_module_names()
        # might not reflect the current state if modules were unregistered or
        # if the global AVAILABLE_MODULES was modified elsewhere.
        # For this specific test case, we'll assume it's meant to check the state
        # after the test runs, but since we're only registering, it's less critical here.
        # If there were unregistration calls, a reload might be necessary.
        # We'll simulate a check that it returns the registered modules.
        registered_modules_after = available_module_names()
        print(f"Modules available after test: {registered_modules_after}")
        self.assertIn("arabic_parser", registered_modules_after)
        self.assertIn("arabic_generator", registered_modules_after)

        print("\nCleaning up test directory...")
        if os.path.exists(TEST_TASK_DIR):
            shutil.rmtree(TEST_TASK_DIR)
            print(f"Removed test directory: {TEST_TASK_DIR}")

    def test_parsing_and_generation(self):
        """Test the basic parsing and generation flow."""
        print("\nRunning test_parsing_and_generation...")

        # Simulate loading modules
        loaded_parser = load_module("arabic_parser")
        loaded_generator = load_module("arabic_generator")

        # Test parsing
        arabic_text = "مرحباً بالعالم"  # "Hello World" in Arabic
        parsed_data = loaded_parser.parse(arabic_text)
        self.assertEqual(parsed_data["original"], arabic_text)
        self.assertEqual(parsed_data["processed"], arabic_text.lower())
        print(f"Parsed data: {parsed_data}")

        # Test generation
        generated_text = loaded_generator.generate(parsed_data)
        self.assertEqual(generated_text, arabic_text.lower())
        print(f"Generated text: {generated_text}")

    def test_module_loading_and_availability(self):
        """Test that modules are loaded and available correctly."""
        print("\nRunning test_module_loading_and_availability...")

        # Check initial availability
        initial_modules = available_module_names()
        self.assertNotIn("arabic_parser", initial_modules)
        self.assertNotIn("arabic_generator", initial_modules)

        # Load modules
        loaded_parser = load_module("arabic_parser")
        loaded_generator = load_module("arabic_generator")

        # Check availability after loading (should not change based on current register_module)
        # If there were a separate mechanism to 'discover' loaded modules, this would be more relevant.
        # With current setup, available_module_names() reflects what's been *registered*.
        modules_after_load = available_module_names()
        self.assertIn("arabic_parser", modules_after_load)
        self.assertIn("arabic_generator", modules_after_load)
        self.assertIsInstance(loaded_parser, ArabicParser)
        self.assertIsInstance(loaded_generator, ArabicGenerator)
        print(f"Modules available after loading: {modules_after_load}")

        # Test loading a non-existent module
        with self.assertRaises(ModuleNotFoundError):
            load_module("non_existent_module")
        print("Successfully caught ModuleNotFoundError for non-existent module.")

# This block allows running the tests directly from the script
if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)