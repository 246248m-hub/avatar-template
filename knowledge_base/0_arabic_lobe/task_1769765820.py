import os
import json
from typing import Dict, List, Any

class ArabicNlpProcessor:
    """
    A module designed to process Arabic natural language, extract intent,
    and map it to structured data for APK generation.
    """
    def __init__(self, knowledge_base_dir: str = "arabic_nlp_kb"):
        """
        Initializes the ArabicNlpProcessor.

        Args:
            knowledge_base_dir (str): The directory to store and load
                                      Arabic NLP knowledge base.
        """
        self.knowledge_base_dir = knowledge_base_dir
        os.makedirs(self.knowledge_base_dir, exist_ok=True)
        self.intent_mappings = self._load_intent_mappings()
        self.entity_regex_patterns = self._load_entity_regex()

    def _get_kb_path(self, filename: str) -> str:
        """Constructs the full path to a knowledge base file."""
        return os.path.join(self.knowledge_base_dir, filename)

    def _load_intent_mappings(self) -> Dict[str, Dict[str, Any]]:
        """
        Loads intent-to-action mappings from a JSON file.
        The structure is expected to be:
        {
            "intent_name": {
                "patterns": ["example phrase 1", "example phrase 2"],
                "entities": ["entity_type_1", "entity_type_2"],
                "action_template": "some_action_template_{entity_type_1}"
            }
        }
        """
        filepath = self._get_kb_path("intent_mappings.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Initialize with some basic examples if file doesn't exist
            default_mappings = {
                "create_button": {
                    "patterns": ["أنشئ زر", "عمل زر جديد", "ضع زر"],
                    "entities": ["button_text", "button_color"],
                    "action_template": "create_button(text='{button_text}', color='{button_color}')"
                },
                "create_label": {
                    "patterns": ["أنشئ نص", "اكتب نص", "ضع نص"],
                    "entities": ["label_text", "label_color"],
                    "action_template": "create_label(text='{label_text}', color='{label_color}')"
                }
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(default_mappings, f, ensure_ascii=False, indent=4)
            return default_mappings

    def _load_entity_regex(self) -> Dict[str, str]:
        """
        Loads entity extraction regex patterns from a JSON file.
        The structure is expected to be:
        {
            "entity_type_1": "regex_pattern_1",
            "entity_type_2": "regex_pattern_2"
        }
        """
        filepath = self._get_kb_path("entity_regex.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Initialize with some basic examples
            default_regex = {
                "button_text": r"\"([^\"]*)\"",  # Captures text within quotes
                "label_text": r"\"([^\"]*)\"",
                "button_color": r"(الأحمر|الأزرق|الأخضر|الأصفر|الأبيض|الأسود)", # Common colors
                "label_color": r"(الأحمر|الأزرق|الأخضر|الأصفر|الأبيض|الأسود)"
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(default_regex, f, ensure_ascii=False, indent=4)
            return default_regex

    def save_intent_mapping(self, intent_name: str, patterns: List[str], entities: List[str], action_template: str):
        """Saves a new or updates an existing intent mapping."""
        self.intent_mappings[intent_name] = {
            "patterns": patterns,
            "entities": entities,
            "action_template": action_template
        }
        filepath = self._get_kb_path("intent_mappings.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.intent_mappings, f, ensure_ascii=False, indent=4)
        print(f"Intent '{intent_name}' saved to knowledge base.")

    def save_entity_regex(self, entity_type: str, regex_pattern: str):
        """Saves a new or updates an existing entity regex pattern."""
        self.entity_regex_patterns[entity_type] = regex_pattern
        filepath = self._get_kb_path("entity_regex.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.entity_regex_patterns, f, ensure_ascii=False, indent=4)
        print(f"Entity regex for '{entity_type}' saved to knowledge base.")

    def extract_intent_and_entities(self, user_utterance: str) -> Dict[str, Any]:
        """
        Processes an Arabic user utterance to extract intent and entities.

        Args:
            user_utterance (str): The Arabic text input from the user.

        Returns:
            Dict[str, Any]: A dictionary containing 'intent', 'entities', and 'action_template'.
                            Returns an empty dictionary if no intent is recognized.
        """
        import re

        best_match = None
        highest_score = 0

        # Simple pattern matching for intent
        for intent_name, mapping_data in self.intent_mappings.items():
            for pattern in mapping_data["patterns"]:
                if pattern in user_utterance:
                    # Basic scoring: more specific patterns get higher score
                    score = len(pattern)
                    if score > highest_score:
                        highest_score = score
                        best_match = {
                            "intent": intent_name,
                            "entities": {},
                            "action_template": mapping_data.get("action_template", "")
                        }

        if not best_match:
            return {}

        # Entity extraction based on the recognized intent
        required_entities = self.intent_mappings[best_match['intent']].get('entities', [])
        action_template = best_match.get('action_template', '')

        for entity_type in required_entities:
            if entity_type in self.entity_regex_patterns:
                regex = self.entity_regex_patterns[entity_type]
                match = re.search(regex, user_utterance, re.IGNORECASE | re.UNICODE)
                if match:
                    # Capture group 1 is typically the actual value
                    entity_value = match.group(1) if match.groups() else match.group(0)
                    best_match["entities"][entity_type] = entity_value
                    # Replace the placeholder in the action template if it exists
                    if entity_type in action_template:
                         # Simple replacement, assumes template uses {entity_type}
                        action_template = action_template.replace(f"{{{entity_type}}}", entity_value)


        # Update the action template with extracted entities if it's still a template
        if best_match["intent"] in self.intent_mappings and "action_template" in self.intent_mappings[best_match["intent"]]:
            template = self.intent_mappings[best_match["intent"]]["action_template"]
            extracted_values = best_match["entities"]
            try:
                # Use string formatting to fill the template
                filled_template = template.format(**extracted_values)
                best_match["action_template"] = filled_template
            except KeyError as e:
                print(f"Warning: Missing entity for template formatting: {e}")
                # Keep the original template or partially filled one
                pass # Or assign a partially filled template

        return best_match

    def cleanup_knowledge_base_if_empty(self):
        """
        Cleans up the knowledge base directory if it's empty of essential files
        after some operations (e.g., during testing or initial setup).
        This is a specific cleanup logic, not a general delete-all.
        """
        # This method is intended to be called by a higher level orchestrator
        # after potentially creating and deleting dummy files.
        # It checks if the essential KB files exist. If not, and the directory
        # is truly empty of everything, it could be removed.
        # For now, it serves as a placeholder for more complex cleanup logic
        # that might be needed.
        if not os.listdir(self.knowledge_base_dir):
            print(f"Knowledge base directory '{self.knowledge_base_dir}' is empty. Consider removing it if no longer needed.")
            # Example: os.rmdir(self.knowledge_base_dir) # Uncomment if direct removal is desired


def demo_arabic_nlp_processor():
    """
    Demonstrates the functionality of the ArabicNlpProcessor.
    """
    kb_dir = "arabic_nlp_kb_demo"
    print(f"\n--- Initializing ArabicNlpProcessor with KB directory: {kb_dir} ---")
    nlp_processor = ArabicNlpProcessor(knowledge_base_dir=kb_dir)

    # --- Test Case 1: Basic intent and entity extraction ---
    utterance1 = "أنشئ زر \"ابدأ\" باللون الأحمر"
    print(f"\nUser utterance: '{utterance1}'")
    result1 = nlp_processor.extract_intent_and_entities(utterance1)
    print(f"NLP Result: {result1}")

    # --- Test Case 2: Another intent ---
    utterance2 = "اكتب نص \"مرحباً بالعالم\" باللون الأزرق"
    print(f"\nUser utterance: '{utterance2}'")
    result2 = nlp_processor.extract_intent_and_entities(utterance2)
    print(f"NLP Result: {result2}")

    # --- Test Case 3: Intent not recognized ---
    utterance3 = "ما هو الطقس اليوم؟"
    print(f"\nUser utterance: '{utterance3}'")
    result3 = nlp_processor.extract_intent_and_entities(utterance3)
    print(f"NLP Result: {result3}")

    # --- Test Case 4: Add a new intent and entity type ---
    print("\n--- Adding a new intent: 'create_image' ---")
    nlp_processor.save_intent_mapping(
        intent_name="create_image",
        patterns=["ضع صورة", "أضف صورة", "أنشئ صورة"],
        entities=["image_url", "image_size"],
        action_template="create_image(url='{image_url}', size='{image_size}')"
    )
    nlp_processor.save_entity_regex(
        entity_type="image_url",
        regex_pattern=r"(https?://[^\s]+)" # Basic URL regex
    )
    nlp_processor.save_entity_regex(
        entity_type="image_size",
        regex_pattern=r"(صغير|متوسط|كبير)"
    )

    utterance4 = "أضف صورة \"http://example.com/logo.png\" بالحجم الكبير"
    print(f"\nUser utterance: '{utterance4}'")
    result4 = nlp_processor.extract_intent_and_entities(utterance4)
    print(f"NLP Result: {result4}")

    # --- Test Case 5: Using the newly added intent with different phrasing ---
    utterance5 = "ضع صورة \"https://my.site/icon.jpg\" بالحجم الصغير"
    print(f"\nUser utterance: '{utterance5}'")
    result5 = nlp_processor.extract_intent_and_entities(utterance5)
    print(f"NLP Result: {result5}")

    # --- Test Case 6: Extracting only entities for an existing intent ---
    utterance6 = "أنشئ زر \"تسجيل الدخول\"" # Color is missing
    print(f"\nUser utterance: '{utterance6}'")
    result6 = nlp_processor.extract_intent_and_entities(utterance6)
    print(f"NLP Result: {result6}")

    # --- Cleanup ---
    print("\n--- Cleaning up demo knowledge base files ---")
    # This cleanup logic might vary based on how the demo is structured.
    # For a simple demo, we might just remove the created directory.
    import shutil
    if os.path.exists(kb_dir):
        try:
            shutil.rmtree(kb_dir)
            print(f"Demo knowledge base directory '{kb_dir}' removed.")
        except OSError as e:
            print(f"Error removing directory {kb_dir}: {e}")

    print("\n--- ArabicNlpProcessor Demo Finished ---")


# Example of how this module might be integrated:
if __name__ == "__main__":
    # To run the demo directly
    demo_arabic_nlp_processor()

    # Example of using it in a hypothetical pipeline:
    #
    # from some_other_module import CodeGenerator # Assume this exists
    # from some_other_module import ApkCompiler   # Assume this exists
    #
    # arabic_processor = ArabicNlpProcessor()
    # code_generator = CodeGenerator()
    # apk_compiler = ApkCompiler()
    #
    # natural_language_command = "أنشئ زر \"حفظ\" باللون الأخضر"
    #
    # # Lobe 0: Language Processing (Arabic)
    # nlp_result = arabic_processor.extract_intent_and_entities(natural_language_command)
    #
    # if nlp_result and nlp_result.get("intent"):
    #     # Lobe 6: Synthesis (combining NLP result with code generation logic)
    #     # This step might prepare a more structured representation for the code generator.
    #     structured_command = {
    #         "intent": nlp_result["intent"],
    #         "action": nlp_result.get("action_template"), # This is now a direct command string
    #         "entities": nlp_result.get("entities", {})
    #     }
    #     print(f"\nSynthesized Command: {structured_command}")
    #
    #     # Lobe 4: Code Generation
    #     generated_code_snippet = code_generator.generate_code(structured_command)
    #     print(f"\nGenerated Code Snippet:\n{generated_code_snippet}")
    #
    #     # Lobe 8: APK Compilation
    #     # This would involve saving the snippet to a file, structuring a project,
    #     # and then compiling.
    #     # apk_path = apk_compiler.compile_apk(generated_code_snippet)
    #     # print(f"\nAPK Compiled Successfully: {apk_path}")
    # else:
    #     print("Could not understand the command.")