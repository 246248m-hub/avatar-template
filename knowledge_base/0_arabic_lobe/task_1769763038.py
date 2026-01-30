import os
import json
from collections import defaultdict

# Assuming apk_generator and language_lobe are defined and accessible in the environment
# For demonstration purposes, we'll define mock classes if they don't exist.

class MockApkGenerator:
    def __init__(self, knowledge_base_dir="knowledge_base"):
        self.knowledge_base_dir = knowledge_base_dir
        os.makedirs(self.knowledge_base_dir, exist_ok=True)

    def save_knowledge_item(self, item_id, data):
        filepath = os.path.join(self.knowledge_base_dir, f"{item_id}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Saved knowledge item: {item_id}")

    def load_knowledge_item(self, item_id):
        filepath = os.path.join(self.knowledge_base_dir, f"{item_id}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def get_all_knowledge_items(self):
        items = {}
        for filename in os.listdir(self.knowledge_base_dir):
            if filename.endswith(".json"):
                item_id = os.path.splitext(filename)[0]
                items[item_id] = self.load_knowledge_item(item_id)
        return items

class MockLanguageLobe:
    def __init__(self):
        self.apk_generator = MockApkGenerator() # Initialize a mock APK generator

    def parse_arabic_text(self, text):
        """
        Simulates parsing Arabic text to extract structured information.
        In a real scenario, this would involve sophisticated NLP techniques.
        """
        print(f"Mock parsing Arabic text: '{text[:50]}...'")
        # For this mock, we'll just return a simplified structure
        if "اسم التطبيق" in text:
            app_name = text.split("اسم التطبيق")[1].split(":")[1].strip().split("\n")[0]
            description = text.split("وصف التطبيق")[1].split(":")[1].strip()
            return {
                "type": "app_definition",
                "name": app_name,
                "description": description
            }
        elif "مكون واجهة" in text:
            component_type = text.split("مكون واجهة")[1].split(":")[1].strip().split("\n")[0]
            label = text.split("اسم للعرض")[1].split(":")[1].strip()
            return {
                "type": "ui_component_definition",
                "component_type": component_type,
                "label": label
            }
        return {"type": "unrecognized", "original_text": text}

    def generate_arabic_text(self, prompt, knowledge_base_dir=None):
        """
        Simulates generating Arabic text based on a prompt and knowledge base.
        """
        print(f"Mock generating Arabic text for prompt: '{prompt[:50]}...'")
        # In a real scenario, this would leverage a language model.
        # Here, we'll simulate based on the prompt.
        if "template for an activity" in prompt.lower():
            return "template for an activity:\nاسم النشاط: [اسم النشاط]\nالغرض: [الغرض من النشاط]\nالخطوات: [الخطوات]"
        elif "template for a button" in prompt.lower():
            return "template for a button:\nاسم الزر: [اسم الزر]\nنص الزر: [نص الزر]\nإجراء عند الضغط: [الإجراء]"
        return "Generated Arabic text placeholder."

# Mocking the existence of these lobes for the sake of this module's definition
if 'apk_generator' not in globals():
    apk_generator = MockApkGenerator()
if 'language_lobe' not in globals():
    language_lobe = MockLanguageLobe()

# --- Lobe 3_arabic_parser_generator_lobe ---
class ArabicParserGeneratorLobe:
    """
    This lobe is responsible for parsing Arabic natural language
    to extract information relevant to APK generation and generating
    Arabic text based on templates or extracted knowledge.
    """
    def __init__(self, language_lobe, apk_generator):
        self.language_lobe = language_lobe
        self.apk_generator = apk_generator
        self.knowledge_base_dir = apk_generator.knowledge_base_dir
        self.component_registry = {}  # Stores definitions of UI components
        self.activity_registry = {}   # Stores definitions of activities

    def process_arabic_instruction(self, instruction: str):
        """
        Processes a natural language Arabic instruction to extract
        app definitions, component definitions, or other relevant data.
        Stores extracted information in the knowledge base.
        """
        parsed_data = self.language_lobe.parse_arabic_text(instruction)

        if parsed_data["type"] == "app_definition":
            app_name = parsed_data["name"]
            app_description = parsed_data["description"]
            item_id = f"app_{app_name.lower().replace(' ', '_')}"
            self.apk_generator.save_knowledge_item(item_id, {
                "type": "app_info",
                "name": app_name,
                "description": app_description
            })
            print(f"Stored app definition for '{app_name}'.")
            return item_id

        elif parsed_data["type"] == "ui_component_definition":
            component_type = parsed_data["component_type"]
            label = parsed_data["label"]
            component_id = f"component_{component_type.lower().replace(' ', '_')}_{label.lower().replace(' ', '_')}"
            self.component_registry[component_id] = {
                "type": "ui_component",
                "component_type": component_type,
                "label": label,
                "id": component_id
            }
            self.apk_generator.save_knowledge_item(component_id, self.component_registry[component_id])
            print(f"Stored UI component definition for '{label}' ({component_type}).")
            return component_id

        elif parsed_data["type"] == "unrecognized":
            print(f"Could not parse instruction: '{instruction}'")
            return None

        return None

    def generate_arabic_template(self, template_type: str, context: dict = None) -> str:
        """
        Generates Arabic text for predefined templates (e.g., for activities, buttons)
        using the language lobe.
        """
        if context is None:
            context = {}

        prompt = f"Provide a template for a {template_type} in Arabic."
        if context:
            prompt += f" Consider the following context: {context}"

        generated_text = self.language_lobe.generate_arabic_text(prompt)
        return generated_text

    def retrieve_knowledge_item(self, item_id: str):
        """
        Retrieves a specific knowledge item from the knowledge base.
        """
        return self.apk_generator.load_knowledge_item(item_id)

    def get_all_stored_components(self):
        """
        Returns all currently stored UI component definitions.
        """
        return {k: v for k, v in self.component_registry.items() if v.get("type") == "ui_component"}

    def get_all_stored_activities(self):
        """
        Returns all currently stored activity definitions.
        """
        return {k: v for k, v in self.activity_registry.items() if v.get("type") == "activity"}

    def initialize_knowledge_base_if_empty(self):
        """
        Ensures the knowledge base directory exists.
        """
        os.makedirs(self.knowledge_base_dir, exist_ok=True)
        print(f"Ensured knowledge base directory exists: {self.knowledge_base_dir}")

    def cleanup_knowledge_base_if_empty(self):
        """
        Removes the knowledge base directory if it is empty.
        This is a simple cleanup and might need refinement.
        """
        if os.path.exists(self.knowledge_base_dir) and not os.listdir(self.knowledge_base_dir):
            os.rmdir(self.knowledge_base_dir)
            print(f"Removed empty knowledge base directory: {self.knowledge_base_dir}")

# --- Demo Usage ---
if __name__ == "__main__":
    print("--- Initiating Arabic Parser and Generator Lobe Demo ---")

    # Instantiate the lobe
    arabic_parser_generator = ArabicParserGeneratorLobe(language_lobe, apk_generator)

    # Ensure knowledge base directory exists
    arabic_parser_generator.initialize_knowledge_base_if_empty()

    # Process Arabic instructions
    instruction_1 = "اسم التطبيق: تطبيق المهام\nوصف التطبيق: يساعد المستخدمين على تنظيم مهامهم اليومية."
    item_id_1 = arabic_parser_generator.process_arabic_instruction(instruction_1)

    instruction_2 = "مكون واجهة: زر\nاسم للعرض: إضافة مهمة جديدة\n"
    item_id_2 = arabic_parser_generator.process_arabic_instruction(instruction_2)

    instruction_3 = "مكون واجهة: حقل إدخال نصي\nاسم للعرض: عنوان المهمة\n"
    item_id_3 = arabic_parser_generator.process_arabic_instruction(instruction_3)

    instruction_4 = "مكون واجهة: قائمة\nاسم للعرض: قائمة المهام المكتملة\n"
    item_id_4 = arabic_parser_generator.process_arabic_instruction(instruction_4)

    # Generate Arabic templates
    activity_template = arabic_parser_generator.generate_arabic_template("activity", {"purpose": "main screen"})
    print(f"\nGenerated Activity Template:\n{activity_template}")

    button_template = arabic_parser_generator.generate_arabic_template("button", {"action": "save"})
    print(f"\nGenerated Button Template:\n{button_template}")

    # Retrieve stored information
    print("\n--- Retrieving stored information ---")
    app_info = arabic_parser_generator.retrieve_knowledge_item(item_id_1)
    print(f"Retrieved App Info: {app_info}")

    component_info_2 = arabic_parser_generator.retrieve_knowledge_item(item_id_2)
    print(f"Retrieved Component Info (Button): {component_info_2}")

    # Get all stored components
    all_components = arabic_parser_generator.get_all_stored_components()
    print(f"\nAll Stored Components: {json.dumps(all_components, indent=4, ensure_ascii=False)}")

    # Example of unrecognized instruction
    instruction_5 = "هذه جملة لا يمكنني فهمها حالياً."
    arabic_parser_generator.process_arabic_instruction(instruction_5)

    # Clean up dummy files created by MockApkGenerator
    print("\n--- Cleaning up dummy knowledge base files ---")
    arabic_parser_generator.cleanup_knowledge_base_if_empty() # This will only run if the directory becomes empty

    print("\n--- Arabic Parser and Generator Lobe Demo Finished ---")