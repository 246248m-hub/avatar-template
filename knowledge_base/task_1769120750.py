import os
import shutil
import unittest

# Define the directory for test files
TEST_TASK_DIR = "arabic_parsing_tests"

class ArabicTextModule:
    """
    A foundational module for Arabic text parsing and generation.
    """

    def __init__(self):
        """Initializes the ArabicTextModule."""
        pass

    def parse_arabic_text(self, text: str) -> dict:
        """
        Parses Arabic text, extracting meaningful components.

        Args:
            text: The Arabic text string to parse.

        Returns:
            A dictionary containing parsed information.
            Example: {'words': ['كلمة', 'أخرى'], 'letters': ['ك', 'ل', 'م', 'ة'], 'sentiment': 'neutral'}
        """
        # Placeholder implementation:
        # In a real-world scenario, this would involve:
        # - Tokenization (splitting text into words)
        # - Lemmatization/Stemming
        # - Part-of-Speech tagging
        # - Named Entity Recognition
        # - Sentiment Analysis
        words = text.split()  # Basic word splitting
        letters = list("".join(words))
        sentiment = "neutral" # Placeholder sentiment

        return {
            'words': words,
            'letters': letters,
            'sentiment': sentiment
        }

    def generate_arabic_text(self, data: dict) -> str:
        """
        Generates Arabic text from structured data.

        Args:
            data: A dictionary containing data to generate text from.
                  Example: {'topic': 'greeting', 'name': 'علي'}

        Returns:
            A generated Arabic text string.
        """
        # Placeholder implementation:
        # In a real-world scenario, this would involve:
        # - Template-based generation
        # - Rule-based generation
        # - Statistical/Neural language models
        if data.get('topic') == 'greeting' and data.get('name'):
            return f"مرحباً يا {data['name']}!"
        elif data.get('topic') == 'farewell':
            return "إلى اللقاء!"
        else:
            return "هذا نص تم إنشاؤه."

class TestArabicTextModule(unittest.TestCase):
    """
    Unit tests for the ArabicTextModule.
    """

    @classmethod
    def setUpClass(cls):
        """Set up the test environment."""
        print("\nSetting up test directory...")
        os.makedirs(TEST_TASK_DIR, exist_ok=True)
        print(f"Test directory created: {TEST_TASK_DIR}")

    @classmethod
    def tearDownClass(cls):
        """Clean up the test environment."""
        print("\nCleaning up test directory...")
        if os.path.exists(TEST_TASK_DIR):
            shutil.rmtree(TEST_TASK_DIR)
            print(f"Removed test directory: {TEST_TASK_DIR}")

    def setUp(self):
        """Set up for each test case."""
        self.arabic_module = ArabicTextModule()

    def test_parse_arabic_text_simple(self):
        """Test parsing of a simple Arabic sentence."""
        text = "السلام عليكم ورحمة الله وبركاته"
        parsed_data = self.arabic_module.parse_arabic_text(text)
        self.assertIn('words', parsed_data)
        self.assertIn('letters', parsed_data)
        self.assertIn('sentiment', parsed_data)
        self.assertEqual(parsed_data['words'], ['السلام', 'عليكم', 'ورحمة', 'الله', 'وبركاته'])
        self.assertEqual(parsed_data['letters'], list("السلامعليكمورحمةاللهوبركاته"))
        self.assertEqual(parsed_data['sentiment'], 'neutral')

    def test_parse_arabic_text_empty(self):
        """Test parsing of an empty string."""
        text = ""
        parsed_data = self.arabic_module.parse_arabic_text(text)
        self.assertEqual(parsed_data['words'], [])
        self.assertEqual(parsed_data['letters'], [])
        self.assertEqual(parsed_data['sentiment'], 'neutral')

    def test_generate_arabic_text_greeting(self):
        """Test generating a greeting message."""
        data = {'topic': 'greeting', 'name': 'علي'}
        generated_text = self.arabic_module.generate_arabic_text(data)
        self.assertEqual(generated_text, "مرحباً يا علي!")

    def test_generate_arabic_text_farewell(self):
        """Test generating a farewell message."""
        data = {'topic': 'farewell'}
        generated_text = self.arabic_module.generate_arabic_text(data)
        self.assertEqual(generated_text, "إلى اللقاء!")

    def test_generate_arabic_text_default(self):
        """Test generating a default message."""
        data = {'topic': 'unknown'}
        generated_text = self.arabic_module.generate_arabic_text(data)
        self.assertEqual(generated_text, "هذا نص تم إنشاؤه.")

    def test_generate_arabic_text_empty_data(self):
        """Test generating text with empty data."""
        data = {}
        generated_text = self.arabic_module.generate_arabic_text(data)
        self.assertEqual(generated_text, "هذا نص تم إنشاؤه.")

if __name__ == "__main__":
    # You can run the tests directly or use this block to demonstrate usage
    print("--- Demonstrating Arabic Text Module ---")

    arabic_processor = ArabicTextModule()

    # --- Parsing Example ---
    arabic_sentence = "هذه جملة عربية بسيطة للاختبار."
    print(f"\nParsing: '{arabic_sentence}'")
    parsed_result = arabic_processor.parse_arabic_text(arabic_sentence)
    print(f"Parsed Result: {parsed_result}")

    # --- Generation Example ---
    greeting_data = {'topic': 'greeting', 'name': 'فاطمة'}
    print(f"\nGenerating with data: {greeting_data}")
    generated_greeting = arabic_processor.generate_arabic_text(greeting_data)
    print(f"Generated Text: '{generated_greeting}'")

    farewell_data = {'topic': 'farewell'}
    print(f"\nGenerating with data: {farewell_data}")
    generated_farewell = arabic_processor.generate_arabic_text(farewell_data)
    print(f"Generated Text: '{generated_farewell}'")

    # --- Running Unit Tests ---
    print("\n--- Running Unit Tests ---")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)