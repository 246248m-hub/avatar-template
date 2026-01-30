import os
import json
import re
from typing import Dict, Any, List

# Assume KNOWLEDGE_BASE_DIR is defined elsewhere and accessible
# For demonstration purposes, let's define it here
KNOWLEDGE_BASE_DIR = "./knowledge_base"
if not os.path.exists(KNOWLEDGE_BASE_DIR):
    os.makedirs(KNOWLEDGE_BASE_DIR)


class ArabicAPKGenerator:
    """
    This module is responsible for parsing Arabic natural language prompts,
    synthesizing them into a structured representation, and then generating
    components suitable for APK compilation.
    """

    def __init__(self, knowledge_base_path: str = KNOWLEDGE_BASE_DIR):
        self.knowledge_base_path = knowledge_base_path
        self.arabic_syntax_rules = self._load_arabic_syntax_rules()
        self.semantic_mapping = self._load_semantic_mapping()

    def _load_arabic_syntax_rules(self) -> Dict[str, Any]:
        """
        Loads predefined Arabic grammatical and structural rules from a JSON file.
        These rules help in parsing the natural language input.
        """
        rules_path = os.path.join(self.knowledge_base_path, "arabic_syntax_rules.json")
        if os.path.exists(rules_path):
            with open(rules_path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            # Fallback or default rules if file not found
            return {
                "sentence_structure": ["Subject", "Verb", "Object"],
                "verb_patterns": {},
                "noun_patterns": {},
                "adjective_patterns": {},
                "prepositional_phrases": {}
            }

    def _load_semantic_mapping(self) -> Dict[str, Any]:
        """
        Loads a mapping from Arabic keywords and phrases to semantic actions
        or UI components. This is crucial for translating user intent.
        """
        mapping_path = os.path.join(self.knowledge_base_path, "arabic_semantic_mapping.json")
        if os.path.exists(mapping_path):
            with open(mapping_path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            # Fallback or default mapping
            return {
                "زر": {"type": "button", "action": "click"},
                "عرض": {"type": "text_view", "action": "display"},
                "إدخال": {"type": "edit_text", "action": "input"},
                "قائمة": {"type": "list_view", "action": "display"},
                "تطبيق": {"type": "app", "action": "create"},
                "صفحة": {"type": "activity", "action": "create"},
                "انقر": {"action": "click"},
                "غير": {"action": "change"},
                "أضف": {"action": "add"},
                "احذف": {"action": "delete"}
            }

    def parse_arabic_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Parses the Arabic natural language prompt to extract its core components
        and intent. This is a simplified parser for demonstration.
        """
        parsed_data = {
            "intent": None,
            "components": [],
            "keywords": [],
            "actions": []
        }

        # Simple keyword spotting and mapping to semantic actions
        words = re.findall(r'\b\w+\b', prompt.lower(), re.UNICODE)
        for word in words:
            if word in self.semantic_mapping:
                mapping = self.semantic_mapping[word]
                if "type" in mapping:
                    parsed_data["components"].append({
                        "name": word,
                        "type": mapping["type"],
                        "attributes": {}
                    })
                if "action" in mapping:
                    parsed_data["actions"].append({
                        "keyword": word,
                        "action": mapping["action"]
                    })
            parsed_data["keywords"].append(word)

        # Basic intent detection (e.g., creating an app or a screen)
        if any("تطبيق" in comp.get("name", "") for comp in parsed_data["components"]) or "إنشاء تطبيق" in prompt:
            parsed_data["intent"] = "create_app"
        elif any("صفحة" in comp.get("name", "") for comp in parsed_data["components"]) or "إنشاء صفحة" in prompt:
            parsed_data["intent"] = "create_screen"
        elif any(action["action"] == "click" for action in parsed_data["actions"]):
            parsed_data["intent"] = "user_interaction"
        else:
            parsed_data["intent"] = "unknown"

        # Further sophisticated parsing would involve NLP libraries for
        # Part-of-Speech tagging, Named Entity Recognition, dependency parsing, etc.
        # This simplified version focuses on direct keyword mapping.

        return parsed_data

    def synthesize_apk_components(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesizes the parsed data into a structured format that can be used
        to generate APK components. This involves resolving ambiguities and
        adding default attributes.
        """
        synthesized_components = {
            "app_name": "MyArabicApp",
            "activities": [],
            "ui_elements": []
        }

        if parsed_data["intent"] == "create_app":
            synthesized_components["app_name"] = self._extract_app_name(parsed_data)
            # Logic to create main activity and potentially others
            main_activity = {"name": "MainActivity", "layout": "activity_main.xml", "elements": []}
            synthesized_components["activities"].append(main_activity)

        elif parsed_data["intent"] == "create_screen":
            screen_name = self._extract_screen_name(parsed_data)
            new_activity = {"name": screen_name, "layout": f"{screen_name.lower()}.xml", "elements": []}
            # Check if this activity already exists to avoid duplicates
            if not any(act["name"] == screen_name for act in synthesized_components["activities"]):
                synthesized_components["activities"].append(new_activity)

        # Process UI elements from parsed components
        component_id_counter = 0
        for comp in parsed_data["components"]:
            element_name = comp.get("name")
            element_type = comp.get("type")
            if element_type:
                # Assign unique IDs and potentially default text/labels
                element_id = f"id_{element_type}_{component_id_counter}"
                default_text = self._get_default_text(element_name)
                element_attributes = comp.get("attributes", {})
                element_attributes.update({
                    "id": element_id,
                    "text": default_text
                })

                synthesized_components["ui_elements"].append({
                    "name": element_name,
                    "type": element_type,
                    "attributes": element_attributes
                })
                component_id_counter += 1

        # Associate UI elements with activities based on context (simplified)
        # In a real scenario, this would be much more complex, looking at sentence structure
        if synthesized_components["activities"]:
            current_activity = synthesized_components["activities"][0] # Assign to first activity by default
            for ui_element in synthesized_components["ui_elements"]:
                if ui_element["type"] not in ["app", "activity"]: # Avoid adding app/activity as UI element
                    current_activity["elements"].append(ui_element)

        return synthesized_components

    def _extract_app_name(self, parsed_data: Dict[str, Any]) -> str:
        """
        Extracts the app name from the parsed data, looking for explicit mentions.
        """
        app_name_keywords = ["تطبيق", "اسم التطبيق"]
        for word in parsed_data.get("keywords", []):
            if word in self.semantic_mapping and self.semantic_mapping[word].get("type") == "app":
                continue # Skip "app" keyword itself

            # Look for noun phrases following "تطبيق" or "اسم التطبيق"
            prompt_words = parsed_data.get("keywords", [])
            try:
                app_keyword_index = prompt_words.index("تطبيق")
                if app_keyword_index < len(prompt_words) - 1:
                    return prompt_words[app_keyword_index + 1].capitalize()
            except ValueError:
                pass
            try:
                app_keyword_index = prompt_words.index("اسم")
                if app_keyword_index < len(prompt_words) - 2 and prompt_words[app_keyword_index + 1] == "التطبيق":
                    return prompt_words[app_keyword_index + 2].capitalize()
            except ValueError:
                pass

        # Fallback if no explicit name found
        return "MyArabicApp"

    def _extract_screen_name(self, parsed_data: Dict[str, Any]) -> str:
        """
        Extracts the screen name from the parsed data.
        """
        screen_name_keywords = ["صفحة", "شاشة"]
        for word in parsed_data.get("keywords", []):
            if word in self.semantic_mapping and self.semantic_mapping[word].get("type") == "activity":
                continue # Skip "page" or "screen" keyword itself

            prompt_words = parsed_data.get("keywords", [])
            try:
                screen_keyword_index = prompt_words.index("صفحة")
                if screen_keyword_index < len(prompt_words) - 1:
                    return prompt_words[screen_keyword_index + 1].capitalize()
            except ValueError:
                pass
            try:
                screen_keyword_index = prompt_words.index("شاشة")
                if screen_keyword_index < len(prompt_words) - 1:
                    return prompt_words[screen_keyword_index + 1].capitalize()
            except ValueError:
                pass

        return "NewScreen"

    def _get_default_text(self, element_name: str) -> str:
        """
        Provides default text or labels for UI elements based on their names.
        This can be expanded with more sophisticated Arabic word analysis.
        """
        default_texts = {
            "زر": "اضغط هنا",
            "عرض": "نص افتراضي",
            "إدخال": "أدخل نصًا",
            "قائمة": "قائمة العناصر"
        }
        return default_texts.get(element_name, element_name.capitalize())

    def generate_apk_components(self, prompt: str) -> Dict[str, Any]:
        """
        Orchestrates the parsing and synthesis process to generate the components
        needed for APK compilation.
        """
        parsed_data = self.parse_arabic_prompt(prompt)
        print(f"--- Parsed Data: {json.dumps(parsed_data, indent=2, ensure_ascii=False)} ---")
        synthesized_components = self.synthesize_apk_components(parsed_data)
        print(f"--- Synthesized Components: {json.dumps(synthesized_components, indent=2, ensure_ascii=False)} ---")
        return synthesized_components

# --- DEMO USAGE ---
if __name__ == "__main__":
    # Ensure knowledge base files exist for demonstration
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        os.makedirs(KNOWLEDGE_BASE_DIR)

    arabic_syntax_rules_path = os.path.join(KNOWLEDGE_BASE_DIR, "arabic_syntax_rules.json")
    if not os.path.exists(arabic_syntax_rules_path):
        with open(arabic_syntax_rules_path, "w", encoding="utf-8") as f:
            json.dump({
                "sentence_structure": ["Subject", "Verb", "Object"],
                "verb_patterns": {},
                "noun_patterns": {},
                "adjective_patterns": {},
                "prepositional_phrases": {}
            }, f, ensure_ascii=False, indent=4)

    arabic_semantic_mapping_path = os.path.join(KNOWLEDGE_BASE_DIR, "arabic_semantic_mapping.json")
    if not os.path.exists(arabic_semantic_mapping_path):
        with open(arabic_semantic_mapping_path, "w", encoding="utf-8") as f:
            json.dump({
                "زر": {"type": "button", "action": "click"},
                "عرض": {"type": "text_view", "action": "display"},
                "إدخال": {"type": "edit_text", "action": "input"},
                "قائمة": {"type": "list_view", "action": "display"},
                "تطبيق": {"type": "app", "action": "create"},
                "صفحة": {"type": "activity", "action": "create"},
                "شاشة": {"type": "activity", "action": "create"},
                "انقر": {"action": "click"},
                "غير": {"action": "change"},
                "أضف": {"action": "add"},
                "احذف": {"action": "delete"},
                "اسم": {"type": "app_name_hint"}, # Special hint for name extraction
                "التطبيق": {"type": "app_name_hint"} # Special hint for name extraction
            }, f, ensure_ascii=False, indent=4)

    generator = ArabicAPKGenerator(knowledge_base_path=KNOWLEDGE_BASE_DIR)

    print("\n--- Testing Arabic Prompt Parsing and Synthesis ---")

    # Test case 1: Creating an app with a button
    prompt1 = "إنشاء تطبيق باسم 'تطبيقي الأول' مع زر لعرض رسالة."
    apk_components1 = generator.generate_apk_components(prompt1)
    print(f"\nGenerated APK Components for Prompt 1:\n{json.dumps(apk_components1, indent=2, ensure_ascii=False)}")

    # Test case 2: Creating a new screen with a text view
    prompt2 = "أضف صفحة جديدة اسمها 'معلومات'."
    apk_components2 = generator.generate_apk_components(prompt2)
    print(f"\nGenerated APK Components for Prompt 2:\n{json.dumps(apk_components2, indent=2, ensure_ascii=False)}")

    # Test case 3: Adding multiple elements to an existing structure
    prompt3 = "في التطبيق، قم بإنشاء إدخال نصي وزر."
    # To demonstrate adding to an existing structure, we would ideally have
    # a pre-existing `synthesized_components` object. For this standalone demo,
    # we'll show how it generates new elements that *could* be merged.
    # In a real flow, the output of prompt1 would be fed into prompt3.
    print("\n--- Simulating adding elements to an existing app structure (conceptual) ---")
    print("In a real scenario, the `apk_components1` would be an input to further generation.")
    apk_components3_standalone = generator.generate_apk_components(prompt3)
    print(f"\nGenerated APK Components for Prompt 3 (standalone):\n{json.dumps(apk_components3_standalone, indent=2, ensure_ascii=False)}")

    # Test case 4: A simpler prompt
    prompt4 = "إنشاء صفحة تسمى 'الرئيسية' بها عرض نص."
    apk_components4 = generator.generate_apk_components(prompt4)
    print(f"\nGenerated APK Components for Prompt 4:\n{json.dumps(apk_components4, indent=2, ensure_ascii=False)}")

    print("\n--- Arabic Parser and Generator Module Demo Finished ---")