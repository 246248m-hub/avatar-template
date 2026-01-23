import os
import shutil
import pytest

TEST_TASK_DIR = "arabic_parsing_generation_test"

class ArabicParsingGeneration:
    def __init__(self):
        self.arabic_data_dir = os.path.join(TEST_TASK_DIR, "arabic_data")
        os.makedirs(self.arabic_data_dir, exist_ok=True)

    def _get_arabic_file_path(self, filename):
        return os.path.join(self.arabic_data_dir, filename)

    def parse_arabic_text(self, text):
        """
        Parses Arabic text. In this foundational phase, it might involve:
        - Basic tokenization (splitting by spaces, punctuation).
        - Identifying common diacritics (harakat).
        - Simple character-level analysis.

        Args:
            text (str): The Arabic text to parse.

        Returns:
            dict: A dictionary containing parsed information.
        """
        tokens = text.split()
        parsed_info = {
            "original_text": text,
            "tokens": tokens,
            "character_count": len(text),
            "word_count": len(tokens),
            "has_diacritics": any('\u064B' <= char <= '\u0652' for char in text)
        }
        return parsed_info

    def generate_arabic_text(self, parsed_data):
        """
        Generates Arabic text from parsed data. In this foundational phase,
        it might involve reconstructing text from tokens.

        Args:
            parsed_data (dict): A dictionary containing parsed information,
                                expected to have at least a 'tokens' key.

        Returns:
            str: The generated Arabic text.
        """
        if "tokens" in parsed_data and isinstance(parsed_data["tokens"], list):
            return " ".join(parsed_data["tokens"])
        return ""

    def save_arabic_text(self, filename, text):
        """
        Saves Arabic text to a file.

        Args:
            filename (str): The name of the file to save.
            text (str): The Arabic text to save.
        """
        file_path = self._get_arabic_file_path(filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved Arabic text to: {file_path}")

    def load_arabic_text(self, filename):
        """
        Loads Arabic text from a file.

        Args:
            filename (str): The name of the file to load.

        Returns:
            str: The loaded Arabic text.
        """
        file_path = self._get_arabic_file_path(filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def list_saved_arabic_files(self):
        """
        Lists all saved Arabic text files in the data directory.

        Returns:
            list: A list of filenames.
        """
        return [f for f in os.listdir(self.arabic_data_dir) if os.path.isfile(os.path.join(self.arabic_data_dir, f))]


# --- Test Cases ---

def test_parse_arabic_text():
    parser = ArabicParsingGeneration()
    text = "السلام عليكم ورحمة الله وبركاته"
    parsed = parser.parse_arabic_text(text)
    assert isinstance(parsed, dict)
    assert parsed["original_text"] == text
    assert parsed["tokens"] == ["السلام", "عليكم", "ورحمة", "الله", "وبركاته"]
    assert parsed["character_count"] == len(text)
    assert parsed["word_count"] == 5
    assert not parsed["has_diacritics"]

    text_with_diacritics = "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللَّهِ وَبَرَكَاتُهُ"
    parsed_with_diacritics = parser.parse_arabic_text(text_with_diacritics)
    assert parsed_with_diacritics["has_diacritics"]

def test_generate_arabic_text():
    parser = ArabicParsingGeneration()
    parsed_data = {
        "tokens": ["هذا", "مثال", "للإنشاء"]
    }
    generated_text = parser.generate_arabic_text(parsed_data)
    assert generated_text == "هذا مثال للإنشاء"

    parsed_data_empty_tokens = {"tokens": []}
    generated_text_empty = parser.generate_arabic_text(parsed_data_empty_tokens)
    assert generated_text_empty == ""

    parsed_data_no_tokens = {"other_key": "value"}
    generated_text_no_tokens = parser.generate_arabic_text(parsed_data_no_tokens)
    assert generated_text_no_tokens == ""

def test_save_and_load_arabic_text():
    parser = ArabicParsingGeneration()
    test_filename = "example.txt"
    arabic_content = "مرحباً بالعالم!"

    parser.save_arabic_text(test_filename, arabic_content)
    assert test_filename in parser.list_saved_arabic_files()

    loaded_content = parser.load_arabic_text(test_filename)
    assert loaded_content == arabic_content

    with pytest.raises(FileNotFoundError):
        parser.load_arabic_text("non_existent_file.txt")

def test_list_saved_arabic_files():
    parser = ArabicParsingGeneration()
    file1 = "file1.txt"
    file2 = "file2.txt"

    parser.save_arabic_text(file1, "content1")
    parser.save_arabic_text(file2, "content2")

    saved_files = parser.list_saved_arabic_files()
    assert file1 in saved_files
    assert file2 in saved_files
    assert len(saved_files) >= 2 # Accounts for potential other files if run multiple times

def test_integration_parse_generate():
    parser = ArabicParsingGeneration()
    original_text = "تجربة بسيطة"
    parsed_data = parser.parse_arabic_text(original_text)
    generated_text = parser.generate_arabic_text(parsed_data)
    assert generated_text == "تجربة بسيطة"


# --- Main Execution and Cleanup ---
if __name__ == "__main__":
    # Ensure the test directory is clean before running tests
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
        print(f"Cleaned up existing test directory: {TEST_TASK_DIR}")

    # Create the test directory and data subdirectory
    os.makedirs(os.path.join(TEST_TASK_DIR, "arabic_data"), exist_ok=True)

    print("Running tests for Arabic Parsing and Generation Module...")

    # Run individual tests
    test_parse_arabic_text()
    test_generate_arabic_text()
    test_save_and_load_arabic_text()
    test_list_saved_arabic_files()
    test_integration_parse_generate()

    # You can also use pytest to discover and run tests if you have it installed
    # import subprocess
    # print("\nRunning tests using pytest...")
    # subprocess.run(["pytest", __file__])

    # --- Cleanup ---
    print("\nCleaning up test directory...")
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
        print(f"Removed test directory: {TEST_TASK_DIR}")

    print("\n--- All Test Cases Completed ---")