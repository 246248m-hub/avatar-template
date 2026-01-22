# knowledge_base/0_arabic_lobe/arabic_parser.py

import os
import json

def parse_arabic_vocabulary(input_filepath: str, output_dir: str):
    """
    Parses a large Arabic vocabulary file and stores it in a structured format
    within the specified output directory.

    The expected input file format is a simple list of Arabic words, one per line.
    The output will be a JSON file containing a list of these words.

    Args:
        input_filepath (str): The path to the input Arabic vocabulary file.
        output_dir (str): The directory where the parsed vocabulary will be saved.
    """

    arabic_words = []
    try:
        with open(input_filepath, 'r', encoding='utf-8') as infile:
            for line in infile:
                word = line.strip()
                if word:  # Ensure the line is not empty
                    arabic_words.append(word)
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_filepath}")
        return
    except Exception as e:
        print(f"An error occurred while reading the input file: {e}")
        return

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    output_filepath = os.path.join(output_dir, 'arabic_vocabulary.json')

    try:
        with open(output_filepath, 'w', encoding='utf-8') as outfile:
            json.dump(arabic_words, outfile, ensure_ascii=False, indent=4)
        print(f"Successfully parsed {len(arabic_words)} Arabic words.")
        print(f"Vocabulary saved to {output_filepath}")
    except Exception as e:
        print(f"An error occurred while writing the output file: {e}")

if __name__ == "__main__":
    # --- Configuration ---
    # This should be the path to your large Arabic vocabulary file.
    # For demonstration purposes, let's assume it's named 'arabic_vocab.txt'
    # and is located in the same directory as this script.
    # You'll need to create this file with some Arabic words.
    VOCAB_INPUT_FILE = 'arabic_vocab.txt'

    # This is the target directory for storing the parsed vocabulary.
    KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'knowledge_base', '0_arabic_lobe')

    # --- Create a dummy input file for testing if it doesn't exist ---
    if not os.path.exists(VOCAB_INPUT_FILE):
        print(f"'{VOCAB_INPUT_FILE}' not found. Creating a dummy file for demonstration.")
        dummy_content = [
            "مرحبا",
            "العالم",
            "اللغة",
            "العربية",
            "برمجة",
            "بيت",
            "كتاب",
            "شمس",
            "قمر",
            "سماء"
        ]
        try:
            with open(VOCAB_INPUT_FILE, 'w', encoding='utf-8') as f:
                for word in dummy_content:
                    f.write(word + '\n')
            print(f"Dummy '{VOCAB_INPUT_FILE}' created successfully.")
        except Exception as e:
            print(f"Error creating dummy file: {e}")

    # --- Execute the parser ---
    print("Starting Arabic Vocabulary Parsing...")
    parse_arabic_vocabulary(VOCAB_INPUT_FILE, KNOWLEDGE_BASE_DIR)
    print("Parsing process finished.")