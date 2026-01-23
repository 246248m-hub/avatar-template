import os
import shutil
import sys

TEST_TASK_DIR = "test_task_arabic_parsing"


def available_module_names():
    """Returns a list of all loaded module names."""
    return set(sys.modules.keys())


def setup_test_environment():
    """Sets up a clean test environment."""
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
    os.makedirs(TEST_TASK_DIR)
    print(f"Created test directory: {TEST_TASK_DIR}")


def cleanup_test_environment():
    """Cleans up the test environment."""
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
        print(f"Removed test directory: {TEST_TASK_DIR}")


def create_mock_pytest_file():
    """Creates a mock pytest file to avoid ModuleNotFoundError."""
    mock_pytest_content = """
def mark(name):
    def decorator(func):
        return func
    return decorator

class MockFixture:
    def __call__(self, *args, **kwargs):
        pass

fixture = MockFixture()
"""
    with open(os.path.join(TEST_TASK_DIR, "mock_pytest.py"), "w", encoding="utf-8") as f:
        f.write(mock_pytest_content)
    sys.path.insert(0, TEST_TASK_DIR)
    print("Created mock_pytest.py")


def remove_mock_pytest_from_path():
    """Removes the mock pytest from sys.path."""
    if TEST_TASK_DIR in sys.path:
        sys.path.remove(TEST_TASK_DIR)
    if os.path.exists(os.path.join(TEST_TASK_DIR, "mock_pytest.py")):
        os.remove(os.path.join(TEST_TASK_DIR, "mock_pytest.py"))
        print("Removed mock_pytest.py")


def test_arabic_parsing_module():
    """
    This test case aims to build a foundational module for Arabic text parsing and generation.
    It will create a simple module that can identify Arabic characters and potentially
    perform basic tokenization.
    """
    module_code = """
import re

def is_arabic_char(char):
    \"\"\"Checks if a character is an Arabic letter.\"\"\"
    # Arabic block range
    return '\u0600' <= char <= '\u06FF'

def tokenize_arabic_text(text):
    \"\"\"
    Basic tokenizer for Arabic text.
    Splits by common punctuation and whitespace.
    \"\"\"
    # Remove punctuation and split by whitespace
    tokens = re.split(r'[\\s\\u060c\\u061b\\u061f\\u0021\\u003f\\u002c\\u003b\\u003a\\u2013\\u2014]+', text)
    # Filter out empty strings that might result from multiple delimiters
    return [token for token in tokens if token]

def generate_simple_arabic_sentence(words):
    \"\"\"Generates a simple Arabic sentence from a list of words.\"\"\"
    return " ".join(words) + "।" # Using a common Arabic full stop

# Example usage (optional, for demonstration)
if __name__ == "__main__":
    arabic_string = "مرحبا بالعالم! كيف حالك اليوم؟"
    print(f"Original string: {arabic_string}")

    print("Checking for Arabic characters:")
    for char in arabic_string:
        if is_arabic_char(char):
            print(f"'{char}' is an Arabic character.")
        else:
            print(f"'{char}' is NOT an Arabic character.")

    print("\\nTokenizing the string:")
    tokens = tokenize_arabic_text(arabic_string)
    print(f"Tokens: {tokens}")

    generated_sentence = generate_simple_arabic_sentence(["هذا", "مثال"])
    print(f"Generated sentence: {generated_sentence}")
"""
    module_filename = os.path.join(TEST_TASK_DIR, "arabic_parser.py")
    with open(module_filename, "w", encoding="utf-8") as f:
        f.write(module_code)
    print(f"Created module file: {module_filename}")

    # Dynamically import the created module
    try:
        # Ensure the directory is in sys.path for import
        sys.path.insert(0, TEST_TASK_DIR)
        import arabic_parser
        print("Successfully imported arabic_parser module.")

        # Test the module functions
        test_string = "السلام عليكم ورحمة الله وبركاته."
        print(f"\nTesting with: '{test_string}'")

        # Test is_arabic_char
        assert arabic_parser.is_arabic_char('ا') is True
        assert arabic_parser.is_arabic_char('A') is False
        assert arabic_parser.is_arabic_char(' ') is False
        print("is_arabic_char tests passed.")

        # Test tokenize_arabic_text
        sample_text_for_tokenize = "أهلاً، يا عالم! كيف الحال؟"
        tokens = arabic_parser.tokenize_arabic_text(sample_text_for_tokenize)
        print(f"Tokens for '{sample_text_for_tokenize}': {tokens}")
        assert tokens == ['أهلاً', 'يا', 'عالم', 'كيف', 'الحال']
        print("tokenize_arabic_text tests passed.")

        # Test generate_simple_arabic_sentence
        words_to_join = ["اليوم", "جميل"]
        generated = arabic_parser.generate_simple_arabic_sentence(words_to_join)
        print(f"Generated sentence from {words_to_join}: '{generated}'")
        assert generated == "اليوم جميل।"
        print("generate_simple_arabic_sentence tests passed.")

        print("\n--- Arabic Parsing Module Test Case Completed ---")

    except ImportError as e:
        print(f"Error importing module: {e}")
        assert False, f"Failed to import the generated module: {e}"
    except Exception as e:
        print(f"An unexpected error occurred during testing: {e}")
        assert False, f"An unexpected error occurred during testing: {e}"
    finally:
        # Clean up sys.path and the module file
        if TEST_TASK_DIR in sys.path:
            sys.path.remove(TEST_TASK_DIR)


if __name__ == "__main__":
    # --- Setup ---
    setup_test_environment()
    create_mock_pytest_file()

    try:
        # --- Run Test Cases ---
        print("\n--- Running Test Cases ---")
        test_arabic_parsing_module()

    finally:
        # --- Cleanup ---
        print("\nCleaning up test directory...")
        remove_mock_pytest_from_path()
        cleanup_test_environment()

    print("\n--- All Test Cases Completed ---")