import os
import shutil
from typing import List, Dict, Any

# --- Constants (for demonstration purposes) ---
# In a real scenario, these would be dynamically managed or passed as arguments.
ARABIC_GRAMMAR_RULES_FILE = "arabic_grammar.json"
ARABIC_SYNTAX_TREES_DIR = "arabic_syntax_trees"
GENERATED_JAVA_CODE_DIR = "generated_java_code"
OUTPUT_APKS_DIR = "output_apks"
ANDROID_PROJECT_TEMPLATE_DIR = "android_project_template"

# --- Helper Functions (for demonstration purposes) ---

def load_arabic_grammar(filepath: str) -> Dict[str, Any]:
    """
    Loads Arabic grammar rules from a JSON file.
    In a real implementation, this would involve sophisticated NLP parsing.
    """
    print(f"INFO: Loading Arabic grammar from {filepath}")
    # Dummy grammar for demonstration
    return {
        "grammar": {
            "noun": {"singular": ["كتاب", "قلم", "طاولة"], "plural": ["كتب", "أقلام", "طاولات"]},
            "verb": {"past": ["كتب", "قرأ", "جلس"], "present": ["يكتب", "يقرأ", "يجلس"]},
            "preposition": ["في", "على", "من"],
            "determiner": ["ال"],
            "conjunction": ["و", "ف"]
        },
        "rules": [
            "determiner + noun",
            "noun + verb",
            "verb + preposition + determiner + noun"
        ]
    }

