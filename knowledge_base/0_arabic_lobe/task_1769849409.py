import os
import shutil
import re

# Assume these are defined elsewhere and accessible
# KNOWLEDGE_BASE_DIR = "path/to/knowledge_base"
# TARGET_LANGUAGE = "arabic"

class ArabicParser:
    """
    Parses natural language Arabic text to extract structured information
    relevant for Android APK generation.
    """
    def __init__(self, knowledge_base_dir):
        self.knowledge_base_dir = knowledge_base_dir
        self.intent_keywords = self._load_intent_keywords()
        self.entity_patterns = self._load_entity_patterns()

    def _load_intent_keywords(self):
        """
        Loads keywords associated with different user intents from the knowledge base.
        This is a placeholder and would typically involve reading from a file or DB.
        """
        # Example:
        return {
            "create_button": ["زر", "أضف زر", "إنشاء زر"],
            "create_text_view": ["نص", "عرض نص", "مربع نص"],
            "set_text": ["اجعل النص", "غيّر النص", "ضع النص"],
            "set_color": ["لون", "غيّر اللون", "اجعل اللون"],
            "create_layout": ["تصميم", "شكل", "ترتيب"],
            "set_background": ["خلفية", "صورة خلفية"]
        }

    def _load_entity_patterns(self):
        """
        Loads regular expression patterns for extracting entities like text content, colors, etc.
        """
        # Example:
        return {
            "text_content": r'بـ"(.*?)"',
            "color_name": r'(أحمر|أزرق|أخضر|أسود|أبيض|أصفر)',
            "color_hex": r'#([0-9a-fA-F]{6})',
            "button_text": r'زر بـ"(.*?)"',
            "layout_type": r'(عمودي|أفقي|خطى)',
            "image_path": r'صورة "(.*?)"'
        }

    def parse(self, arabic_text):
        """
        Analyzes Arabic text to identify intent and extract relevant entities.

        Args:
            arabic_text (str): The natural language input in Arabic.

        Returns:
            dict: A structured representation of the parsed input,
                  including 'intent' and 'entities'.
        """
        intent = "unknown"
        entities = {}

        # Detect intent
        for intent_name, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in arabic_text.lower():
                    intent = intent_name
                    break
            if intent != "unknown":
                break

        # Extract entities based on detected intent or general patterns
        if intent == "set_text" or intent == "button_text":
            match = re.search(self.entity_patterns["text_content"], arabic_text)
            if match:
                entities["text_content"] = match.group(1)
        elif intent in ["set_color", "set_background"]:
            match_name = re.search(self.entity_patterns["color_name"], arabic_text)
            if match_name:
                entities["color"] = match_name.group(1)
            else:
                match_hex = re.search(self.entity_patterns["color_hex"], arabic_text)
                if match_hex:
                    entities["color"] = "#" + match_hex.group(1)
        elif intent == "create_button":
            match = re.search(self.entity_patterns["button_text"], arabic_text)
            if match:
                entities["button_text"] = match.group(1)
        elif intent == "create_layout":
            match = re.search(self.entity_patterns["layout_type"], arabic_text)
            if match:
                entities["layout_type"] = match.group(1)
        elif intent == "set_background":
            match = re.search(self.entity_patterns["image_path"], arabic_text)
            if match:
                entities["image_path"] = match.group(1)

        # General entity extraction if not covered by specific intents
        if "text_content" not in entities:
            match = re.search(self.entity_patterns["text_content"], arabic_text)
            if match:
                entities["text_content"] = match.group(1)
        if "color" not in entities:
            match_name = re.search(self.entity_patterns["color_name"], arabic_text)
            if match_name:
                entities["color"] = match_name.group(1)
            else:
                match_hex = re.search(self.entity_patterns["color_hex"], arabic_text)
                if match_hex:
                    entities["color"] = "#" + match_hex.group(1)

        return {"intent": intent, "entities": entities}

