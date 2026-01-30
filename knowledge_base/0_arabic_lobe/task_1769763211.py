import os
import json
import re

# Assuming a structure for knowledge base files
KNOWLEDGE_BASE_DIR_ARABIC = "arabic_knowledge_base"

class ArabicNLPProcessor:
    """
    Processes Arabic natural language to extract structured data for APK generation.
    This lobe focuses on understanding Arabic syntax, semantics, and intent.
    """

    def __init__(self, knowledge_base_dir=KNOWLEDGE_BASE_DIR_ARABIC):
        self.knowledge_base_dir = knowledge_base_dir
        os.makedirs(self.knowledge_base_dir, exist_ok=True)
        self.rules = self._load_rules()

    def _load_rules(self):
        """
        Loads predefined rules for Arabic NLP processing.
        These rules would typically be stored in external files (e.g., JSON, YAML)
        and would define mappings from Arabic phrases to structured data.
        """
        rules_file = os.path.join(self.knowledge_base_dir, "arabic_nlp_rules.json")
        if os.path.exists(rules_file):
            with open(rules_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Default rules if none exist
            return {
                "intent_mapping": {
                    "إنشاء تطبيق": "create_app",
                    "تطبيق بميزة": "add_feature",
                    "شاشة جديدة": "add_screen",
                    "زر": "add_button",
                    "نص": "add_text",
                    "صورة": "add_image",
                    "إدخال": "add_input_field",
                    "عرض البيانات": "display_data",
                    "قائمة": "add_list",
                    "قاعدة بيانات": "configure_database"
                },
                "entity_extraction": {
                    "اسم التطبيق": "app_name",
                    "اسم الشاشة": "screen_name",
                    "نص الزر": "button_text",
                    "محتوى النص": "text_content",
                    "مسار الصورة": "image_path",
                    "اسم الحقل": "field_name",
                    "نوع البيانات": "data_type",
                    "اسم الجدول": "table_name",
                    "أعمدة": "columns"
                }
            }

    def _save_rules(self):
        """Saves the current rules to the knowledge base."""
        rules_file = os.path.join(self.knowledge_base_dir, "arabic_nlp_rules.json")
        with open(rules_file, 'w', encoding='utf-8') as f:
            json.dump(self.rules, f, indent=4, ensure_ascii=False)

    def process_arabic_prompt(self, prompt: str) -> dict:
        """
        Processes an Arabic natural language prompt to extract structured intent and entities.

        Args:
            prompt: The Arabic natural language prompt.

        Returns:
            A dictionary representing the structured output, including intent and extracted entities.
        """
        structured_output = {"intent": None, "entities": {}}
        prompt_lower = prompt.lower()

        # 1. Intent Recognition
        for phrase, intent_tag in self.rules["intent_mapping"].items():
            if phrase in prompt_lower:
                structured_output["intent"] = intent_tag
                # Remove the matched phrase to simplify entity extraction
                prompt_lower = prompt_lower.replace(phrase, "", 1)
                break

        # 2. Entity Extraction
        # This is a simplified approach. A more robust solution would involve
        # Named Entity Recognition (NER) models trained on Arabic.
        for entity_key, entity_tag in self.rules["entity_extraction"].items():
            # Look for patterns like "اسم التطبيق: [value]" or "تطبيق اسمه [value]"
            # This uses regex for demonstration purposes.
            match = re.search(rf"{entity_key}\s*[:؛]\s*([^,.;]+)", prompt_lower, re.IGNORECASE)
            if match:
                entity_value = match.group(1).strip()
                if entity_value:
                    structured_output["entities"][entity_tag] = entity_value
                    prompt_lower = prompt_lower.replace(match.group(0), "", 1)
                    continue # Move to the next entity to avoid re-processing

            # Alternative pattern: "اسم التطبيق [value]"
            match_alt = re.search(rf"{entity_key}\s+([^,.;]+)", prompt_lower, re.IGNORECASE)
            if match_alt:
                entity_value = match_alt.group(1).strip()
                # Check if the entity_value is not a part of another phrase that might be an intent
                if entity_value and not any(phrase in entity_value for phrase in self.rules["intent_mapping"]):
                    structured_output["entities"][entity_tag] = entity_value
                    prompt_lower = prompt_lower.replace(match_alt.group(0), "", 1)
                    continue

        # Special handling for list of columns
        if "أعمدة" in prompt_lower:
            columns_match = re.search(r"أعمدة\s*[:؛]?\s*(.+?)(?:،|;|$)", prompt_lower, re.IGNORECASE)
            if columns_match:
                columns_str = columns_match.group(1).strip()
                # Split by comma or semicolon, and then by colon for key:value pairs (e.g., "name:string")
                columns_list = []
                for col_spec in re.split(r'[،;]\s*', columns_str):
                    if ':' in col_spec:
                        name, col_type = col_spec.split(':', 1)
                        columns_list.append({"name": name.strip(), "type": col_type.strip()})
                    else:
                        columns_list.append({"name": col_spec.strip()}) # Assume default type if not specified
                structured_output["entities"]["columns"] = columns_list
                prompt_lower = prompt_lower.replace(columns_match.group(0), "", 1)

        # Further refinement could be done here based on the detected intent

        # Clean up any remaining extra whitespace
        structured_output["entities"] = {k: v.strip() for k, v in structured_output["entities"].items() if v.strip()}

        return structured_output

    def cleanup_knowledge_base_if_empty(self):
        """
        Cleans up the knowledge base directory if it becomes empty after potential removals.
        This is a placeholder for more complex KB management.
        """
        if not os.listdir(self.knowledge_base_dir) or (len(os.listdir(self.knowledge_base_dir)) == 1 and "arabic_nlp_rules.json" in os.listdir(self.knowledge_base_dir) and not self._has_other_files()):
            print(f"Knowledge base directory '{self.knowledge_base_dir}' is empty. Removing it.")
            try:
                os.rmdir(self.knowledge_base_dir)
            except OSError as e:
                print(f"Error removing directory {self.knowledge_base_dir}: {e}")

    def _has_other_files(self):
        """Helper to check if there are files other than the rules file."""
        for item in os.listdir(self.knowledge_base_dir):
            if item != "arabic_nlp_rules.json":
                return True
        return False

    def add_rule(self, rule_type: str, key: str, value: str):
        """
        Allows dynamic addition or modification of NLP rules.
        Args:
            rule_type: 'intent_mapping' or 'entity_extraction'.
            key: The Arabic phrase or entity key.
            value: The corresponding tag or identifier.
        """
        if rule_type not in ["intent_mapping", "entity_extraction"]:
            raise ValueError("Invalid rule_type. Must be 'intent_mapping' or 'entity_extraction'.")

        if key in self.rules.get(rule_type, {}):
            print(f"Warning: Overwriting existing rule for '{key}' in '{rule_type}'.")
        self.rules[rule_type][key] = value
        self._save_rules()
        print(f"Rule added: '{key}' -> '{value}' in '{rule_type}'.")

    def remove_rule(self, rule_type: str, key: str):
        """
        Allows dynamic removal of NLP rules.
        Args:
            rule_type: 'intent_mapping' or 'entity_extraction'.
            key: The Arabic phrase or entity key to remove.
        """
        if rule_type not in ["intent_mapping", "entity_extraction"]:
            raise ValueError("Invalid rule_type. Must be 'intent_mapping' or 'entity_extraction'.")

        if key in self.rules.get(rule_type, {}):
            del self.rules[rule_type][key]
            self._save_rules()
            print(f"Rule removed: '{key}' from '{rule_type}'.")
        else:
            print(f"Warning: Rule '{key}' not found in '{rule_type}'.")


# Example Usage (for demonstration, this code would be part of a larger system)
if __name__ == "__main__":
    # Ensure the knowledge base directory exists for the demo
    os.makedirs(KNOWLEDGE_BASE_DIR_ARABIC, exist_ok=True)

    nlp_processor = ArabicNLPProcessor()

    # Test prompts
    prompts = [
        "إنشاء تطبيق جديد اسمه 'سوق', بشاشة رئيسية اسمها 'الصفحة الرئيسية'",
        "أريد إضافة زر في الشاشة 'الصفحة الرئيسية' نص الزر 'إضافة للعربة'",
        "أضف نصًا في الشاشة 'تفاصيل المنتج' محتوى النص 'هذا منتج رائع'",
        "أضف صورة في الشاشة 'معرض الصور' مسار الصورة 'assets/image1.png'",
        "أضف حقل إدخال في الشاشة 'تسجيل الدخول' اسم الحقل 'البريد الإلكتروني'",
        "عرض البيانات من جدول 'المستخدمين' بأعمدة: id:integer, name:string, email:string",
        "أضف شاشة جديدة اسمها 'الإعدادات'",
        "إنشاء تطبيق بميزة قاعدة بيانات",
        "تطبيق اسمه 'المفكرة' مع شاشة 'الملاحظات' وقاعدة بيانات اسمها 'notes_db' بأعمدة: title:string, content:text"
    ]

    for i, prompt in enumerate(prompts):
        print(f"\n--- Processing Prompt {i+1} ---")
        print(f"Prompt: {prompt}")
        structured_data = nlp_processor.process_arabic_prompt(prompt)
        print(f"Structured Output: {json.dumps(structured_data, indent=2, ensure_ascii=False)}")

    # Example of adding a rule dynamically
    print("\n--- Adding a new rule ---")
    nlp_processor.add_rule("intent_mapping", "تحديث البيانات", "update_data")
    nlp_processor.add_rule("entity_extraction", "اسم المستخدم", "username")

    print("\n--- Processing prompt with new rule ---")
    new_prompt = "تحديث البيانات للمستخدم 'علي' في قاعدة بيانات 'users'"
    print(f"Prompt: {new_prompt}")
    structured_data_new = nlp_processor.process_arabic_prompt(new_prompt)
    print(f"Structured Output: {json.dumps(structured_data_new, indent=2, ensure_ascii=False)}")

    # Example of removing a rule
    print("\n--- Removing a rule ---")
    nlp_processor.remove_rule("intent_mapping", "إنشاء تطبيق")
    print("\n--- Processing prompt after rule removal ---")
    prompt_after_removal = "إنشاء تطبيق جديد اسمه 'المهام'"
    print(f"Prompt: {prompt_after_removal}")
    structured_data_after_removal = nlp_processor.process_arabic_prompt(prompt_after_removal)
    print(f"Structured Output: {json.dumps(structured_data_after_removal, indent=2, ensure_ascii=False)}")


    # Clean up dummy files created by MockApkGenerator
    print("\n--- Cleaning up dummy knowledge base files ---")
    nlp_processor.cleanup_knowledge_base_if_empty() # This will only run if the directory becomes empty

    print("\n--- Arabic Parser and Generator Lobe Demo Finished ---")