def parse_arabic_sentence(sentence: str, grammar: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parses an Arabic sentence based on provided grammar rules.
    This is a highly simplified placeholder for actual NLP parsing.
    """
    print(f"INFO: Parsing Arabic sentence: '{sentence}'")
    # In a real implementation, this would involve techniques like
    # context-free grammar parsing, dependency parsing, etc.
    # For this demo, we'll just simulate a simple tokenization and rule matching.
    tokens = sentence.split()
    parsed_structures = []

    # Very basic matching for demonstration
    if "ال" in tokens and "كتاب" in tokens and "في" in tokens:
        parsed_structures.append({
            "type": "noun_phrase",
            "head": "determiner",
            "modifier": "noun",
            "details": {"word": "الكتاب", "type": "noun"}
        })
        parsed_structures.append({
            "type": "prepositional_phrase",
            "preposition": "في",
            "noun_phrase": {
                "type": "noun_phrase",
                "head": "noun",
                "details": {"word": "المكتب", "type": "noun"}
            }
        })
    elif "كتب" in tokens and "ال" in tokens and "قلم" in tokens:
        parsed_structures.append({
            "type": "verb_phrase",
            "verb": "كتب",
            "object": {
                "type": "noun_phrase",
                "head": "determiner",
                "modifier": "noun",
                "details": {"word": "القلم", "type": "noun"}
            }
        })

    print(f"INFO: Simulated parsed structures: {parsed_structures}")
    return parsed_structures

def generate_syntax_tree_representation(parsed_data: List[Dict[str, Any]], output_dir: str):
    """
    Generates a representation of the syntax tree (e.g., saves to a file).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    tree_filename = os.path.join(output_dir, f"syntax_tree_{len(os.listdir(output_dir)) + 1}.json")
    import json
    with open(tree_filename, 'w', encoding='utf-8') as f:
        json.dump(parsed_data, f, ensure_ascii=False, indent=4)
    print(f"INFO: Generated syntax tree representation: {tree_filename}")

# --- Lobe 4: Arabic NLP and Syntax Analysis ---

class ArabicNlpLobe:
    def __init__(self, grammar_filepath: str = ARABIC_GRAMMAR_RULES_FILE,
                 syntax_trees_dir: str = ARABIC_SYNTAX_TREES_DIR):
        self.grammar = load_arabic_grammar(grammar_filepath)
        self.syntax_trees_dir = syntax_trees_dir
        os.makedirs(self.syntax_trees_dir, exist_ok=True)
        print("INFO: ArabicNlpLobe initialized.")

    def analyze_sentence(self, sentence: str) -> List[Dict[str, Any]]:
        """
        Analyzes a given Arabic sentence, producing parsed structures.
        """
        print(f"INFO: Analyzing Arabic sentence: '{sentence}'")
        parsed_data = parse_arabic_sentence(sentence, self.grammar)
        generate_syntax_tree_representation(parsed_data, self.syntax_trees_dir)
        return parsed_data

# --- Lobe 3: Code Generation (focused on Java/Android) ---

class JavaCodeGeneratorLobe:
    def __init__(self, generated_code_dir: str = GENERATED_JAVA_CODE_DIR):
        self.generated_code_dir = generated_code_dir
        os.makedirs(self.generated_code_dir, exist_ok=True)
        print("INFO: JavaCodeGeneratorLobe initialized.")

    def generate_java_code_from_syntax_tree(self, syntax_tree_data: List[Dict[str, Any]], activity_name: str = "MainActivity") -> str:
        """
        Generates Java code for an Android Activity based on the parsed Arabic syntax tree.
        This is a highly simplified mapping.
        """
        print(f"INFO: Generating Java code for activity '{activity_name}' from syntax tree data.")
        java_code_lines = [
            "package com.example.myapp;",
            "",
            "import androidx.appcompat.app.AppCompatActivity;",
            "import android.os.Bundle;",
            "import android.widget.TextView;",
            "",
            f"public class {activity_name} extends AppCompatActivity {{",
            "",
            "    @Override",
            f"    protected void onCreate(Bundle savedInstanceState) {{",
            "        super.onCreate(savedInstanceState);",
            "        setContentView(R.layout.activity_main); // Assuming a default layout",
        ]

        # Simulate generating UI elements or logic based on parsed data
        ui_element_id_counter = 0
        for item in syntax_tree_data:
            if item.get("type") == "noun_phrase" and item.get("details", {}).get("type") == "noun":
                noun_word = item["details"]["word"]
                # Example: Create a TextView for each noun identified
                java_code_lines.append(f"        TextView textView{ui_element_id_counter} = findViewById(R.id.textView_{noun_word.replace('ال', '').lower()}); // Assumes ID mapping")
                java_code_lines.append(f"        if (textView{ui_element_id_counter} != null) {{")
                java_code_lines.append(f"            textView{ui_element_id_counter}.setText(\"{noun_word}\");")
                java_code_lines.append(f"        }}")
                ui_element_id_counter += 1
            elif item.get("type") == "verb_phrase":
                verb = item.get("verb")
                java_code_lines.append(f"        // Logic related to verb: {verb}")
                # Placeholder for action triggering
                if item.get("object"):
                    obj_details = item["object"].get("details", {})
                    obj_word = obj_details.get("word", "unknown object")
                    java_code_lines.append(f"        // Action: {verb} on {obj_word}")

        java_code_lines.extend([
            "    }",
            "}",
        ])

        java_code_content = "\n".join(java_code_lines)

        # Save the generated code
        java_filename = os.path.join(self.generated_code_dir, f"{activity_name}.java")
        with open(java_filename, "w", encoding="utf-8") as f:
            f.write(java_code_content)
        print(f"INFO: Generated Java code saved to: {java_filename}")
        return java_code_content

# --- DEMO EXECUTION ---

if __name__ == "__main__":
    print("\n--- Starting Lobe 4 (Arabic NLP) and Lobe 3 (Java Code Generation) Demo ---")

    # Initialize Lobe 4
    arabic_nlp_lobe = ArabicNlpLobe()

    # Initialize Lobe 3
    code_generator_lobe = JavaCodeGeneratorLobe()

    # Example Arabic sentences
    arabic_sentences = [
        "الكتاب في المكتب",  # The book is in the office
        "كتب القلم"          # The pen wrote (simplified)
    ]

    # Process each sentence
    all_generated_code = []
    for i, sentence in enumerate(arabic_sentences):
        print(f"\n--- Processing sentence {i+1}: '{sentence}' ---")

        # Lobe 4: Analyze the Arabic sentence
        print("\n--- Executing Lobe 4: ArabicNlpLobe ---")
        parsed_syntax_tree = arabic_nlp_lobe.analyze_sentence(sentence)

        # Lobe 3: Generate Java code from the parsed data
        print("\n--- Executing Lobe 3: JavaCodeGeneratorLobe ---")
        activity_name = f"DynamicActivity{i+1}"
        generated_java = code_generator_lobe.generate_java_code_from_syntax_tree(
            parsed_syntax_tree,
            activity_name=activity_name
        )
        all_generated_code.append(generated_java)
        print(f"Generated Java code for {activity_name}:\n{generated_java[:200]}...\n") # Print snippet

    print("\n--- Lobe 4 (Arabic NLP) and Lobe 3 (Java Code Generation) Demo Finished ---")
    print(f"INFO: Generated Java code snippets are available in '{GENERATED_JAVA_CODE_DIR}'.")
    print(f"INFO: Syntax tree representations are available in '{ARABIC_SYNTAX_TREES_DIR}'.")

    # Clean up dummy directories created by this demo
    print("\n--- Cleaning up dummy directories created by this demo ---")
    if os.path.exists(ARABIC_SYNTAX_TREES_DIR):
        shutil.rmtree(ARABIC_SYNTAX_TREES_DIR)
        print(f"Removed dummy syntax trees directory: {ARABIC_SYNTAX_TREES_DIR}")
    if os.path.exists(GENERATED_JAVA_CODE_DIR):
        shutil.rmtree(GENERATED_JAVA_CODE_DIR)
        print(f"Removed dummy generated Java code directory: {GENERATED_JAVA_CODE_DIR}")
    if os.path.exists(ARABIC_GRAMMAR_RULES_FILE):
        os.remove(ARABIC_GRAMMAR_RULES_FILE)
        print(f"Removed dummy grammar file: {ARABIC_GRAMMAR_RULES_FILE}")