class ArabicGenerator:
    """
    Generates structured code representations (e.g., JSON, intermediate code)
    from parsed Arabic input, preparing it for code generation.
    """
    def __init__(self, target_language):
        self.target_language = target_language # e.g., "android_xml", "kotlin_code"
        self.layout_map = {
            "عمودي": "LinearLayout",
            "أفقي": "LinearLayout",
            "خطى": "RelativeLayout"
        }
        self.color_map = {
            "أحمر": "#FF0000",
            "أزرق": "#0000FF",
            "أخضر": "#00FF00",
            "أسود": "#000000",
            "أبيض": "#FFFFFF",
            "أصفر": "#FFFF00"
        }

    def generate_code_structure(self, parsed_data):
        """
        Translates parsed Arabic data into a structured format suitable for
        further processing into actual code.

        Args:
            parsed_data (dict): The output from ArabicParser.

        Returns:
            dict: A structured representation of the desired code elements.
        """
        generated_structure = {
            "elements": [],
            "layout_type": "LinearLayout", # Default
            "layout_orientation": "vertical" # Default for LinearLayout
        }

        intent = parsed_data.get("intent")
        entities = parsed_data.get("entities", {})

        if intent == "create_layout":
            layout_type_arabic = entities.get("layout_type")
            if layout_type_arabic:
                generated_structure["layout_type"] = self.layout_map.get(layout_type_arabic, "LinearLayout")
                if generated_structure["layout_type"] == "LinearLayout":
                    if "أفقي" in layout_type_arabic:
                        generated_structure["layout_orientation"] = "horizontal"
                    else:
                        generated_structure["layout_orientation"] = "vertical"
            else:
                 generated_structure["layout_type"] = "LinearLayout"
                 generated_structure["layout_orientation"] = "vertical"


        # Process elements based on intent
        element_config = {}
        if intent == "create_button":
            element_config["type"] = "Button"
            if "button_text" in entities:
                element_config["text"] = entities["button_text"]
        elif intent == "create_text_view":
            element_config["type"] = "TextView"
            if "text_content" in entities:
                element_config["text"] = entities["text_content"]
        elif intent == "set_text":
            # This intent usually modifies an existing element,
            # but for generation, we'll assume it's creating a new one for now,
            # or needs to be associated with an ID.
            element_config["type"] = "TextView"
            if "text_content" in entities:
                element_config["text"] = entities["text_content"]
        elif intent == "set_color":
            color_value = entities.get("color")
            if color_value:
                if color_value in self.color_map:
                    element_config["textColor"] = self.color_map[color_value]
                else:
                    element_config["textColor"] = color_value # Assume hex if not mapped
        elif intent == "set_background":
            color_value = entities.get("color")
            if color_value:
                if color_value in self.color_map:
                    element_config["backgroundColor"] = self.color_map[color_value]
                else:
                    element_config["backgroundColor"] = color_value
            image_path = entities.get("image_path")
            if image_path:
                element_config["backgroundImage"] = image_path


        if element_config:
            # If it's not a layout creation, add the element
            if intent != "create_layout":
                # Assign a temporary ID if none is provided implicitly or explicitly
                element_config["id"] = f"id/generated_{len(generated_structure['elements'])}"
                generated_structure["elements"].append(element_config)

        # If the intent was to set properties for an element, we need to find it or create it.
        # For simplicity in this example, we'll assume direct creation or modification of the last element.
        if intent in ["set_text", "set_color", "set_background"] and generated_structure["elements"]:
            last_element = generated_structure["elements"][-1]
            if intent == "set_text" and "text_content" in entities:
                last_element["text"] = entities["text_content"]
            if intent == "set_color" and "color" in entities:
                color_val = entities["color"]
                if color_val in self.color_map:
                    last_element["textColor"] = self.color_map[color_val]
                else:
                    last_element["textColor"] = color_val
            if intent == "set_background" and "color" in entities:
                color_val = entities["color"]
                if color_val in self.color_map:
                    last_element["backgroundColor"] = self.color_map[color_val]
                else:
                    last_element["backgroundColor"] = color_val
            if intent == "set_background" and "image_path" in entities:
                last_element["backgroundImage"] = entities["image_path"]
        elif intent in ["set_text", "set_color", "set_background"] and not generated_structure["elements"]:
            # If no element exists, create one with the specified properties.
            # This is a simplification. In a real system, we'd need context to know which element to modify.
            element_type = "TextView" # Default type if intent is for setting properties
            if intent == "set_text":
                element_type = "TextView"
            elif intent == "set_color":
                 element_type = "TextView" # Or could be a Button, etc.
            elif intent == "set_background":
                element_type = "ConstraintLayout" # Or FrameLayout, etc.

            element_config = {"type": element_type, "id": f"id/generated_{len(generated_structure['elements'])}"}
            if "text_content" in entities and intent == "set_text":
                element_config["text"] = entities["text_content"]
            if "color" in entities:
                color_val = entities["color"]
                if color_val in self.color_map:
                    if intent == "set_color":
                        element_config["textColor"] = self.color_map[color_val]
                    elif intent == "set_background":
                        element_config["backgroundColor"] = self.color_map[color_val]
                else:
                    if intent == "set_color":
                        element_config["textColor"] = color_val
                    elif intent == "set_background":
                        element_config["backgroundColor"] = color_val
            if "image_path" in entities and intent == "set_background":
                element_config["backgroundImage"] = entities["image_path"]
            generated_structure["elements"].append(element_config)


        return generated_structure

