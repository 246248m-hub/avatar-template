import os
import re
import json
import shutil

# --- Constants ---
ARABIC_GRAMMAR_RULES_FILE = "arabic_grammar_rules.json"
DEFAULT_ARABIC_GRAMMAR_RULES = {
    "syntax": {
        "statement": "<noun_phrase> <verb_phrase>",
        "noun_phrase": "<determiner>? <adjective>* <noun>",
        "verb_phrase": "<verb> <noun_phrase>|<verb> <adverb>",
        "determiner": "ال",
        "adjective": "",  # Placeholder for more complex adjective rules
        "noun": "",       # Placeholder for actual nouns
        "verb": "",       # Placeholder for actual verbs
        "adverb": ""      # Placeholder for actual adverbs
    },
    "vocabulary": {
        "nouns": ["تطبيق", "برنامج", "واجهة", "زر", "نص"],
        "verbs": ["إنشاء", "بناء", "عرض", "تغيير", "إنشاء_واجهة"],
        "adjectives": ["جديد", "بسيط", "فعال"],
        "adverbs": ["بسرعة", "بسلاسة"]
    }
}

# --- Helper Functions ---
def load_grammar_rules(filepath=ARABIC_GRAMMAR_RULES_FILE):
    """Loads Arabic grammar rules from a JSON file."""
    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_ARABIC_GRAMMAR_RULES, f, ensure_ascii=False, indent=4)
        return DEFAULT_ARABIC_GRAMMAR_RULES
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_random_word(word_type, grammar_rules):
    """Gets a random word of a specified type from the grammar rules."""
    words = grammar_rules["vocabulary"].get(word_type, [])
    if not words:
        return ""
    import random
    return random.choice(words)

def generate_phrase(phrase_type, grammar_rules):
    """Recursively generates a phrase based on grammar rules."""
    rule = grammar_rules["syntax"].get(phrase_type)
    if not rule:
        return ""

    parts = rule.split('|')
    chosen_rule = random.choice(parts)

    generated = ""
    for token in chosen_rule.split():
        if token.endswith('?'):  # Optional
            if random.random() > 0.5:
                generated += generate_phrase(token[:-1], grammar_rules) + " "
        elif token.endswith('*'): # Zero or more
            num_items = random.randint(0, 2)
            for _ in range(num_items):
                generated += generate_phrase(token[:-1], grammar_rules) + " "
        elif token in grammar_rules["syntax"]:
            generated += generate_phrase(token, grammar_rules) + " "
        elif token in grammar_rules["vocabulary"]:
            generated += get_random_word(token, grammar_rules) + " "
        else:
            generated += token + " " # Treat as literal

    return generated.strip()

