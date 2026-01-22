```python
# -*- coding: utf-8 -*-

import os
import json
from collections import defaultdict

# --- Configuration ---
VOCAB_INPUT_FILE = "arabic_vocabulary.txt"  # Path to the input vocabulary file
KNOWLEDGE_BASE_DIR = "arabic_kb"  # Directory for the knowledge base

# --- Data Structures ---
arabic_lexicon = {}  # Stores word forms and their properties
arabic_morphology = defaultdict(list)  # Stores root-to-word mappings
arabic_semantics = defaultdict(list)  # Stores root-to-meaning mappings

# --- Helper Functions ---

def create_knowledge_base_dir():
    """Creates the directory for the knowledge base if it doesn't exist."""
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        os.makedirs(KNOWLEDGE_BASE_DIR)
        print(f"Created knowledge base directory: {KNOWLEDGE_BASE_DIR}")

def save_knowledge_base():
    """Saves the parsed Arabic knowledge base to files."""
    with open(os.path.join(KNOWLEDGE_BASE_DIR, "lexicon.json"), "w", encoding="utf-8") as f:
        json.dump(arabic_lexicon, f, ensure_ascii=False, indent=4)
    with open(os.path.join(KNOWLEDGE_BASE_DIR, "morphology.json"), "w", encoding="utf-8") as f:
        json.dump(arabic_morphology, f, ensure_ascii=False, indent=4)
    with open(os.path.join(KNOWLEDGE_BASE_DIR, "semantics.json"), "w", encoding="utf-8") as f:
        json.dump(arabic_semantics, f, ensure_ascii=False, indent=4)
    print(f"Knowledge base saved to {KNOWLEDGE_BASE_DIR}")

def parse_arabic_vocabulary(input_file_path, kb_dir):
    """
    Parses the Arabic vocabulary file and populates the knowledge base.

    The input file is expected to have lines in the format:
    word_form | root | part_of_speech | meaning
    """
    create_knowledge_base_dir()

    print(f"Reading vocabulary from: {input_file_path}")
    try:
        with open(input_file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith('#'):  # Skip empty lines and comments
                    continue

                parts = line.split('|')
                if len(parts) != 4:
                    print(f"Warning: Skipping malformed line {line_num}: {line}. Expected format: word_form | root | part_of_speech | meaning")
                    continue

                word_form, root, part_of_speech, meaning = [p.strip() for p in parts]

                # Populate lexicon
                arabic_lexicon[word_form] = {
                    "root": root,
                    "pos": part_of_speech,
                    "meaning": meaning
                }

                # Populate morphology
                arabic_morphology[root].append({
                    "word_form": word_form,
                    "pos": part_of_speech
                })

                # Populate semantics
                arabic_semantics[root].append(meaning)

        print(f"Successfully parsed {len(arabic_lexicon)} vocabulary entries.")
        save_knowledge_base()

    except FileNotFoundError:
        print(f"Error: Input vocabulary file not found at {input_file_path}")
        # As a fallback, create an empty knowledge base if the input file is missing
        save_knowledge_base()
    except Exception as e:
        print(f"An unexpected error occurred during parsing: {e}")
        # Attempt to save what has been parsed so far, or an empty KB if nothing was parsed
        save_knowledge_base()

# --- Main Initialization Function ---

def initialize_arabic_language_module():
    """Initializes the Arabic language module by parsing the vocabulary."""
    print("--- Initializing Arabic Language Module ---")
    print("PHASE 0: Master Language.")

    # Create dummy input file if it doesn't exist, for demonstration
    if not os.path.exists(VOCAB_INPUT_FILE):
        print(f"'{VOCAB_INPUT_FILE}' not found. Creating a dummy file for demonstration.")
        with open(VOCAB_INPUT_FILE, "w", encoding="utf-8") as f:
            f.write("# Example Arabic vocabulary\n")
            f.write("كتاب | كتب | NOUN | book\n")
            f.write("يكتب | كتب | VERB | writes\n")
            f.write("مكتبة | كتب | NOUN | library\n")
            f.write("جميل | جمل | ADJ | beautiful\n")
            f.write("يجمّل | جمل | VERB | beautifies\n")

    # --- Execute the parser ---
    print("Starting Arabic Vocabulary Parsing...")
    parse_arabic_vocabulary(VOCAB_INPUT_FILE, KNOWLEDGE_BASE_DIR)
    print("Parsing process finished.")
    print("// STM from 0_language_lobe: Arabic vocabulary parsing complete. Knowledge base ready.")
    print("--- Arabic Language Module Initialization Complete ---")


if __name__ == "__main__":
    initialize_arabic_language_module()
```