class ArabicNLPModule:
    """
    Orchestrates the Arabic parsing and code structure generation.
    """
    def __init__(self, knowledge_base_dir, target_language):
        self.parser = ArabicParser(knowledge_base_dir)
        self.generator = ArabicGenerator(target_language)

    def process_arabic_input(self, arabic_text):
        """
        Processes natural language Arabic text to produce a structured code representation.

        Args:
            arabic_text (str): The natural language input in Arabic.

        Returns:
            dict: A structured representation of the desired code elements,
                  ready for code generation.
        """
        parsed_data = self.parser.parse(arabic_text)
        print(f"Parsed Arabic data: {parsed_data}")
        generated_structure = self.generator.generate_code_structure(parsed_data)
        print(f"Generated code structure: {generated_structure}")
        return generated_structure

# Example Usage (for demonstration, this part would be triggered by the main orchestrator)
if __name__ == "__main__":
    # Dummy values for demonstration
    KNOWLEDGE_BASE_DIR = "./dummy_kb"
    TARGET_LANGUAGE = "android_xml" # Example target

    # Create dummy knowledge base directory and files if they don't exist
    os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
    # In a real scenario, these files would contain actual keywords and patterns.
    # For this example, the logic is hardcoded in the classes.

    arabic_nlp_module = ArabicNLPModule(KNOWLEDGE_BASE_DIR, TARGET_LANGUAGE)

    # Test cases
    prompts = [
        "أنشئ زر بـ\"اضغط هنا\"",
        "أضف مربع نص بـ\"أدخل اسمك\"",
        "اجعل النص \"أهلاً بك\" في الزر السابق",
        "غيّر لون النص إلى الأحمر",
        "ضع خلفية سوداء",
        "أنشئ تصميم عمودي",
        "أنشئ زر بـ\"موافق\" ولون أزرق",
        "أضف نص بـ\"رسالة ترحيب\" بلون أصفر",
        "غيّر خلفية النص إلى صورة \"my_image.png\""
    ]

    for i, prompt in enumerate(prompts):
        print(f"\n--- Processing Prompt {i+1}: \"{prompt}\" ---")
        structured_output = arabic_nlp_module.process_arabic_input(prompt)
        # In a real system, this 'structured_output' would be passed to the
        # next lobe (e.g., Lobe 4_code_generation_lobe).
        print(f"Structured Output for Prompt {i+1}: {structured_output}")

    # Clean up dummy knowledge base directory
    if os.path.exists(KNOWLEDGE_BASE_DIR):
        try:
            shutil.rmtree(KNOWLEDGE_BASE_DIR)
            print(f"\nRemoved dummy knowledge base directory: {KNOWLEDGE_BASE_DIR}")
        except OSError as e:
            print(f"Error removing dummy knowledge base directory {KNOWLEDGE_BASE_DIR}: {e}")

    print("\n--- Arabic NLP Module Demo Finished ---")