# --- Arabic Logic Module ---
class ArabicLogicLobe:
    def __init__(self, grammar_rules_path=ARABIC_GRAMMAR_RULES_FILE):
        self.grammar_rules = load_grammar_rules(grammar_rules_path)
        self.generated_arabic_code = {}

    def parse_nlp_request(self, natural_language_request: str) -> dict:
        """
        Parses a natural language Arabic request into structured data for APK generation.
        This is a simplified parser. Real-world would involve more complex NLP.
        """
        # Basic keyword matching for demonstration
        parsed_data = {"components": [], "actions": []}

        if "إنشاء واجهة" in natural_language_request or "بناء تطبيق" in natural_language_request:
            parsed_data["intent"] = "create_app_ui"
            if "زر" in natural_language_request:
                parsed_data["components"].append({"type": "button", "label": "Click Me"})
            if "نص" in natural_language_request:
                parsed_data["components"].append({"type": "text_view", "text": "Hello, World!"})
            if "شاشة" in natural_language_request:
                parsed_data["components"].append({"type": "screen", "name": "main_screen"})

        elif "تغيير النص" in natural_language_request:
            parsed_data["intent"] = "change_text"
            match = re.search(r"تغيير النص إلى (.*)", natural_language_request)
            if match:
                parsed_data["new_text"] = match.group(1).strip()

        return parsed_data

    def generate_arabic_code_structure(self, parsed_data: dict) -> dict:
        """
        Generates a Python-like code structure (represented as strings)
        from the parsed NLP data, using Arabic-inspired naming conventions.
        This is a symbolic representation, not executable Python for the APK itself.
        """
        generated_structure = {}
        components_code = []
        actions_code = []

        if parsed_data.get("intent") == "create_app_ui":
            screen_name = "MainScreen"
            generated_structure["screen_name"] = screen_name
            generated_structure["imports"] = ["import android.os.Bundle", "import androidx.activity.ComponentActivity", "import androidx.activity.compose.setContent", "import androidx.compose.material3.Text", "import androidx.compose.runtime.Composable", "import androidx.compose.ui.tooling.preview.Preview"]

            # Generate UI components based on parsed data
            for component in parsed_data.get("components", []):
                if component["type"] == "screen":
                    screen_name = component.get("name", "MainScreen").replace(" ", "_").capitalize()
                    generated_structure["screen_name"] = screen_name
                elif component["type"] == "button":
                    button_label = component.get("label", "زر")
                    components_code.append(f'    Button(onClick = {{ /* Add action here */ }}) {{ Text("{button_label}") }}')
                elif component["type"] == "text_view":
                    text_content = component.get("text", "نص افتراضي")
                    components_code.append(f'    Text(text = "{text_content}")')

            # Combine components into a Composable function
            composable_body = "\n".join(components_code)
            generated_structure["ui_composable"] = f"""
@Composable
fun {screen_name}() {{
    // UI elements will be placed here based on parsed components
{composable_body}
}}
"""
            generated_structure["main_activity"] = f"""
class MainActivity : ComponentActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContent {{
            // Your App Theme
            {screen_name}()
        }}
    }}
}}
"""
        elif parsed_data.get("intent") == "change_text":
            if "new_text" in parsed_data:
                actions_code.append(f"// Action: Change text to '{parsed_data['new_text']}'")
                # In a real scenario, this would involve state management and UI updates

        generated_structure["actions"] = "\n".join(actions_code)
        self.generated_arabic_code = generated_structure
        return generated_structure

    def generate_arabic_sentence_from_rules(self, num_sentences=1):
        """Generates Arabic sentences based on defined grammar rules."""
        generated_sentences = []
        for _ in range(num_sentences):
            sentence = generate_phrase("statement", self.grammar_rules)
            generated_sentences.append(sentence)
        return generated_sentences

    def get_generated_code(self):
        """Returns the last generated symbolic code structure."""
        return self.generated_arabic_code

# --- Demo Usage ---
if __name__ == "__main__":
    print("--- Initiating Arabic Logic Lobe ---")

    # Initialize the lobe
    arabic_logic_lobe = ArabicLogicLobe()

    # --- Demo 1: Parsing and Code Generation ---
    print("\n--- Demo 1: Parsing NLP Request ---")
    test_prompt_1 = "إنشاء تطبيق بسيط بواجهة تحتوي على زر ونص."
    parsed_data_1 = arabic_logic_lobe.parse_nlp_request(test_prompt_1)
    print(f"NLP Request: '{test_prompt_1}'")
    print(f"Parsed Data: {json.dumps(parsed_data_1, indent=2, ensure_ascii=False)}")

    generated_code_1 = arabic_logic_lobe.generate_arabic_code_structure(parsed_data_1)
    print("\nGenerated Symbolic Code Structure:")
    for key, value in generated_code_1.items():
        if isinstance(value, str):
            print(f"--- {key} ---")
            print(value)
        else:
            print(f"{key}: {value}")

    # --- Demo 2: Generating Arabic Sentences ---
    print("\n--- Demo 2: Generating Arabic Sentences from Grammar Rules ---")
    generated_sentences = arabic_logic_lobe.generate_arabic_sentence_from_rules(num_sentences=2)
    print("Generated Arabic Sentences:")
    for sentence in generated_sentences:
        print(f"- {sentence}")

    # --- Demo 3: More Complex Request ---
    print("\n--- Demo 3: Parsing another NLP Request ---")
    test_prompt_2 = "بناء برنامج يعرض رسالة ترحيب."
    parsed_data_2 = arabic_logic_lobe.parse_nlp_request(test_prompt_2)
    print(f"NLP Request: '{test_prompt_2}'")
    print(f"Parsed Data: {json.dumps(parsed_data_2, indent=2, ensure_ascii=False)}")

    generated_code_2 = arabic_logic_lobe.generate_arabic_code_structure(parsed_data_2)
    print("\nGenerated Symbolic Code Structure:")
    for key, value in generated_code_2.items():
        if isinstance(value, str):
            print(f"--- {key} ---")
            print(value)
        else:
            print(f"{key}: {value}")

    print("\n--- Arabic Logic Lobe Demo Finished ---")

    # --- Placeholder for next logical step ---
    print("\n--- Initiating next step: Lobe 4_code_generation_lobe ---")