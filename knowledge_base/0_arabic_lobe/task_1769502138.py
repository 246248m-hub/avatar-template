import os
import shutil
import re

# Global constants (assuming these are defined elsewhere or will be defined)
KNOWLEDGE_BASE_DIR = "knowledge_base"
ARABIC_GRAMMAR_RULES_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "arabic_grammar_rules.json")
ARABIC_VOCABULARY_FILE = os.path.join(KNOWLEDGE_BASE_DIR, "arabic_vocabulary.json")
APK_OUTPUT_DIR = "apk_output"
JAVA_PROJECT_DIR = "generated_java_project"

def initialize_arabic_knowledge_base():
    """
    Initializes the Arabic grammar rules and vocabulary files if they don't exist.
    For this demo, we'll create placeholder files.
    In a real scenario, these would be populated with actual linguistic data.
    """
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        os.makedirs(KNOWLEDGE_BASE_DIR)

    if not os.path.exists(ARABIC_GRAMMAR_RULES_FILE):
        with open(ARABIC_GRAMMAR_RULES_FILE, "w", encoding="utf-8") as f:
            f.write('{"grammar": {"root": "sentence", "rules": {"sentence": [["noun_phrase", "verb_phrase"]], "noun_phrase": [["determiner", "noun"], ["noun"]], "verb_phrase": [["verb", "noun_phrase"], ["verb"]]}, "tokens": {"determiner": ["ال", "ا"], "noun": ["رجل", "بيت", "كتاب"], "verb": ["ذهب", "قرأ", "كتب"]}}}')
        print(f"Created placeholder Arabic grammar rules: {ARABIC_GRAMMAR_RULES_FILE}")

    if not os.path.exists(ARABIC_VOCABULARY_FILE):
        with open(ARABIC_VOCABULARY_FILE, "w", encoding="utf-8") as f:
            f.write('{"vocabulary": {"noun": {"رجل": "man", "بيت": "house", "كتاب": "book"}, "verb": {"ذهب": "go", "قرأ": "read", "كتب": "write"}, "determiner": {"ال": "the", "ا": "a"}}}')
        print(f"Created placeholder Arabic vocabulary: {ARABIC_VOCABULARY_FILE}")

def parse_arabic_sentence(sentence: str, grammar_rules: dict, vocabulary: dict) -> list:
    """
    A simplified placeholder for an Arabic sentence parser.
    This function aims to break down an Arabic sentence into its constituent
    grammatical parts based on provided rules.
    In a real implementation, this would involve sophisticated NLP techniques.
    """
    print(f"Attempting to parse sentence: '{sentence}'")
    parsed_structure = []
    words = sentence.split() # Basic tokenization

    # Extremely simplified parsing logic
    # This looks for direct matches of words in vocabulary and tries to apply grammar rules
    current_rule = grammar_rules["grammar"]["root"]
    temp_parsed = []
    for word in words:
        found_token_type = None
        for token_type, translations in vocabulary.items():
            if word in translations:
                found_token_type = token_type
                break

        if found_token_type:
            temp_parsed.append((word, found_token_type))
        else:
            temp_parsed.append((word, "unknown"))

    # Very basic attempt to match a simple SVO structure from grammar
    if len(temp_parsed) >= 2:
        # Assume first part is noun phrase, second is verb phrase (highly simplistic)
        noun_phrase_tokens = []
        verb_phrase_tokens = []

        # Find potential subject (noun/noun phrase)
        subject_found = False
        for i, (word, token_type) in enumerate(temp_parsed):
            if token_type in ["noun", "determiner"] and not subject_found:
                noun_phrase_tokens.append((word, token_type))
                if token_type == "noun":
                    subject_found = True
            elif subject_found and token_type in ["verb"]: # Assume verb follows noun phrase
                verb_phrase_tokens.append((word, token_type))
                break
            elif subject_found and token_type in ["noun", "determiner"] and len(verb_phrase_tokens) > 0:
                verb_phrase_tokens.append((word, token_type)) # Add object to verb phrase
            elif subject_found and token_type not in ["verb", "noun", "determiner"]:
                break # Stop if we encounter something unexpected after a subject

        if noun_phrase_tokens and verb_phrase_tokens:
            parsed_structure.append({
                "type": "sentence",
                "children": [
                    {"type": "noun_phrase", "tokens": noun_phrase_tokens},
                    {"type": "verb_phrase", "tokens": verb_phrase_tokens}
                ]
            })
    else:
        parsed_structure.append({"type": "unknown", "tokens": temp_parsed})

    print(f"Simplified parsed structure: {parsed_structure}")
    return parsed_structure

def generate_java_code_from_ast(parsed_ast: list, vocabulary: dict) -> str:
    """
    Generates a simplified Java code snippet based on a parsed Abstract Syntax Tree (AST)
    from an Arabic sentence. This is a highly conceptual placeholder.
    """
    java_code = "public class GeneratedApp {\n    public static void main(String[] args) {\n"
    if not parsed_ast:
        java_code += "        System.out.println(\"No valid structure found.\");\n"
    else:
        for element in parsed_ast:
            if element.get("type") == "sentence":
                noun_phrase = element.get("children", [{}])[0]
                verb_phrase = element.get("children", [{}])[1]

                subject_words = [token[0] for token in noun_phrase.get("tokens", [])]
                verb_words = [token[0] for token in verb_phrase.get("tokens", [])]

                subject_en = " ".join([vocabulary["vocabulary"].get(word, word) for word in subject_words])
                verb_en = " ".join([vocabulary["vocabulary"].get(word, word) for word in verb_words])

                # Simplistic translation to Java print statement
                java_code += f"        System.out.println(\"Arabic: {' '.join(subject_words)} {' '.join(verb_words)}\");\n"
                java_code += f"        System.out.println(\"Meaning: {subject_en} {verb_en}\");\n"
            else:
                java_code += f"        // Could not translate: {element}\n"

    java_code += "    }\n}\n"
    return java_code

