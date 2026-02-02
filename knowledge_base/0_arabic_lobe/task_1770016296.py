import os
import json
import subprocess
from pathlib import Path

# Assume these directories and files are defined elsewhere or will be created
KNOWLEDGE_BASE_DIR = Path("./knowledge_base")
TEMPLATE_DIR = Path("./android_project_template")
BUILD_OUTPUT_DIR = Path("./build_output")
GENERATED_CODE_DIR = Path("./generated_code")

class ArabicNLPProcessor:
    """
    A sophisticated module for processing and generating Arabic text,
    focusing on understanding intent and generating structured output.
    """
    def __init__(self, knowledge_base_path: Path):
        self.knowledge_base_path = knowledge_base_path
        if not self.knowledge_base_path.exists():
            self.knowledge_base_path.mkdir(parents=True, exist_ok=True)
        self.language_data = self._load_language_data()

    def _load_language_data(self) -> dict:
        """
        Loads language-specific data (e.g., grammar rules, lexicons) from the knowledge base.
        In a real scenario, this would involve parsing complex linguistic files.
        For this example, we'll use a placeholder.
        """
        data_file = self.knowledge_base_path / "arabic_linguistic_data.json"
        if data_file.exists():
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Placeholder: In a real system, this would be more robust.
            # This could involve downloading data or initializing with basic rules.
            print(f"Warning: Language data not found at {data_file}. Using minimal placeholder.")
            return {
                "grammar": {},
                "lexicon": {},
                "intent_patterns": {}
            }

    def parse_arabic_intent(self, text: str) -> dict:
        """
        Parses natural language Arabic to identify user intent and extract relevant entities.

        Args:
            text: The Arabic input string.

        Returns:
            A dictionary representing the parsed intent, e.g.,
            {'intent': 'create_button', 'entities': {'text': 'انقر هنا', 'color': 'blue'}}
        """
        # This is a highly simplified intent parsing mechanism.
        # A real-world implementation would use advanced NLP techniques like
        # sequence labeling, dependency parsing, and custom rule-based systems.

        parsed_output = {"intent": "unknown", "entities": {}}

        # Example: Simple keyword-based intent detection
        if "زر" in text and "انقر" in text:
            parsed_output["intent"] = "create_button"
            # Extracting entities like button text and color (very basic)
            if "النص" in text:
                parts = text.split("النص")
                if len(parts) > 1:
                    entity_text = parts[1].strip().split(" ")[0]
                    parsed_output["entities"]["text"] = entity_text
            if "اللون" in text:
                parts = text.split("اللون")
                if len(parts) > 1:
                    entity_color = parts[1].strip().split(" ")[0]
                    parsed_output["entities"]["color"] = entity_color
        elif "تسمية" in text or "عنوان" in text:
            parsed_output["intent"] = "create_label"
            if "النص" in text:
                parts = text.split("النص")
                if len(parts) > 1:
                    entity_text = parts[1].strip().split(" ")[0]
                    parsed_output["entities"]["text"] = entity_text

        # In a more advanced system, you'd match patterns against self.language_data["intent_patterns"]
        # and use more sophisticated entity extraction methods.

        print(f"Parsed Arabic intent for '{text}': {parsed_output}")
        return parsed_output

    def generate_arabic_response(self, parsed_intent: dict) -> str:
        """
        Generates natural language Arabic text based on a parsed intent.

        Args:
            parsed_intent: The dictionary representing the parsed intent.

        Returns:
            A natural language Arabic string.
        """
        intent = parsed_intent.get("intent", "unknown")
        entities = parsed_intent.get("entities", {})

        if intent == "create_button":
            button_text = entities.get("text", "زر")
            response = f"سيتم إنشاء زر بالنص '{button_text}'."
            if "color" in entities:
                response += f" بلون '{entities['color']}'."
            return response
        elif intent == "create_label":
            label_text = entities.get("text", "تسمية")
            return f"سيتم إنشاء تسمية بالنص '{label_text}'."
        elif intent == "unknown":
            return "لم أفهم طلبك. هل يمكنك توضيح المزيد؟"
        else:
            return f"تم فهم القصد '{intent}' ولكن لا أعرف كيف أرد عليه."

    def generate_structured_output(self, parsed_intent: dict) -> str:
        """
        Generates a structured representation (e.g., JSON or specific DSL)
        from the parsed Arabic intent, intended for code generation.

        Args:
            parsed_intent: The dictionary representing the parsed intent.

        Returns:
            A string representing the structured output.
        """
        intent = parsed_intent.get("intent")
        entities = parsed_intent.get("entities")

        if not intent or not entities:
            return ""

        structured_data = {
            "component_type": intent,
            "attributes": entities
        }
        return json.dumps(structured_data, ensure_ascii=False, indent=2)


