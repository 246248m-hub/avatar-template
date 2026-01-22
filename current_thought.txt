```python
import os
import re
from collections import defaultdict

# Define file paths and directories
VOCAB_INPUT_FILE = "arabic_vocabulary.txt"  # Assume this file exists and contains Arabic words
KNOWLEDGE_BASE_DIR = "arabic_knowledge_base"
GRAMMAR_RULES_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "grammar_rules.txt")
SYNTACTIC_RELATIONS_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "syntactic_relations.txt")
SEMANTIC_ROLES_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "semantic_roles.txt")
LEXICON_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "lexicon.txt")

def create_knowledge_base_directories():
    """Creates the necessary directories for the Arabic knowledge base."""
    os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
    print(f"Created directory: {KNOWLEDGE_BASE_DIR}")

def parse_arabic_vocabulary(input_file, knowledge_base_dir):
    """
    Parses an Arabic vocabulary file and populates the knowledge base.

    This is a simplified parser. In a real-world scenario, this would involve
    more sophisticated linguistic analysis, potentially using NLP libraries.

    Args:
        input_file (str): Path to the file containing Arabic vocabulary.
        knowledge_base_dir (str): Directory to store the parsed knowledge base.
    """
    create_knowledge_base_directories()

    # --- Dummy Knowledge Base Structures ---
    # In a real application, these would be loaded from or populated into
    # more robust data structures like databases or knowledge graphs.
    grammar_rules = defaultdict(list)
    syntactic_relations = defaultdict(list)
    semantic_roles = defaultdict(list)
    lexicon = {}

    # --- Simulate Parsing from a File ---
    print(f"Reading vocabulary from: {input_file}")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if not word:
                    continue

                # --- Simplified Linguistic Analysis (for demonstration) ---
                # In a real parser, this would involve morphology, POS tagging, etc.
                # For this example, we'll just make assumptions.

                # Assume some basic parts of speech (POS) for demonstration
                if re.search(r'[اأإيى]', word): # Very crude heuristic for potential verbs/nouns
                    pos = "NOUN" if len(word) > 3 else "VERB"
                else:
                    pos = "ADJECTIVE"

                # Assign a dummy lemma (root word)
                lemma = word # Placeholder

                # Populate lexicon
                lexicon[word] = {"lemma": lemma, "pos": pos}

                # --- Populate dummy knowledge base entries ---
                # This part is highly simplified and for illustration purposes only.
                # In a real system, these would be derived from linguistic analysis.

                if pos == "NOUN":
                    grammar_rules["noun_declension"].append(word)
                    syntactic_relations["subject"].append(word)
                    semantic_roles["agent"].append(word)
                elif pos == "VERB":
                    grammar_rules["verb_conjugation"].append(word)
                    syntactic_relations["verb"].append(word)
                    semantic_roles["action"].append(word)
                elif pos == "ADJECTIVE":
                    grammar_rules["adjective_agreement"].append(word)
                    syntactic_relations["modifier"].append(word)
                    semantic_roles["attribute"].append(word)

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return
    except Exception as e:
        print(f"An error occurred during file reading or parsing: {e}")
        return

    # --- Save Parsed Knowledge to Files ---
    # In a real system, this might involve serialization to JSON, XML, or database storage.
    save_knowledge_base_to_files(
        grammar_rules,
        syntactic_relations,
        semantic_roles,
        lexicon,
        knowledge_base_dir
    )
    print("Knowledge base populated and saved.")

def save_knowledge_base_to_files(grammar_rules, syntactic_relations, semantic_roles, lexicon, kb_dir):
    """Saves the parsed knowledge base components to individual files."""
    def write_dict_to_file(data, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            for key, values in data.items():
                f.write(f"{key}: {', '.join(values)}\n")

    def write_lexicon_to_file(data, filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            for word, info in data.items():
                f.write(f"{word}: lemma={info['lemma']}, pos={info['pos']}\n")

    write_dict_to_file(grammar_rules, os.path.join(kb_dir, "grammar_rules.txt"))
    write_dict_to_file(syntactic_relations, os.path.join(kb_dir, "syntactic_relations.txt"))
    write_dict_to_file(semantic_roles, os.path.join(kb_dir, "semantic_roles.txt"))
    write_lexicon_to_file(lexicon, os.path.join(kb_dir, "lexicon.txt"))
    print("Knowledge base files saved:")
    print(f"- {os.path.join(kb_dir, 'grammar_rules.txt')}")
    print(f"- {os.path.join(kb_dir, 'syntactic_relations.txt')}")
    print(f"- {os.path.join(kb_dir, 'semantic_roles.txt')}")
    print(f"- {os.path.join(kb_dir, 'lexicon.txt')}")


def build_arabic_language_module():
    """
    Builds the foundational Arabic language parsing and generation module.
    """
    print("--- Initializing Arabic Language Module (Phase 0) ---")

    # --- Create dummy input file if it doesn't exist ---
    if not os.path.exists(VOCAB_INPUT_FILE):
        print(f"Creating dummy input file: {VOCAB_INPUT_FILE}")
        with open(VOCAB_INPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("الكتاب\n")
            f.write("يقرأ\n")
            f.write("جميل\n")
            f.write("البيت\n")
            f.write("يكتب\n")
            f.write("كبير\n")

    # --- Execute the parser ---
    print("Starting Arabic Vocabulary Parsing...")
    parse_arabic_vocabulary(VOCAB_INPUT_FILE, KNOWLEDGE_BASE_DIR)
    print("Parsing process finished.")

    # --- Placeholder for Generation (Phase 1 and beyond) ---
    print("\n--- Arabic Generation Module (To be implemented in subsequent phases) ---")
    print("Lexicon, grammar rules, and relations are now available in the '{}' directory.".format(KNOWLEDGE_BASE_DIR))
    print("This data will be used for text generation in future phases.")
    print("--- Arabic Language Module Initialization Complete ---")


if __name__ == "__main__":
    build_arabic_language_module()
```