class ArabicNLPModule:
    def __init__(self):
        self.grammar_rules = {}
        self.vocabulary = {}
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        """Loads Arabic grammar rules and vocabulary."""
        try:
            with open(ARABIC_GRAMMAR_RULES_FILE, "r", encoding="utf-8") as f:
                import json
                self.grammar_rules = json.load(f)
        except FileNotFoundError:
            print(f"Error: {ARABIC_GRAMMAR_RULES_FILE} not found. Please ensure it's initialized.")
            initialize_arabic_knowledge_base()
            with open(ARABIC_GRAMMAR_RULES_FILE, "r", encoding="utf-8") as f:
                import json
                self.grammar_rules = json.load(f)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {ARABIC_GRAMMAR_RULES_FILE}.")

        try:
            with open(ARABIC_VOCABULARY_FILE, "r", encoding="utf-8") as f:
                import json
                self.vocabulary = json.load(f)
        except FileNotFoundError:
            print(f"Error: {ARABIC_VOCABULARY_FILE} not found. Please ensure it's initialized.")
            initialize_arabic_knowledge_base()
            with open(ARABIC_VOCABULARY_FILE, "r", encoding="utf-8") as f:
                import json
                self.vocabulary = json.load(f)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {ARABIC_VOCABULARY_FILE}.")


    def process_arabic_input(self, arabic_text: str) -> dict:
        """
        Processes an Arabic text input, parses it, and prepares for code generation.
        Returns a dictionary containing the parsed structure and English translation.
        """
        if not self.grammar_rules or not self.vocabulary:
            return {"error": "Knowledge base not loaded."}

        parsed_ast = parse_arabic_sentence(arabic_text, self.grammar_rules, self.vocabulary)

        # Basic translation based on parsed structure and vocabulary
        english_translation = ""
        if parsed_ast and parsed_ast[0].get("type") == "sentence":
            subject_tokens = parsed_ast[0]["children"][0].get("tokens", [])
            verb_tokens = parsed_ast[0]["children"][1].get("tokens", [])

            subject_en_parts = []
            for word, token_type in subject_tokens:
                if token_type in self.vocabulary.get("vocabulary", {}):
                    subject_en_parts.append(self.vocabulary["vocabulary"][token_type].get(word, word))
                else:
                    subject_en_parts.append(word)
            subject_en = " ".join(subject_en_parts)

            verb_en_parts = []
            for word, token_type in verb_tokens:
                if token_type in self.vocabulary.get("vocabulary", {}):
                    verb_en_parts.append(self.vocabulary["vocabulary"][token_type].get(word, word))
                else:
                    verb_en_parts.append(word)
            verb_en = " ".join(verb_en_parts)

            english_translation = f"{subject_en} {verb_en}".strip()

        return {
            "arabic_input": arabic_text,
            "parsed_ast": parsed_ast,
            "english_translation": english_translation
        }

    def cleanup_arabic_resources(self):
        """Cleans up generated Arabic language resource files."""
        print("\n--- Cleaning up Arabic NLP Module resources ---")
        if os.path.exists(ARABIC_GRAMMAR_RULES_FILE):
            os.remove(ARABIC_GRAMMAR_RULES_FILE)
            print(f"Removed: {ARABIC_GRAMMAR_RULES_FILE}")
        if os.path.exists(ARABIC_VOCABULARY_FILE):
            os.remove(ARABIC_VOCABULARY_FILE)
            print(f"Removed: {ARABIC_VOCABULARY_FILE}")
        if os.path.exists(KNOWLEDGE_BASE_DIR) and not os.listdir(KNOWLEDGE_BASE_DIR):
            os.rmdir(KNOWLEDGE_BASE_DIR)
            print(f"Removed empty directory: {KNOWLEDGE_BASE_DIR}")

# Example usage (demonstrating the module's functionality)
if __name__ == "__main__":
    # Ensure knowledge base exists for the demo
    initialize_arabic_knowledge_base()

    arabic_nlp_module = ArabicNLPModule()

    # Test case 1: Simple sentence
    test_sentence_1 = "ذهب الرجل" # The man went
    result_1 = arabic_nlp_module.process_arabic_input(test_sentence_1)
    print("\n--- Test Case 1 ---")
    print(f"Input: {result_1['arabic_input']}")
    print(f"Parsed AST: {result_1['parsed_ast']}")
    print(f"English Translation: {result_1['english_translation']}")

    # Test case 2: Sentence with object
    test_sentence_2 = "قرأ الرجل الكتاب" # The man read the book
    result_2 = arabic_nlp_module.process_arabic_input(test_sentence_2)
    print("\n--- Test Case 2 ---")
    print(f"Input: {result_2['arabic_input']}")
    print(f"Parsed AST: {result_2['parsed_ast']}")
    print(f"English Translation: {result_2['english_translation']}")

    # Generate dummy Java code from the parsed AST
    dummy_java_code_1 = generate_java_code_from_ast(result_1.get("parsed_ast", []), arabic_nlp_module.vocabulary)
    print("\n--- Generated Java Code (from Test Case 1) ---")
    print(dummy_java_code_1)

    dummy_java_code_2 = generate_java_code_from_ast(result_2.get("parsed_ast", []), arabic_nlp_module.vocabulary)
    print("\n--- Generated Java Code (from Test Case 2) ---")
    print(dummy_java_code_2)

    # Simulate APK compilation step (cleanup for this module's generated files)
    # In a real flow, this would be called by Lobe 8_apk_compiler_lobe
    arabic_nlp_module.cleanup_arabic_resources()