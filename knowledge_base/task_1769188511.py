import os
import shutil
import pytest

# Define a directory for testing
TEST_TASK_DIR = "test_arabic_parsing"

def setup_test_directory():
    """Creates a temporary directory for test files."""
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
    os.makedirs(TEST_TASK_DIR)
    print(f"Created test directory: {TEST_TASK_DIR}")

def cleanup_test_directory():
    """Removes the temporary test directory."""
    print("\nCleaning up test directory...")
    if os.path.exists(TEST_TASK_DIR):
        shutil.rmtree(TEST_TASK_DIR)
        print(f"Removed test directory: {TEST_TASK_DIR}")

def create_test_file(filename, content):
    """Creates a test file with the given content."""
    filepath = os.path.join(TEST_TASK_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created test file: {filepath}")

# --- Arabic Text Parsing Module ---

def parse_arabic_sentence(sentence: str) -> dict:
    """
    Parses an Arabic sentence, returning a dictionary with identified components.
    This is a placeholder function and needs significant development.
    """
    # Basic example: split into words. A real parser would involve:
    # - Tokenization (handling punctuation, ligatures)
    # - Morphological Analysis (stemming, root extraction, affixes)
    # - Part-of-Speech Tagging
    # - Named Entity Recognition
    # - Dependency Parsing
    words = sentence.split()
    return {"original_sentence": sentence, "words": words}

# --- Arabic Text Generation Module ---

def generate_arabic_sentence(components: dict) -> str:
    """
    Generates an Arabic sentence from given components.
    This is a placeholder function and needs significant development.
    """
    # Basic example: join words. A real generator would involve:
    # - Lexical selection
    # - Syntactic construction (handling verb conjugation, noun-adjective agreement, etc.)
    # - Pragmatic considerations
    if "words" in components:
        return " ".join(components["words"])
    elif "original_sentence" in components:
        return components["original_sentence"]
    else:
        return ""

# --- Tests ---

def test_parse_arabic_sentence_basic():
    """Tests the basic parsing functionality."""
    sentence = "مرحبا بالعالم"
    expected_output = {"original_sentence": sentence, "words": ["مرحبا", "بالعالم"]}
    assert parse_arabic_sentence(sentence) == expected_output

def test_generate_arabic_sentence_basic():
    """Tests the basic generation functionality."""
    components = {"words": ["أنا", "أحب", "العربية"]}
    expected_output = "أنا أحب العربية"
    assert generate_arabic_sentence(components) == expected_output

def test_parse_and_generate_roundtrip():
    """Tests if parsing and then generating returns the original sentence (simplified)."""
    original_sentence = "هذه جملة تجريبية"
    parsed_data = parse_arabic_sentence(original_sentence)
    # For this simple case, we expect the words to be reconstructed directly.
    # A real roundtrip test would need to handle variations.
    generated_sentence = generate_arabic_sentence({"words": parsed_data["words"]})
    assert generated_sentence == original_sentence

def test_parse_empty_string():
    """Tests parsing an empty string."""
    sentence = ""
    expected_output = {"original_sentence": sentence, "words": []}
    assert parse_arabic_sentence(sentence) == expected_output

def test_generate_empty_components():
    """Tests generating from empty components."""
    components = {}
    expected_output = ""
    assert generate_arabic_sentence(components) == expected_output

def test_parse_sentence_with_punctuation():
    """Tests parsing a sentence with basic punctuation (simplified)."""
    sentence = "كيف حالك؟"
    # Our basic splitter will include the punctuation attached to the word.
    expected_output = {"original_sentence": sentence, "words": ["كيف", "حالك؟"]}
    assert parse_arabic_sentence(sentence) == expected_output

def test_generate_sentence_with_components_dict():
    """Tests generating from a components dictionary with 'original_sentence' key."""
    components = {"original_sentence": "شكرا جزيلا"}
    expected_output = "شكرا جزيلا"
    assert generate_arabic_sentence(components) == expected_output

def test_generate_sentence_with_no_words():
    """Tests generating when 'words' key is missing but other keys might be present."""
    components = {"some_other_key": "value"}
    expected_output = ""
    assert generate_arabic_sentence(components) == expected_output

if __name__ == "__main__":
    print("--- Starting Arabic Parsing and Generation Module ---")
    setup_test_directory()

    # Example Usage
    arabic_text = "السلام عليكم ورحمة الله وبركاته"
    parsed_result = parse_arabic_sentence(arabic_text)
    print(f"\nOriginal Sentence: {arabic_text}")
    print(f"Parsed Result: {parsed_result}")

    generated_components = {"words": ["يوم", "سعيد", "إن", "شاء", "الله"]}
    generated_text = generate_arabic_sentence(generated_components)
    print(f"\nComponents for Generation: {generated_components}")
    print(f"Generated Sentence: {generated_text}")

    # Run tests if pytest is available
    try:
        print("\n--- Running Unit Tests ---")
        # This will discover and run all functions starting with 'test_'
        pytest.main([__file__])
    except ModuleNotFoundError:
        print("\nPytest not found. Skipping unit tests. Please install pytest: pip install pytest")
    except Exception as e:
        print(f"\nAn error occurred during testing: {e}")
    finally:
        cleanup_test_directory()

    print("\n--- Arabic Parsing and Generation Module Completed ---")