class ArabicLobe:
    """
    The Arabic Lobe responsible for understanding and generating Arabic language.
    This lobe acts as an intermediary between natural language input and structured code representations.
    """
    def __init__(self, knowledge_base_dir: Path):
        self.knowledge_base_dir = knowledge_base_dir
        self.nlp_processor = ArabicNLPProcessor(knowledge_base_dir)

    def process_arabic_request(self, arabic_text: str) -> dict:
        """
        Processes a given Arabic text input to extract intent and generate a structured representation.

        Args:
            arabic_text: The natural language Arabic input string.

        Returns:
            A dictionary containing the parsed intent and the structured output for code generation.
        """
        print(f"\n--- ArabicLobe processing request: '{arabic_text}' ---")
        parsed_intent = self.nlp_processor.parse_arabic_intent(arabic_text)
        generated_response = self.nlp_processor.generate_arabic_response(parsed_intent)
        structured_output = self.nlp_processor.generate_structured_output(parsed_intent)

        print(f"ArabicLobe generated response: '{generated_response}'")
        print(f"ArabicLobe generated structured output:\n{structured_output}")

        return {
            "parsed_intent": parsed_intent,
            "generated_response": generated_response,
            "structured_output": structured_output
        }

# Example Usage (for demonstration purposes, these would be called by other lobes)
if __name__ == "__main__":
    # --- Setup for demonstration ---
    DEMO_KB_DIR = Path("./demo_arabic_knowledge_base")
    DEMO_KB_DIR.mkdir(exist_ok=True)
    with open(DEMO_KB_DIR / "arabic_linguistic_data.json", "w", encoding='utf-8') as f:
        json.dump({
            "grammar": {},
            "lexicon": {},
            "intent_patterns": {
                "create_button": [
                    r"إنشاء زر بالنص (?P<text>\S+) بلون (?P<color>\S+)",
                    r"زر (?P<text>\S+) (?P<color>\S+) اللون"
                ],
                "create_label": [
                    r"إنشاء تسمية بالنص (?P<text>\S+)",
                    r"تسمية (?P<text>\S+)"
                ]
            }
        }, f, ensure_ascii=False)

    arabic_lobe = ArabicLobe(DEMO_KB_DIR)

    # --- Test Case 1: Create a button ---
    request_1 = "إنشاء زر بالنص 'اضغط هنا' بلون أزرق"
    result_1 = arabic_lobe.process_arabic_request(request_1)
    print(f"Final ArabicLobe result for '{request_1}': {result_1}")

    # --- Test Case 2: Create a label ---
    request_2 = "تسمية 'عنوان التطبيق'"
    result_2 = arabic_lobe.process_arabic_request(request_2)
    print(f"Final ArabicLobe result for '{request_2}': {result_2}")

    # --- Test Case 3: Unknown intent ---
    request_3 = "أريد أن أرى صورة قطة"
    result_3 = arabic_lobe.process_arabic_request(request_3)
    print(f"Final ArabicLobe result for '{request_3}': {result_3}")

    # --- Clean up demo files ---
    import shutil
    if DEMO_KB_DIR.exists():
        shutil.rmtree(DEMO_KB_DIR)
    print("\n--- ArabicLobe Demo Finished ---")