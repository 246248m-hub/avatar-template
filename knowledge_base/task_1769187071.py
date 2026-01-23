import re
import os
import shutil
import pytest

# Define a directory for test files
TEST_TASK_DIR = "test_arabic_parser_generator"

def normalize_arabic(text):
    """Normalizes Arabic text by removing diacritics, Tatweel, and Hamza variations."""
    text = re.sub(r'[\u064B-\u0652]', '', text)  # Remove diacritics
    text = re.sub(r'\u0650', '', text) # Remove Kasra
    text = re.sub(r'\u064C', '', text) # Remove Fathatan
    text = re.sub(r'\u064D', '', text) # Remove Dammatan
    text = re.sub(r'\u064E', '', text) # Remove Fatha
    text = re.sub(r'\u064F', '', text) # Remove Damma
    text = re.sub(r'\u0651', '', text) # Remove Shadda
    text = re.sub(r'\u0652', '', text) # Remove Sukun
    text = re.sub(r'\u0670', '', text) # Remove Alef maksura
    text = re.sub(r'\u0621', 'ء', text)  # Normalize Hamzat Wasl to Hamza
    text = re.sub(r'\u0623', 'أ', text)  # Normalize Hamzat Alif to Alif with Hamza above
    text = re.sub(r'\u0624', 'ؤ', text)  # Normalize Waw with Hamza to Waw with Hamza above
    text = re.sub(r'\u0625', 'إ', text)  # Normalize Alif with Hamza below to Alif with Hamza below
    text = re.sub(r'\u0626', 'ئ', text)  # Normalize Ya with Hamza to Ya with Hamza above
    text = re.sub(r'\u0622', 'آ', text)  # Normalize Alif Maddah to Alif Maddah
    text = re.sub(r'\u0627', 'ا', text)  # Normalize Alif to Alif
    text = re.sub(r'\u0640', '', text)  # Remove Tatweel (Kashida)
    text = re.sub(r'\u0649', 'ي', text)  # Normalize Alif Maqsura to Ya
    text = re.sub(r'\u064A', 'ي', text)  # Normalize Ya to Ya
    text = re.sub(r'\u0648', 'و', text)  # Normalize Waw to Waw
    text = re.sub(r'\u0647', 'ه', text)  # Normalize Ha to Ha
    text = re.sub(r'\u0629', 'ة', text)  # Normalize Taa Marbuta to Taa Marbuta

    # Handle common ligatures or variations if needed, e.g. Lam-Alef
    text = re.sub(r'ﻻ', 'لا', text)
    text = re.sub(r'ـ', '', text) # Generic connector removal

    return text

def parse_arabic_sentence(sentence):
    """
    Parses an Arabic sentence into its constituent words.
    This is a basic parser; more advanced parsing would involve POS tagging, dependency parsing, etc.
    """
    if not isinstance(sentence, str):
        raise TypeError("Input must be a string.")

    normalized_sentence = normalize_arabic(sentence)
    # Split by whitespace. This is a very basic approach.
    words = normalized_sentence.split()
    return [word for word in words if word] # Filter out empty strings


def generate_arabic_text(words):
    """
    Generates Arabic text from a list of words.
    This is a basic generator; more advanced generation would involve grammar and context.
    """
    if not isinstance(words, list) or not all(isinstance(word, str) for word in words):
        raise TypeError("Input must be a list of strings.")

    # Simple concatenation with spaces.
    return " ".join(words)

# --- Test Cases ---

def setup_module(module):
    """Set up test directory."""
    os.makedirs(TEST_TASK_DIR, exist_ok=True)
    print(f"\nCreated test directory: {TEST_TASK_DIR}")

def teardown_module(module):
    """Clean up test directory."""
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
        print(f"Removed test directory: {TEST_TASK_DIR}")

def test_normalize_arabic_basic():
    """Test basic normalization with diacritics."""
    text_with_diacritics = "بِسْمِ ٱللَّٰهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"
    expected_text = "بسم الله الرحمن الرحيم"
    assert normalize_arabic(text_with_diacritics) == expected_text

def test_normalize_arabic_tatweel():
    """Test normalization with Tatweel."""
    text_with_tatweel = "مــرحــبــا"
    expected_text = "مرحبا"
    assert normalize_arabic(text_with_tatweel) == expected_text

def test_normalize_arabic_hamza_variations():
    """Test normalization of Hamza variations."""
    text_with_hamzas = "أَإِؤُئِآء"
    expected_text = "آآآآآآ" # Assuming standard normalization to Alif Maddah or similar for illustrative purposes
    assert normalize_arabic(text_with_hamzas) == expected_text

def test_normalize_arabic_mixed():
    """Test normalization with a mix of features."""
    mixed_text = "اَلْحَمْدُ لِلَّٰهِ رَبِّ ٱلْعَٰلَمِينَ"
    expected_text = "الحمد لله رب العالمين"
    assert normalize_arabic(mixed_text) == expected_text

def test_parse_arabic_sentence_basic():
    """Test basic sentence parsing."""
    sentence = "السلام عليكم ورحمة الله وبركاته"
    expected_words = ["السلام", "عليكم", "رحمة", "الله", "وبركاته"]
    assert parse_arabic_sentence(sentence) == expected_words

def test_parse_arabic_sentence_with_diacritics():
    """Test parsing a sentence with diacritics."""
    sentence = "ٱلسَّلَامُ عَلَيْكُمْ وَرَحْمَةُ ٱللَّٰهِ وَبَرَكَاتُهُ"
    expected_words = ["السلام", "عليكم", "رحمة", "الله", "وبركاته"]
    assert parse_arabic_sentence(sentence) == expected_words

def test_parse_arabic_sentence_with_tatweel():
    """Test parsing a sentence with Tatweel."""
    sentence = "مــرحــبــا بــك"
    expected_words = ["مرحبا", "بك"]
    assert parse_arabic_sentence(sentence) == expected_words

def test_parse_arabic_sentence_empty_input():
    """Test parsing an empty string."""
    assert parse_arabic_sentence("") == []

def test_parse_arabic_sentence_whitespace_only():
    """Test parsing a string with only whitespace."""
    assert parse_arabic_sentence("   \t  \n ") == []

def test_parse_arabic_sentence_invalid_input_type():
    """Test parsing with invalid input type."""
    with pytest.raises(TypeError):
        parse_arabic_sentence(123)
    with pytest.raises(TypeError):
        parse_arabic_sentence(None)

def test_generate_arabic_text_basic():
    """Test basic text generation."""
    words = ["اهلا", "بك", "يا", "صديقي"]
    expected_text = "اهلا بك يا صديقي"
    assert generate_arabic_text(words) == expected_text

def test_generate_arabic_text_empty_list():
    """Test text generation with an empty list."""
    assert generate_arabic_text([]) == ""

def test_generate_arabic_text_single_word():
    """Test text generation with a single word."""
    words = ["الله"]
    expected_text = "الله"
    assert generate_arabic_text(words) == expected_text

def test_generate_arabic_text_invalid_input_type_list():
    """Test text generation with invalid input type for list."""
    with pytest.raises(TypeError):
        generate_arabic_text("not a list")
    with pytest.raises(TypeError):
        generate_arabic_text(None)

def test_generate_arabic_text_invalid_input_type_elements():
    """Test text generation with invalid input type for list elements."""
    with pytest.raises(TypeError):
        generate_arabic_text(["hello", 123, "world"])
    with pytest.raises(TypeError):
        generate_arabic_text(["hello", None, "world"])

def test_parse_and_generate_roundtrip():
    """Test a roundtrip of parsing and then generating."""
    original_sentence = "اللغة العربية جميلة جداً."
    parsed_words = parse_arabic_sentence(original_sentence)
    generated_sentence = generate_arabic_text(parsed_words)
    # Note: Normalization might alter the exact string, so we compare normalized versions if necessary.
    # For this basic implementation, the output of generate_arabic_text should match the normalized input.
    assert normalize_arabic(generated_sentence) == normalize_arabic(original_sentence).split()
    # Let's re-evaluate this assertion based on current implementation.
    # The parse function normalizes, and generate joins with spaces.
    # So generated_sentence should be the normalized string components joined.
    expected_generated = " ".join(normalize_arabic(original_sentence).split())
    assert generated_sentence == expected_generated

# --- Main execution block for demonstration ---
if __name__ == "__main__":
    print("Running Arabic Text Parsing and Generation Module Tests...")

    # Create test directory if it doesn't exist for manual runs
    os.makedirs(TEST_TASK_DIR, exist_ok=True)

    # Example Usage:
    print("\n--- Example Usage ---")
    sample_text = "بِسْمِ ٱللَّٰهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ، اَلْحَمْدُ لِلَّٰهِ رَبِّ ٱلْعَٰلَمِينَ."
    print(f"Original Text: {sample_text}")

    normalized_text = normalize_arabic(sample_text)
    print(f"Normalized Text: {normalized_text}")

    parsed_words = parse_arabic_sentence(sample_text)
    print(f"Parsed Words: {parsed_words}")

    generated_text = generate_arabic_text(parsed_words)
    print(f"Generated Text: {generated_text}")

    # Running pytest programmatically (optional, as pytest is typically run from the command line)
    # This part will actually run the tests defined above.
    print("\n--- Running Pytest ---")
    # Collect all functions starting with 'test_' in this module
    test_functions = [obj for name, obj in locals().items() if callable(obj) and name.startswith('test_')]

    # Temporarily create a dummy test file for pytest to discover
    # This is a workaround if pytest runner is not directly invoked.
    # In a real scenario, you'd run 'pytest your_module_name.py' from the terminal.
    test_file_path = os.path.join(TEST_TASK_DIR, "test_arabic_module.py")
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write("import pytest\n")
        f.write("from __main__ import normalize_arabic, parse_arabic_sentence, generate_arabic_text\n") # Adjust import if needed
        for func in test_functions:
            # Write the function definition to the test file
            import inspect
            f.write(inspect.getsource(func))
            f.write("\n\n") # Add space between function definitions

    print(f"Created temporary test file: {test_file_path}")

    # Execute pytest
    try:
        # Passing the directory to pytest.main() makes it discover tests within that directory.
        # The '-v' flag increases verbosity.
        exit_code = pytest.main(["-v", TEST_TASK_DIR])
        if exit_code == 0:
            print("\nAll tests passed successfully!")
        else:
            print(f"\nSome tests failed. Pytest exit code: {exit_code}")
    except Exception as e:
        print(f"\nAn error occurred during pytest execution: {e}")


    # --- Cleanup ---
    print("\nCleaning up test directory...")
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
        print(f"Removed test directory: {TEST_TASK_DIR}")

    print("\n--- All Test Cases Completed ---")